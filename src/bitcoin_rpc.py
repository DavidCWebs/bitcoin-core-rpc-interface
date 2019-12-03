#!/usr/bin/env python3

import requests, json
from . import config

class BitcoinRPC:
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}

    def __init__(self, network=None):
        if network == None:
            network = "regtest"
        self.url = getattr(config, network)["url"]
        self.rpc_user = getattr(config, network)["rpc_user"]
        self.rpc_password = getattr(config, network)["rpc_password"]
        #self.report()

    def report(self):
        print("url: " + self.url)

    def call(self, rpc_method, *params):
        payload = json.dumps({"method": rpc_method, "params": list(params), "jsonrpc": "2.0"})
        try:
            response = requests.request(
                    "POST",
                    self.url,
                    data=payload,
                    headers=self.headers,
                    auth=(self.rpc_user, self.rpc_password)
                    )
            # print(response.status_code)
            # Return JSON format - handy since jq can be used for post-processing
            # if python format required, return json.loads(response.text)
            full = response.json()
            #return json_loads(full["result"])
            return json.dumps(full["result"])
        except requests.exceptions.RequestException as e:
            print(e)
        except:
            # Not acceptable, should check response codes - this is wrong message
            print("No response from " + self.url + ". Check bitcoind is running.")


