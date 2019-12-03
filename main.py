#!/usr/bin/env python3

from src.bitcoin_rpc import BitcoinRPC

def main():
    request = BitcoinRPC()
    #print(request.call("listunspent"))
    print(request.call("getblockhash", 1))
    print(request.call("getblockbyheight", 1))

    # Example showing multiple params
    # --------------------------------
    #print(request.call("listunspent", 0, 9999999, ["2N1sijJT3YMv1EctDnSpRNWgJm7U3pbr2iC"]))

if __name__ == '__main__':
    main()
