from web3 import HTTPProvider
from contract import Contract, W3
import unittest

w3 = W3(HTTPProvider('http://localhost:8545'), 6, 100000000000).instance()

class MyTest(unittest.TestCase):
    def test_invest(self):
        
        price_per_token = 1000
        token_value = 5

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tusd = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
     
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})
        tusd.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})
       
        #Crowdsale
        crowdsale = Contract("MintedCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[base_token.address, w3.eth.accounts[0], [tether.address,tusd.address], [price_per_token,price_per_token]]})
        base_token.instance.addMinter(crowdsale.address, transact={'from': w3.eth.accounts[0]})  

        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), 0)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

        tether.instance.approve(crowdsale.address,price_per_token*token_value, transact={'from': w3.eth.accounts[1]})
        crowdsale.instance.invest(price_per_token*token_value,tether.address, transact={'from': w3.eth.accounts[1]})
      
        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), token_value)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), token_value*price_per_token)
        
if __name__ == '__main__':
    unittest.main()
        