#!/usr/bin/env python3
import json
import requests
import sys

rpc_user = "david"
rpc_password = "2fd5934"
url = "http://192.168.122.18:18443"

def remote_call(method, params):
    payload = json.dumps({"method": method, "params": params})
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}
    try:
        response = requests.request("POST", url, data=payload, headers=headers, auth=(rpc_user, rpc_password))
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(e)
    except:
        print("No response from " + url + ". Check bitcoind is running.")

def main():
    if len(sys.argv) < 2:
        print("Please specify an RPC method.")
    method = sys.argv[1]
    answer = remote_call('listunspent', [])
    #answer = remote_call('getblockbyheight', [2])
    #answer = remote_call('listreceivedbyaddress', [])
    if answer['error']:
        print(answer['error'])
    else:
        print(json.dumps(answer['result']))

if __name__ == '__main__':
    main()


