import json
import os
from datetime import datetime
from typing import List

from assembling.dataset_labeler_abstract import BaseDatasetLabeler
from assembling.dataset_timeframe_aggregator import DatasetTimeframeAggregator
from common.common import load_json, prepare_directory, random_string
from indicators.indicator_abstract import BaseIndicator


class CryptoSeriesDatasetAssembler:
    dataset_out_root_folder = './out/datasets'

    def __init__(self,
                 instruments: List[str],
                 aggregation_window: int,
                 dataset_labeler: BaseDatasetLabeler,
                 raw_series_folder: str,
                 indicators: List[BaseIndicator] = None,
                 dataset_cleanup_keys: List[str] = None):
        self.instruments = instruments
        self.aggregation_window = aggregation_window
        self.indicators: List[BaseIndicator] = indicators
        self.dataset_labeler: BaseDatasetLabeler = dataset_labeler
        self.raw_series_folder = raw_series_folder
        self.dataset_unique_name = random_string()
        self.dataset_out_folder = os.path.join(self.dataset_out_root_folder, self.dataset_unique_name)
        prepare_directory(self.dataset_out_folder)
        self.dataset_cleanup_keys = set(dataset_cleanup_keys) if dataset_cleanup_keys else None

    def generate_dataset(self):
        for instrument in self.instruments:
            labeled_series = []
            self.dataset_labeler.reset()
            [indicator.reset() for indicator in self.indicators]
            timeframe_aggregator = DatasetTimeframeAggregator(60 * self.aggregation_window)
            aggregated_candles = []
            loaded_candles = 0
            for file in self._filter_and_sort_files(instrument):
                series = load_json(file)
                for candle in series:
                    loaded_candles = loaded_candles + 1
                    aggregated_candle = timeframe_aggregator.aggregate(candle)
                    if aggregated_candle:
                        aggregated_candles.append(aggregated_candle)
            aggregated_candle = timeframe_aggregator.get_aggregated_tail()
            if aggregated_candle:
                aggregated_candles.append(aggregated_candle)
            print(
                f'Instrument: {instrument}, loaded candles: {loaded_candles}, aggregated candles: {len(aggregated_candles)}')

            for i, candle in enumerate(aggregated_candles):
                for indicator in self.indicators:
                    indicator_value = indicator.apply(candle)
                    candle[indicator.get_name()] = indicator_value

            aggregated_candles = [candle for candle in aggregated_candles if
                                  all(value is not None for value in candle.values())]
            aggregated_candles = sorted(aggregated_candles, key=lambda x: x['t'])

            indicator_names = [indicator.get_name() for indicator in self.indicators]
            print(f"Instrument: {instrument}, indicators applied: {', '.join(indicator_names)}")

            for candle in aggregated_candles:
                labeled_window = self.dataset_labeler.apply(candle)
                if labeled_window:
                    labeled_series.append(labeled_window)

            print(f'{instrument}: {len(labeled_series)} examples assembled')

            self._cleanup_series(labeled_series, instrument)
            self._save_series(labeled_series, instrument)
        self._save_dataset_config()

    def _save_dataset_config(self):
        config = self._generate_dataset_config()
        config_path = os.path.join(self.dataset_out_root_folder, f'{self.dataset_unique_name}_dataset_config.json')
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=1)

        print(f"Config saved at: {config_path}")

    def _save_series(self, labeled_series: List[dict], instrument: str):
        for labeled in labeled_series:
            series = labeled['series']
            labels = labeled['labels']

            timestamp = series[0]['t']
            series_filename = f"{instrument}_{timestamp}.json"
            series_filepath = os.path.join(self.dataset_out_folder, series_filename)

            with open(series_filepath, 'w') as f:
                json.dump(series, f, indent=1)

            labels_filename = f"{instrument}_{timestamp}_labels.json"
            labels_filepath = os.path.join(self.dataset_out_folder, labels_filename)

            with open(labels_filepath, 'w') as f:
                json.dump(labels, f, indent=1)

    def _generate_dataset_config(self):
        config = {
            "instruments": self.instruments,
            "aggregation_window": self.aggregation_window,
            "labeling" : {
                "name" : self.dataset_labeler.get_name(),
                "training_window_length": self.dataset_labeler.training_window_length,
                "prediction_window_length" : self.dataset_labeler.prediction_window_length,
            },
            "indicators": [
                {
                    "name": indicator.get_name(),
                    "window_length": indicator.window_length
                } for indicator in self.indicators
            ]
        }
        return config

    def _cleanup_series(self, labeled_series, instrument):
        if not self.dataset_cleanup_keys:
            return

        for labeled in labeled_series:
            for candle in labeled['series']:
                for key in list(candle.keys()):
                    if key in self.dataset_cleanup_keys:
                        del candle[key]

    def _filter_and_sort_files(self, instrument):
        all_files = os.listdir(self.raw_series_folder)
        instrument_files = [f for f in all_files if f.startswith(instrument)]
        instrument_files.sort(key=lambda x: datetime.strptime(x.split('_')[1].split('.')[0], '%Y-%m-%d'))
        return [os.path.join(self.raw_series_folder, f) for f in instrument_files]
