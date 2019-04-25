from web3 import HTTPProvider
from contract import Contract, W3

w3 = W3(HTTPProvider('http://localhost:8545'), 6, 100000000000).instance()

for account in w3.eth.accounts:
    print("Account", account, "with balance:", w3.eth.getBalance(account))

tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})

tether.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
print(tether.instance.balanceOf(w3.eth.accounts[0]))

