# evaDB python wrapper

This is a simple wrapper around evaDB using python. This requires a running
evaDB instance, which will be used for individual requests.

## Setup

Install all python packages in `requirements.txt`. Python 3.8 is required.

Install package locally with `pip install -e .`.

## Examples

`example_calls_user.py` and `example_calls_admin.py` are small scripts that
contain a sequence of calls against EVAdb. These can be used as reference for
direct development on top of the requests-based interface.

## Roadmap

- [ ] Cover all evaDB user functionality
- [ ] Expose functionality as minimal flask jsonRPC server for frontend development
