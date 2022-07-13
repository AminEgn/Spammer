# request
import requests


def _exec(method, url, **kwargs):
    try:
        res = getattr(requests, method)(url, **kwargs)
    except Exception as e:
        raise e
    else:
        return res


def get(url, **kwargs):
    """get"""
    return _exec('get', url, **kwargs)


def post(url, **kwargs):
    """post"""
    return _exec('post', url, **kwargs)


def delete(url, **kwargs):
    """delete"""
    return _exec('delete', url, **kwargs)


def put(url, **kwargs):
    """put"""
    return _exec('put', url, **kwargs)
