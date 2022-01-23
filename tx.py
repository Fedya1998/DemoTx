import sys
PRIVATE_KEY = sys.argv[2]

from web3 import Web3
w3rin = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/46cdf84a608f468598ea90234fa5f9bc"))
w3rop = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/46cdf84a608f468598ea90234fa5f9bc"))

from web3.middleware import geth_poa_middleware
w3rin.middleware_onion.inject(geth_poa_middleware, layer=0)
w3rop.middleware_onion.inject(geth_poa_middleware, layer=0)


public_address_of_senders_account = '0xeB75f110985Ed415dD396eb96D617483Bdacddb0'
private_key_for_senders_account = PRIVATE_KEY

def send_ether(network, value, dest):
	if network == "rin":
		w3 = w3rin
	else:
		w3 = w3rop
	tx = {
		'nonce': w3.eth.get_transaction_count(public_address_of_senders_account),
	    'to': dest,
	  	'value': w3.toWei(value, 'ether'),
	    'gas': 2000000,
	    'gasPrice': w3.toWei('5', 'gwei')
	}

	signed_txn = w3.eth.account.sign_transaction(tx, private_key_for_senders_account)


	tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
	print(tx)
	return tx

#send_ether("rin", 0.0003, "0x9cc2534799Dc2106A00469039c8644Ca610a2A09")
#send_ether("rop", 0.0003, "0x9cc2534799Dc2106A00469039c8644Ca610a2A09")
