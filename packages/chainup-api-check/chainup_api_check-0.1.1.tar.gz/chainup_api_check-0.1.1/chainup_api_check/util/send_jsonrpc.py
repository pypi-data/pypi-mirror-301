import requests
import json


def send_rpc_request(url, method, params=None):
    """
    发送 JSON-RPC 请求
    """
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        "id": 1,
    }
    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(payload))
        # response.raise_for_status()
        if response.status_code == 200:
            return response.json()["result"], response.status_code
        else:
            return None, response.status_code
    except requests.exceptions.RequestException as e:
        return None, response.status_code if response else "N/A"


def send_get_request(url,  params=None):
    """
    发送 HTTP GET 请求
    """
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            url, headers=headers)
        # response.raise_for_status()
        if response.status_code == 200:
            return response.json(), response.status_code
        else:
            return None, response.status_code
    except requests.exceptions.RequestException as e:
        return None, response.status_code if response else "N/A"
