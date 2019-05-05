from web3 import HTTPProvider
from contract import Contract, W3
import unittest

w3 = W3(HTTPProvider('http://localhost:8545'), 6, 100000000000).instance()

class MyTest(unittest.TestCase):
    def test_on_pause(self):

        price_per_token = 1000
        token_value = 2

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
    
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})
                
        #Crowdsale
        pausable_crowdsale = Contract("PausableCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]})
        base_token.instance.transfer(pausable_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})
        pausable_crowdsale.instance.pause(transact={'from': w3.eth.accounts[0]})
        #Pause
        with self.assertRaises(ValueError):
            tether.instance.approve(pausable_crowdsale.address,token_value*price_per_token, transact={'from': w3.eth.accounts[1]})
            pausable_crowdsale.instance.invest(token_value*price_per_token,tether.address, transact={'from': w3.eth.accounts[1]})

    def test_without_pause(self):

        price_per_token = 1000
        token_value = 2

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})
                
        #Crowdsale
        pausable_crowdsale = Contract("PausableCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]})
        base_token.instance.transfer(pausable_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})
        
        #Pause
        pausable_crowdsale.instance.pause(transact={'from': w3.eth.accounts[0]})
        pausable_crowdsale.instance.unpause(transact={'from': w3.eth.accounts[0]})

        tether.instance.approve(pausable_crowdsale.address,token_value*price_per_token, transact={'from': w3.eth.accounts[1]})
        pausable_crowdsale.instance.invest(token_value*price_per_token,tether.address, transact={'from': w3.eth.accounts[1]})

        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), token_value)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), token_value*price_per_token)
        
if __name__ == '__main__':
    unittest.main()

