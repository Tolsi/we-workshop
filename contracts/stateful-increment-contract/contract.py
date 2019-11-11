import json
import os
import requests
import sys


def find_param_value(params, name):
    for param in params:
        if param['key'] == name: return param['value']
    return None


if __name__ == '__main__':
    command = os.environ['COMMAND']
    if command == 'CALL':
        node = os.environ['NODE']
        port = os.environ['NODE_PORT']
        contract_id = json.loads(os.environ['TX'])['contractId']
        if not node or not port: sys.exit(1)
        url = 'http://{0}:{1}/contracts/{2}/sum'.format(node, port, contract_id)
        r = requests.get(url, verify=False, timeout=2)
        data = r.json()
        value = data['value']
        print(json.dumps([{
            "key": "sum",
            "type": "integer",
            "value": value + 1}], separators=(',', ':')))
    elif command == 'CREATE':
        print(json.dumps([{
            "key": "sum",
            "type": "integer",
            "value": 0}], separators=(',', ':')))
    else:
        sys.exit(1)
