from web3 import HTTPProvider
from contract import Contract, W3
import unittest

w3 = W3().instance()

class MyTest(unittest.TestCase):
    def test_cap(self):

        price_per_token = 1000
        token_value = 5
        cap = token_value * 2
        

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})
                
        #Crowdsale
        capped_crowdsale = Contract("CappedCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[cap, base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]})
        base_token.instance.transfer(capped_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})
        
        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), 0)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

        #Invest
        tether.instance.approve(capped_crowdsale.address,price_per_token * token_value, transact={'from': w3.eth.accounts[1]})
        capped_crowdsale.instance.invest(price_per_token * token_value,tether.address, transact={'from': w3.eth.accounts[1]})

        with self.assertRaises(ValueError):
            tether.instance.approve(capped_crowdsale.address,price_per_token * token_value * 2, transact={'from': w3.eth.accounts[1]})
            capped_crowdsale.instance.invest(price_per_token * token_value * 2,tether.address, transact={'from': w3.eth.accounts[1]})

        tether.instance.approve(capped_crowdsale.address,price_per_token * token_value, transact={'from': w3.eth.accounts[1]})
        capped_crowdsale.instance.invest(price_per_token * token_value,tether.address, transact={'from': w3.eth.accounts[1]})
        
        with self.assertRaises(ValueError):
            tether.instance.approve(capped_crowdsale.address,price_per_token * token_value, transact={'from': w3.eth.accounts[1]})
            capped_crowdsale.instance.invest(price_per_token * token_value,tether.address, transact={'from': w3.eth.accounts[1]})

        self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[1]), token_value * 2)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), price_per_token * token_value * 2)
                

if __name__ == '__main__':
    unittest.main()
