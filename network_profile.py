#!/usr/bin/env python3
#
#   Copyright 2018 Filip Krestan <krestfi1@fit.cvut.cz>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import datetime
import json
import logging
from pathlib import Path

import pandas
import fbprophet

IP_PROTO_TRANS_TABLE = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP',
    # These do not have enough traffic (statistics do not work too well)
    # 41: 'IPv6 Encapsulation',
    # 47: 'GREs',
    # 50: 'ESP',
    # 132: 'SCTP'
}

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s'

PROPHET_CHANGEPOINT_PRIOR_SCALE = 0.01
PROPHET_PREDICT_PERIODS = 24


def load_data(data_file_path):
    logging.debug('Loading data from %s', data_file_path)
    data = pandas.read_csv(
        data_file_path,
        parse_dates=['time TIME_FIRST', 'time TIME_LAST'],
        infer_datetime_format=True,
        dtype={
            'uint64 BYTES': 'uint64',
            'uint32 COUNT': 'uint32',
            'uint32 PACKETS': 'uint32',
            'uint8 PROTOCOL': 'uint8'
        })
    data.rename(
        columns={
            'uint64 BYTES': 'bytes',
            'time TIME_FIRST': 'time_first',
            'time TIME_LAST': 'time_last',
            'uint32 COUNT': 'flow_count',
            'uint32 PACKETS': 'packets',
            'uint8 PROTOCOL': 'protocol'
        },
        inplace=True)

    return data


def make_forecast(data):
    logging.debug('Computing forecast: changepoint_prior_scale: %d. predict_periods: %d',
                  PROPHET_CHANGEPOINT_PRIOR_SCALE, PROPHET_PREDICT_PERIODS)
    model = fbprophet.Prophet(changepoint_prior_scale=PROPHET_CHANGEPOINT_PRIOR_SCALE).fit(data)
    future = model.make_future_dataframe(
        periods=PROPHET_PREDICT_PERIODS, freq='H', include_history=False)
    forecast = model.predict(future)

    return forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].to_dict('index')


def make_profile(data_file_path):
    forecasts = dict()
    data = load_data(data_file_path)

    for ip_proto_num, name in IP_PROTO_TRANS_TABLE.items():
        forecasts[name] = dict()
        # Filter data by protocol number
        proto_data = data.loc[data['protocol'] == ip_proto_num]

        for metric in ['bytes', 'packets', 'flow_count']:
            # Prepare data for FBProphet expected format
            proto_data_prophet = proto_data[['time_first', metric]].rename(columns={
                'time_first': 'ds',
                metric: 'y'
            })
            # Drop top 5% values (outliers)
            proto_data_prophet_95th = proto_data_prophet.loc[
                proto_data_prophet['y'] <= proto_data_prophet['y'].quantile(0.95)]
            logging.debug('Generating forecast for "%s" "%s" metric', name, metric)
            forecasts[name][metric] = {
                k.isoformat(): v
                for k, v in make_forecast(proto_data_prophet_95th).items()
            }

    return forecasts


def parse_args():
    """Parse arguments and return parsed options."""
    parser = argparse.ArgumentParser(
        description=
        'Generate "prediction profile" based on aggregated historical network data. See README.md for details about data format.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        dest='loglevel',
        action='store_const',
        const=logging.DEBUG,
        default=logging.INFO,
        help='Increase logging verbosity')
    parser.add_argument('data_root', help='Path to data root directory')
    return parser.parse_args()


def main():
    # fbprophet.logging.
    args = parse_args()
    logging.basicConfig(level=args.loglevel, format=LOG_FORMAT)

    directories = [
        x for x in Path(args.data_root).glob('????????-????-????-????-????????????') if x.is_dir()
    ]

    for directory in directories:
        logging.info('Processing %s', directory)

        data_path = directory / 'data.csv'

        profile = make_profile(str(data_path))
        profile_json = json.dumps(profile)

        profile_path = directory / 'profile-{}.json'.format(datetime.datetime.now().isoformat())
        logging.info('Writing profile to %s', profile_path)
        profile_path.write_text(profile_json)
        latest_link_path = directory / 'latest.json.new'
        latest_link_path.symlink_to(profile_path.name)
        latest_link_path.replace(directory / 'latest.json')


if __name__ == '__main__':
    main()
