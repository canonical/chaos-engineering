# Contributing

## Style Guide

Please follow the [Canonical Documentation Style Guide](https://docs.ubuntu.com/styleguide/en).

## Build and test the documentation

To build and run this documentation locally, run: 

```bash
cd docs
make install
make run
```

Documentation page will be available at http://127.0.0.1:8000

## Running automated documentation checks

There are some automated documentation checks you may want to run to validate your changes. To do that, run:

```bash
cd docs
make install
make spelling
make woke
```
