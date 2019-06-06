import json
import web3
import os
import time
from web3 import HTTPProvider
from web3 import Web3
from web3.contract import ConciseContract

def url(address,port):
    return "http://{}:{}".format(address,port)

class W3:
    w3 = None

    def __init__(self):
        
        config = open('config.json','r')
        data = json.loads(config.read())
        config.close()                

        self.w3 = Web3(HTTPProvider(url(data['address'],data['port'])))

        for i in range(1, int(data['accounts_count']+1)):     
            if len(self.w3.eth.accounts) < data["accounts_count"] + 1:               
                self.w3.personal.newAccount('password')

        self.w3.personal.unlockAccount(self.w3.eth.accounts[0], '')

        for i in range(1, int(data['accounts_count'])+1):
            self.w3.personal.unlockAccount(self.w3.eth.accounts[i], 'password')         
                       
        for account in self.w3.eth.accounts:
            if account == self.w3.eth.accounts[0]:
                continue
            
            if self.w3.eth.getBalance(account) >= int(data['account_balance']):
                self.w3.eth.sendTransaction({'to': self.w3.eth.accounts[0], 'from': account, 'value': self.w3.eth.getBalance(account) - int(data['account_balance'])})
        
            if self.w3.eth.getBalance(account) < int(data['account_balance']):
                self.w3.eth.sendTransaction({'to': account, 'from': self.w3.eth.accounts[0], 'value': int(data['account_balance'] - self.w3.eth.getBalance(account))})

    def instance(self):
        return self.w3

class Contract:
    abi = None
    bin = None

    address = None
    instance = None
    w3 = None

    def __init__(self, contract_name, w3, deploy_info):
        self.set_w3(w3)
        self.load(contract_name)
        self.deploy(deploy_info["owner"], deploy_info["args"])


    def load(self, name):
        with open(os.path.join('../bin/', name + '.bin'), 'r') as f:
            self.bin = f.read()
            f.close()

        with open(os.path.join('../bin/', name + '.abi'), 'r') as f:
            self.abi = json.loads(f.read())
            f.close()


    def deploy(self, sender, _args):
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)
        tx_hash = contract.deploy(transaction={'from': sender}, args=_args)
        tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)   
  
        while(tx_receipt == None):
            tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)

        self.address = tx_receipt['contractAddress']
        self.instance = ConciseContract(self.w3.eth.contract(self.abi, self.address))

    def set_w3(self, w3):
        self.w3 = w3
