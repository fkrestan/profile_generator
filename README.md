Network Profile Service
=======================

This scripts generates network "profile" based on network communication history.
The profile contains hourly prediction (read estimate) of the several network
utilization metrics: packet, byte and flow count. The actual metric ultimately
depends on the supplied data, but the example [NEMEA][1] config provided generates
the metric sum over one hour period.

The prediction heavily relies on [Facebook Prophet][2].


Usage
-----

``` shell
usage: network_profile.py [-h] [-v] data_root

Generate "prediction profile" based on aggregated historical network data. See
README.md for details about data format.

positional arguments:
  data_root      Path to data root directory

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Increase logging verbosity
```

The `data_root` needs to have specific structure: `$DATA_ROOT/$PREFIX_TAG/data.csv`.
There can be multiple `$PREFIX_TAG` folders, where `$PREFIX_TAG` is positive
integer used to identify the network prefix (see [prefix_tags NEMEA module][3]).
See input and output data formats.


Input Data Format
-----------------

The input data file must be located in `$DATA_ROOT/$PREFIX_TAG/data.csv`. These are
basically an output of [NEMEA][1] Aggregator plugin written by `logger` plugin.
The example `.sup` NEMEA configuration can be found in `NEMEA_example_config.sup`
file.

```csv
uint64 BYTES,time TIME_FIRST,time TIME_LAST,uint32 COUNT,uint32 PACKETS,uint8 PROTOCOL
22117876394,2018-08-19T18:48:34.098,2018-08-19T19:48:34.555,913260,38307749,17
124839591977,2018-08-19T18:48:25.766,2018-08-19T19:48:34.051,2842950,108201719,6
...
```

The `BYTES`, `PACKETS` and `COUNT` should contain a sum of byte, packet and flow
count observed in the time period given in `TIME_FIRST` and `TIME_LAST` period.
Each time period should span one hour and not overlap with each other.


Output Data Format
------------------

Output data are written to `$DATA_ROOT/$PREFIX_TAG/profile-$TIMESTAMP.json`,
where `$TIMESTAMP` is ISO8601 timestamp. Also, `$DATA_ROOT/$PREFIX_TAG/latest.json`
symlink always points to the latest profile. The format is best described by
example (see "comments" inline):

```
{
  // Protocol identified by ip protocol number (by default `TCP`, `UDP`, `ICMP`)
  "TCP": {
    // Metric - currently `bytes`, `packets` or `flow_count`
    "bytes": {
       // Start of the 1 hour period in ISO8601 timestamp
      "2018-09-03T08:39:28.705000": {
        // Predicted value of metric
        "yhat": 143619009181.51968,
        // Lower bound of predicted value of metric
        "yhat_lower": 106421980435.8867,
        // Upper bound of predicted value of metric
        "yhat_upper": 180611097587.87106
      },
      ...
    },
    "packets": {
      "2018-09-03T08:39:28.705000": {
        "yhat": 132767186.71602453,
        "yhat_lower": 104456788.4368862,
        "yhat_upper": 162249041.21929315
      },
      ...
    },
    "flow_count": {
      "2018-09-03T08:39:28.705000": {
        "yhat": 5207526.119025636,
        "yhat_lower": 3498401.1832782286,
        "yhat_upper": 6998606.405906358
      },
      ...
    },
  },
  ...
}
```

[1]: https://github.com/CESNET/Nemea
[2]: https://facebook.github.io/prophet/
[3]: https://github.com/CESNET/Nemea-Modules/tree/master/prefix_tags
