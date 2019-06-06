from web3 import HTTPProvider
from contract import Contract, W3
import unittest
import time

w3 = W3().instance()

class MyTest(unittest.TestCase):
    def test_refund(self):

        price_per_token = 1000
        token_value = 5
        goal = token_value * 4

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        
        
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        for i in range(1,4):
            tether.instance.mint(w3.eth.accounts[i], 100000, transact={'from': w3.eth.accounts[0]})
            before = tether.instance.balanceOf(w3.eth.accounts[i])
            
        #Crowdsale
        block = w3.eth.getBlock("latest")["timestamp"]
        refundable_crowdsale = Contract("RefundableCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[goal, block + 5, block + 7, base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]})
        base_token.instance.transfer(refundable_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})
        
        #AssertEqual
        for i in range(1,4):
            self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[i]), 0)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

        #Invest
        time.sleep(6)
        
        for i in range(1,4):
            tether.instance.approve(refundable_crowdsale.address,price_per_token * token_value, transact={'from': w3.eth.accounts[i]})
            refundable_crowdsale.instance.invest(price_per_token * token_value, tether.address, transact={'from': w3.eth.accounts[i]})
        
        time.sleep(6)

        # ????
        tether.instance.mint(w3.eth.accounts[4], 1, transact={'from': w3.eth.accounts[0]})

        refundable_crowdsale.instance.finalize(transact={'from': w3.eth.accounts[1]})

        for i in range(1,4):
            self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[i]), token_value)
            self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[i]), before - token_value * price_per_token)

            refundable_crowdsale.instance.refund(tether.address, transact={'from': w3.eth.accounts[i]})
            self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[i]), token_value)
            self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[i]), before)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

    def test_goal_reached(self):

        price_per_token = 1000
        token_value = 5
        goal = token_value * 3

        #Tokens
        base_token = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        tether = Contract("ERC20Mintable", w3, {"owner": w3.eth.accounts[0], "args": []})
        
        base_token.instance.mint(w3.eth.accounts[0], 100, transact={'from': w3.eth.accounts[0]})
        for i in range(1,4):
            tether.instance.mint(w3.eth.accounts[i], 100000, transact={'from': w3.eth.accounts[0]})
            before = tether.instance.balanceOf(w3.eth.accounts[i])
            
        #Crowdsale
        block = w3.eth.getBlock("latest")["timestamp"]
        refundable_crowdsale = Contract("RefundableCrowdsale", w3, {"owner": w3.eth.accounts[0], "args":[goal, block + 5, block + 7, base_token.address, w3.eth.accounts[0], [tether.address], [price_per_token]]})
        base_token.instance.transfer(refundable_crowdsale.address,100, transact={'from': w3.eth.accounts[0]})
        
        #AssertEqual
        for i in range(1,4):
            self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[i]), 0)
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

        #Invest
        time.sleep(6)
        
        for i in range(1,4):
            tether.instance.approve(refundable_crowdsale.address,price_per_token * token_value, transact={'from': w3.eth.accounts[i]})
            refundable_crowdsale.instance.invest(price_per_token * token_value, tether.address, transact={'from': w3.eth.accounts[i]})
        
        time.sleep(6)

        # ????
        tether.instance.mint(w3.eth.accounts[4], 1, transact={'from': w3.eth.accounts[0]})

        refundable_crowdsale.instance.finalize(transact={'from': w3.eth.accounts[1]})

        for i in range(1,4):
            with self.assertRaises(ValueError):
                refundable_crowdsale.instance.refund(tether.address, transact={'from': w3.eth.accounts[i]})

            self.assertEqual(base_token.instance.balanceOf(w3.eth.accounts[i]), token_value)
            self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[i]), before - token_value * price_per_token)
            self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), 0)

        refundable_crowdsale.instance.getFunds(tether.address, transact={'from': w3.eth.accounts[0]})
        self.assertEqual(tether.instance.balanceOf(w3.eth.accounts[0]), price_per_token*goal)
        
if __name__ == '__main__':
    unittest.main()
