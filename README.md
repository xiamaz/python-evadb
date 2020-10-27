# evaDB python wrapper

This is a simple wrapper around evaDB using python. This requires a running
evaDB instance, which will be used for individual requests.

## Setup

Install all python packages in `requirements.txt`. Python 3.8 is required.

Install package locally with `pip install -e .`.

## Test run

Running `python -m evadb` will test some of the available requests. The
`evadb/__main__.py` also can be used as reference for calling against evaDB.

## Roadmap

- [ ] Cover all evaDB user functionality
- [ ] Expose functionality as minimal flask jsonRPC server for frontend development
