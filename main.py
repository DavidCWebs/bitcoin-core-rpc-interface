#!/usr/bin/env python3
import sys

from src.bitcoin_rpc import BitcoinRPC

def main(config_file):
    request = BitcoinRPC(config_file)
    #print(request.call("listunspent"))
    #print(request.call("getblockhash", 1))

    # Example showing multiple params
    # --------------------------------
    adds = ["2N1sijJT3YMv1EctDnSpRNWgJm7U3pbr2iC"]
    # print(request.call("listunspent", 0, 9999999, ["2N1sijJT3YMv1EctDnSpRNWgJm7U3pbr2iC"]))
    print(request.call("listunspent", 0, 9999999, adds))

    params = "f44df8d739d61ec181e9045762fbc07c80c75c5b608b4ecea98af8098d7d9f98"
    print(request.call("gettransaction", params))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main("src/config.json")
