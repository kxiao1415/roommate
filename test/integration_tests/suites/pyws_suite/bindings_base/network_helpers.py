import sys
import requests
import httplib
import urllib3
import json

DEFAULT_ENCODING = 'utf-8'
HOST = 'localhost'
PORT = 5000


def post_file_to_url(token, url, field_name, path, headers=None, data=None):
    if headers is None:
        headers = {'X-TOKEN': token}

    files = {field_name: open(path, 'rb')}
    response = requests.post(url, files=files, verify=False, headers=headers, data=data)

    return response


def http_request(interface, token=None, data='', headers=None, verb="POST"):
    urllib3.disable_warnings()

    if headers is None:
        headers = _get_headers(token)
    else:
        for header, value in _get_headers(token):
            headers[header] = value

    json_data = json.dumps(data)

    try:
        conn = _get_http_client(HOST, PORT)
        conn.request(verb, interface, json_data, headers)
        response = conn.getresponse()

        if response.status != 200:
            print('response.status={0}'.format(response.status))
            print('response.msg={0}'.format(response.msg))
            print('response.reason={0}'.format(response.reason))

    except Exception as e:
        err_msg = "{0}\n host={1}\n port={2}\n data={3}".format(
            e,
            HOST,
            PORT,
            json_data
        )
        print('Caught Exception!\n {0}'.format(err_msg))

    else:
        return response.read()


def _get_http_client(host, port):
    try:
        conn_str = '{0}:{1}'.format(host, port)
        conn = httplib.HTTPConnection(conn_str, timeout=120)
    except Exception as e:
        print('method _get_http_client caught an exception: {0}'.format(str(e)), 'error')
        sys.exit(1)
    else:
        return conn


def _get_headers(token):
    return {
        "Content-Type": "application/json",
        "X-TOKEN": token
    }
