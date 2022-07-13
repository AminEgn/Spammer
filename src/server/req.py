# standard
from re import search
# internal
from src.server import httpclient as hc


def get(url, **kwargs):
    """get"""
    response = hc.get(url, **kwargs)
    status_code = response.status_code
    if status_code == 200 or status_code == 201:
        return True, response
    else:
        print(f'{response.reason}<{status_code}> --- {response.text}')
        return False


def post(url, **kwargs):
    """post"""
    response = hc.post(url, **kwargs)
    status_code = response.status_code
    if status_code == 200 or status_code == 201 or status_code == 204:
        return True, response
    # check if object is already exists on server
    # elif status_code == 400 and search('this mid already exists', response.json()['mid'][0]):
    #     return True, response
    else:
        print(f'{response.reason}<{status_code}> --- {response.text}')
        return False


def put(url, **kwargs):
    """put"""
    response = hc.put(url, **kwargs)
    status_code = response.status_code
    if status_code == 200 or status_code == 201 or status_code == 204:
        return True, response
    else:
        print(f'{response.reason}<{status_code}> --- {response.text}')
        return False


def delete(url, **kwargs):
    """delete"""
    response = hc.delete(url, **kwargs)
    status_code = response.status_code
    if status_code == 200 or status_code == 201 or status_code == 204 or status_code == 404:
        return True, response
    else:
        print(f'{response.reason}<{status_code}> --- {response.text}')
        return False
