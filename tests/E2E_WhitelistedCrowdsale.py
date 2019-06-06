from web3 import HTTPProvider
from contract import Contract, W3
import unittest

w3 = W3().instance()

class MyTest(unittest.TestCase):
    def test_user_in_list(self):
        
        price_per_token = 1000
        token_value = 5

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
             
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})

        #Whitelist
        whitelist_crowdsale = Contract("WhitelistedCrowdsale", w3, {"owner": w3.eth.accounts[0], "args": [base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]}) 
        whitelist_crowdsale.instance.addWhitelisted(w3.eth.accounts[1], transact={'from': w3.eth.accounts[0]})
        base_token.instance.transfer(whitelist_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})    
       
        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), 0)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

        tether.instance.approve(whitelist_crowdsale.address,price_per_token*token_value, transact={'from': w3.eth.accounts[1]})
        whitelist_crowdsale.instance.invest(price_per_token*token_value,tether.address, transact={'from': w3.eth.accounts[1]})

        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), token_value)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), token_value*price_per_token)
     
    def test_user_not_in_list(self):
        
        price_per_token = 1000
        token_value = 5

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
             
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})

        #Whitelist
        whitelist_crowdsale = Contract("WhitelistedCrowdsale", w3, {"owner": w3.eth.accounts[0], "args": [base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]}) 
        base_token.instance.transfer(whitelist_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})    
        
        with self.assertRaises(ValueError):       
            tether.instance.approve(whitelist_crowdsale.address,price_per_token*token_value, transact={'from': w3.eth.accounts[1]})
            whitelist_crowdsale.instance.invest(price_per_token*token_value,tether.address, transact={'from': w3.eth.accounts[1]})   
        
if __name__ == '__main__':
    unittest.main()

