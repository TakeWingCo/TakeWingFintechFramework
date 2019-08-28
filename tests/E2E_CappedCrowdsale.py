import unittest
import time

from web3 import Web3, HTTPProvider
from ethtools import EthTools
from ethtools import EthServer

class MyTest(unittest.TestCase):
    def test_cap(self):

        price_per_token = 1000
        token_value = 5
        cap = token_value * 2

        eth = EthTools("http://localhost:5000")
        eth.init_fixtures("/var/lib/takewing/tests/fixtures.json")
        
        #Tokens
        base_token = eth.filter(name="BaseToken").contract
        tether = eth.filter(name="Tether").contract
        
        #Accounts
        deployer = eth.filter(role="Deployer").accounts[0].address
        tester = eth.filter(role="Tester").accounts[0].address
        eth.filter(role="Tester").unlock()

        base_token.instance.mint(deployer, 100, transact={'from': deployer})
        tether.instance.mint(tester, 100000, transact={'from': deployer})
                
        #Crowdsale
        capped_crowdsale = eth.filter(name="CappedCrowdsale").contract
        base_token.instance.transfer(capped_crowdsale.address,100, transact={'from': deployer})
        
        self.assertEqual(base_token.instance.balanceOf(tester), 0)
        self.assertEqual(tether.instance.balanceOf(deployer), 0)

        #Invest
        tether.instance.approve(capped_crowdsale.address,price_per_token * token_value, transact={'from': tester})
        capped_crowdsale.instance.invest(price_per_token * token_value,tether.address, transact={'from': tester})

        with self.assertRaises(ValueError):
            tether.instance.approve(capped_crowdsale.address,price_per_token * token_value * 2, transact={'from': tester})
            capped_crowdsale.instance.invest(price_per_token * token_value * 2,tether.address, transact={'from': tester})

        tether.instance.approve(capped_crowdsale.address,price_per_token * token_value, transact={'from':tester})
        capped_crowdsale.instance.invest(price_per_token * token_value,tether.address, transact={'from': tester})
        
        with self.assertRaises(ValueError):
            tether.instance.approve(capped_crowdsale.address,price_per_token * token_value, transact={'from': tester})
            capped_crowdsale.instance.invest(price_per_token * token_value,tether.address, transact={'from': tester})

        self.assertEqual(base_token.instance.balanceOf(tester), token_value * 2)
        self.assertEqual(tether.instance.balanceOf(deployer), price_per_token * token_value * 2)

                
EthServer('/var/lib/takewing/tests/config.json')
time.sleep(3)

if __name__ == '__main__':
    unittest.main()
