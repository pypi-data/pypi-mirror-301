# --------------------------------------------------------------------------------
# Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
# Last updated 2022.
#
# DataRobot, Inc. Confidential.
# This is proprietary source code of DataRobot, Inc. and its affiliates.
#
# This file and its contents are subject to DataRobot Tool and Utility Agreement.
# For details, see
# https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
# --------------------------------------------------------------------------------
from typing import List
from typing import NamedTuple
from typing import Union

import pandas as pd
from datarobot_mlops.drift.metrics import _psi_for_bin
from datarobot_mlops.stats_aggregator import FeatureType

BIN_VALUES_COLUMN = "Bin Values"
BASELINE_HIST_VALUES_COLUMN = "Baseline"
CURRENT_HIST_VALUES_COLUMN = "Current"

HISTOGRAMS_PLOT_DEFAULTS = {
    "kind": "bar",
    "fontsize": 6,
    "rot": 25,
    "colormap": "tab20",
    "figsize": (8, 6),
}

WORDCLOUD_PLOT_DEFAULTS = {
    "background_color": "white",
    "width": 800,
    "height": 600,
    "colormap": "tab20",
}


class FeatureDistributions(NamedTuple):
    """
    Class containing all necessary info to compute drift metrics.
    """

    feature_name: str
    feature_type: str
    bin_values: List[str]
    ref_histogram: Union[List[int], List[float]]
    expected_sample_size: int
    com_histogram: Union[List[int], List[float]]
    actual_sample_size: int

    def to_df(self, limit=25) -> pd.DataFrame:
        if self.feature_type == FeatureType.TEXT_WORDS:
            return pd.DataFrame.from_records(self._get_bin_details()[:limit])
        indices = []
        missing_index = -1
        oov_index = -1
        for i in range(len(self.bin_values)):
            bin_value = self.bin_values[i]
            if bin_value == "__oov__":
                oov_index = i
                continue
            if bin_value == "__missing__":
                missing_index = i
                continue
            indices.append(i)
        if self.feature_type == FeatureType.CATEGORY:
            indices.sort(key=lambda index: self.ref_histogram[index], reverse=True)
        bin_values = [self.bin_values[i] for i in indices]
        ref_values = [self.ref_histogram[i] for i in indices]
        com_values = [self.com_histogram[i] for i in indices]
        if len(bin_values) > limit:
            bin_values = bin_values[:25] + ["others"]
            ref_values = ref_values[:25] + [sum(ref_values[25:])]
            com_values = com_values[:25] + [sum(com_values[25:])]
        if missing_index >= 0:
            bin_values.append("missing")
            ref_values.append(self.ref_histogram[missing_index])
            com_values.append(self.com_histogram[missing_index])
        if oov_index >= 0:
            bin_values.append("new levels")
            ref_values.append(self.ref_histogram[oov_index])
            com_values.append(self.com_histogram[oov_index])
        df = pd.DataFrame(
            {
                BIN_VALUES_COLUMN: bin_values,
                BASELINE_HIST_VALUES_COLUMN: ref_values,
                CURRENT_HIST_VALUES_COLUMN: com_values,
            }
        )
        df[BASELINE_HIST_VALUES_COLUMN] = (
            df[BASELINE_HIST_VALUES_COLUMN] / self.expected_sample_size
        )
        df[CURRENT_HIST_VALUES_COLUMN] = df[CURRENT_HIST_VALUES_COLUMN] / self.actual_sample_size
        return df

    def _get_bin_details(self):
        result = []
        total_expected = sum(self.ref_histogram)
        total_actual = sum(self.com_histogram)
        if total_expected == 0 or total_actual == 0:
            return result
        for bin_value, expected, actual in zip(
            self.bin_values, self.ref_histogram, self.com_histogram
        ):
            score = _psi_for_bin(expected, actual, total_expected, total_actual)
            if score is None:
                continue
            training_frequency = float(expected) / total_expected
            prediction_frequency = float(actual) / total_actual
            frequency_score = training_frequency - prediction_frequency
            result.append(
                {
                    "bin_name": bin_value,
                    "drift_score": score,
                    "frequency_score": frequency_score,
                    "training_frequency": training_frequency,
                    "prediction_frequency": prediction_frequency,
                }
            )
        score_sum = sum(info["drift_score"] for info in result)
        max_frequency = max(info["frequency_score"] for info in result)
        normilized_result = [dict(info) for info in result]
        for info in normilized_result:
            info["drift_score"] /= score_sum
            info["frequency_score"] /= max_frequency
        normilized_result.sort(key=lambda x: x["drift_score"], reverse=True)
        return normilized_result

    def plot(self, *args, **kwargs):
        if self.feature_type == FeatureType.TEXT_WORDS:
            self._plot_text(**kwargs)
        else:
            self._plot_default(*args, **kwargs)

    def _plot_default(self, *args, **kwargs):
        df = self.to_df()
        defaults = dict(HISTOGRAMS_PLOT_DEFAULTS)
        defaults["xlabel"] = self.feature_name
        defaults.update(kwargs)
        defaults["x"] = BIN_VALUES_COLUMN
        defaults["y"] = [BASELINE_HIST_VALUES_COLUMN, CURRENT_HIST_VALUES_COLUMN]
        df.plot(**defaults)

    def _plot_text(self, *args, **kwargs):
        import matplotlib  # type: ignore
        import matplotlib.pyplot as plt  # type: ignore
        from wordcloud import WordCloud  # type: ignore

        infos = self._get_bin_details()[:2000]
        params = dict(WORDCLOUD_PLOT_DEFAULTS)
        params.update(kwargs)
        frequencies = {info["bin_name"]: info["drift_score"] for info in infos}
        wc = WordCloud(**params).generate_from_frequencies(frequencies)
        plt.imshow(wc)
        plt.xlabel(self.feature_name)
        plt.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
        plt.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())
