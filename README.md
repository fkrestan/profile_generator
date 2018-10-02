Network Profile Service
=======================

Usage
-----




Input Data Format
-----------------

The input data file must be located in `$DATAFILE/$UUID/data.csv`. These are
basically an output of [NEMEA][1] Aggregator plugin written by `logger` plugin (TODO
write actual description of data fields). The example `.sup` NEMEA configuration
can be found in `NEMEA_example_config.sup` file.

```csv
uint64 BYTES,time TIME_FIRST,time TIME_LAST,uint32 COUNT,uint32 PACKETS,uint8 PROTOCOL
22117876394,2018-08-19T18:48:34.098,2018-08-19T19:48:34.555,913260,38307749,17
124839591977,2018-08-19T18:48:25.766,2018-08-19T19:48:34.051,2842950,108201719,6
...
```


Output Data Format
------------------

Output data are written to `$DATAFILE/$UUID/profile-$TIMESTAMP.json`. Also,
`$DATAFILE/$UUID/latest.json` symlink always points to the latest profile. The
format is best described by example (see "comments" inline):

```json
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
    }
  },
  ...
}
```

[1]: https://github.com/CESNET/Nemea
