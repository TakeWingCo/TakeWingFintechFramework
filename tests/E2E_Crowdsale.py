import unittest
import time

from web3 import Web3
from ethtools import EthTools
from ethtools import EthServer

class MyTest(unittest.TestCase):
    def test_invest(self):

        price_per_token = 1000
        token_value = 2

        eth = EthTools("http://localhost:5000")
        eth.init_fixtures("/var/lib/takewing/tests/fixtures.json")

        #Tokens
        base_token = eth.filter(name="BaseToken").contract
        tether = eth.filter(name="Tether").contract

        #Accounts
        deployer = eth.filter(role="Deployer").accounts[0].address
        tester = eth.filter(role="Tester").accounts[0].address
        eth.filter(role="Tester").unlock()

        #Crowdsale
        crowdsale = eth.filter(name="Crowdsale").contract
        base_token.instance.transfer(crowdsale.address, 100, transact={'from': deployer})

        self.assertEqual(base_token.instance.balanceOf(tester), 0)
        self.assertEqual(tether.instance.balanceOf(deployer), 0)

        tether.instance.approve(crowdsale.address,token_value*price_per_token, transact={'from': tester})
        crowdsale.instance.invest(token_value*price_per_token,tether.address, transact={'from': tester})

        self.assertEqual(base_token.instance.balanceOf(tester), token_value)
        self.assertEqual(tether.instance.balanceOf(deployer), token_value*price_per_token)


EthServer('/var/lib/takewing/tests/config.json')
time.sleep(3)
        
if __name__ == '__main__':
    unittest.main()
    
