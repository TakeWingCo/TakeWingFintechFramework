from web3 import HTTPProvider
from contract import Contract, W3
import unittest
import time

w3 = W3(HTTPProvider('http://localhost:8545'), 6, 100000000000).instance()

class MyTest(unittest.TestCase):
    def test_timed(self):

        price_per_token = 1000
        token_value = 2

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
    
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        tether.instance.mint(w3.eth.accounts[1], 100000, transact={'from': w3.eth.accounts[0]})
                
        #Crowdsale
        block = w3.eth.getBlock("latest")["timestamp"]
        timed_crowdsale = Contract("TimedCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[block + 5,block + 10, base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]})
        base_token.instance.transfer(timed_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})
           
        #before
        with self.assertRaises(ValueError):
            tether.instance.approve(timed_crowdsale.address,token_value*price_per_token, transact={'from': w3.eth.accounts[1]})
            timed_crowdsale.instance.invest(token_value*price_per_token,tether.address, transact={'from': w3.eth.accounts[1]})

        time.sleep(6)   

        #opened
        tether.instance.approve(timed_crowdsale.address,token_value*price_per_token, transact={'from': w3.eth.accounts[1]})
        timed_crowdsale.instance.invest(token_value*price_per_token,tether.address, transact={'from': w3.eth.accounts[1]})

        time.sleep(6)
    
        #closed
        with self.assertRaises(ValueError):
            tether.instance.approve(timed_crowdsale.address,token_value*price_per_token, transact={'from': w3.eth.accounts[1]})
            timed_crowdsale.instance.invest(token_value*price_per_token,tether.address, transact={'from': w3.eth.accounts[1]})
        

if __name__ == '__main__':
    unittest.main()

