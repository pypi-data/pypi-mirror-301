# target-clickhouse

### Quick Start

1. Create a python virtual environment
2. install target-clickhouse, `pip install yw-etl-target-clickhouse`
3. pipe data to target

```shell
$ <some-tap> | <venv-bin>/target-clickhouse -c '<config-json>'
```

### Response to Different Types of Message

Only `RECORD` message is processed.

target-clickhouse uses the "stream" field of `RECORD` message to decide into what table the data is inserted into.
Configuration document should provide a mapping,`sync.stream_table_map`, between stream name and destination table.

target-clickhouse processes and accumulates `RECORD` message of a stream into a CSV file
and relies
on [HTTP interface](https://stackoverflow.com/questions/52002023/how-to-insert-data-to-clickhouse-from-file-by-http-interface)
to perform bulk load.

### Target Configuration Document

```json5
{
  // mandatory
  connection: {
    host: '...',
    port: '...',
    username: '...',
    password: '...',
  },
  // mandatory
  'sync.stream_table_map': {
    '<stream-name>': '<database>.<table-name>',
  },
  // optional
  // working directory precedence:
  // 1. conf["sync.working_directory"]
  // 2. env["TARGET_CLICKHOUSE_HOME"]
  // 3. $HOME/.target-clickhouse
  // path is relative to $PWD
  'sync.working_directory': '...',
  // optional
  // default to false
  'sync.retain_csv': false,
}
```

## Developer Guide

The idea behind `target-clickhouse` is rather simple: read from stdin and take action according to received message.

### Message Format

`tap-clickhouse` expects to see a stream of [JSON-line](https://jsonlines.org/).
The emitted message format follows
the [Singer Specification](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md#output).
Current implementation will only process RECORD message.

### Loading Mechanism

It is very inefficient to perform `INSERT` on clickhouse where bulk loads perform much more better. Therefore, `target-clickhouse` buffers all the `RECORD` messages into a CSV file and after the input stream closes, perform HTTP-based file upload action on Clickhouse. Intermediate CSV files are saved inside **working directory**, and a configuration entry
`sync.retain_csv` controls whether the CSV file is dropped after uploading to Clickhouse.

# Publish

create a file in ~/.pypirc and save username, password.

```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = xxxx
password = xxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = xxxx
password = xxxx
```

```shell
python -m build
```

```shell
python -m twine upload --repository pypi dist/*
```
