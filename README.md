Bitcoin RPC Interface
=====================
This article describes running a Bitcoin Core node on a virtual machine (Ubuntu 18.04) and accessing functionality through the RPC interface from a different computer on the same network.

You might need this if you are compiling and testing Bitcoin Core and want to keep the test instance completely separate from a running full node that is being used to manage funds.

Pre-requisites
--------------
* [Bitcoin core][1] installed on one computer.
* [curl][2] installed on the client computer - a convenient way to transfer HTTP data on the command line.
* [jq][3] for filtering and displaying JSON data on the command line - used to display data returned by curl requests.

Bitcoin Configuration
---------------------
Create a configuration file `~/.bitcoin/bitcoin.conf` with the following content:

```bash
# ~/.bitcoin/bitcoin.conf

# These settings apply to the regtest network only
[regtest]
rpcbind=0.0.0.0
rpcallowip=192.168.122.0/24 # Allow access fromm the 192.168.122 subnet
server=1 # Tells the bitcoin server to accept JSON-RPC commands
rpcuser=yourusername # Required for the JSON-RPC API
rpcpassword=yourpassword # Required

```
Note that you must specify `rpcallowip` - by default, only RPC connections from localhost are permitted. You can specify multiple `rpcallowip` on multiple lines.

To determine the necessary subnet, run `ip a | grep inet` on the client Ubuntu instance and look for the relevant IPv4 address.

You may not use `*` as a wildcard - instead, use CIDR notation to specify a subnet (so specify `192.168.122.0/24`, not `192.168.122.0.*`.

If necessary, you could lock access to a single machine on the subnet (e.g. the host computer running the VM) by adding the full IP address for the host's virtual bridge interface. To determine this, run `ip a` on the host computer and look for the `inet` ip address that shares a subnet with the client VM (i.e. the first 3 bytes of the client i VM's IP).


Start bitcoind
--------------
To start Bitcoin regtest local test network, with the REST API enabled: 

```bash
bitcoind -regtest -rest=1
```

Access RPC Through the command line
-----------------------------------
```bash
curl --user csknk:151b7e69 \
--data-binary '{"jsonrpc":"1.0","id":"curltext","method":"listunspent","params":[]}' \
-H 'content-type:text/plain;' http://192.168.122.18:18443/ \
| jq '.result[] | {address: .address,txid: .txid, amount: .amount, vout: .vout}'
```

Output:

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1520  100  1452  100    68   255k  12263 --:--:-- --:--:-- --:--:--  283k
{
  "address": "2N1sijJT3YMv1EctDnSpRNWgJm7U3pbr2iC",
  "txid": "bfe362293ecb042915d6b451bd02f0d12607679f8e9f2ffe4c605bdf91b7394a",
  "amount": 50,
  "vout": 0
}
{
  "address": "2N1sijJT3YMv1EctDnSpRNWgJm7U3pbr2iC",
  "txid": "f44df8d739d61ec181e9045762fbc07c80c75c5b608b4ecea98af8098d7d9f98",
  "amount": 50,
  "vout": 0
}
{
  "address": "2N1sijJT3YMv1EctDnSpRNWgJm7U3pbr2iC",
  "txid": "282448e328b48b1cf136c2ec2a1c9c84d56cce3378177106c73b3ac1535857bc",
  "amount": 50,
  "vout": 0
}

```
Using the Command Line
----------------------
In the `curl` example shown above, there are no shell variables, and variable expansion is not an issue.

Consider the following example:

```bash
# assign a transaction id to a shell variable
TXID=f44df8d739d61ec181e9045762fbc07c80c75c5b608b4ecea98af8098d7d9f98

curl --user csknk:151b7e69 \
--data-binary '{"jsonrpc":"1.0","id":"curltext","method":"gettransaction","params":["'${TXID}'"]}' \
-H 'content-type:text/plain;' http://127.0.0.1:5555/ | jq
```
Note that the `--data-binary` data is enclosed in single quotes - this is necessary so that the shell interprets the data as a single parameter, regardless of spaces.

The single quotes pass all the enclosed data verbatim - including the double quotes, which are necessary for the payload to be properly formed JSON.

Where the variable `$TXID` is inserted in the middle of the single quoted section, the single quotes must be ended so that the shell can expand the variable and restarted after the variable.

References
----------
* [http authentication with curl][3]

[1]: https://github.com/bitcoin/bitcoin
[2]: https://curl.haxx.se/
[3]: https://ec.haxx.se/cmdline-passwords.html?q=
