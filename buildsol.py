#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os, sys, traceback, json
from web3 import Web3, HTTPProvider
from solc import compile_source
import random

from py3mylib.mylog import *

def compile_contract(contract_source_file, contractName=None):
    """
    Reads file, compiles, returns contract name and interface
    """
    with open(contract_source_file, "r") as f:
        contract_source_code = f.read()
    compiled_sol = compile_source(contract_source_code) # Compiled source code
    if not contractName:
        contractName = list(compiled_sol.keys())[0]
        contract_interface = compiled_sol[contractName]
    else:
        contract_interface = compiled_sol['<stdin>:' + contractName]
    return contractName, contract_interface

def deploy_contract(acct, contract_interface, contract_args=None):
    """
    deploys contract using self-signed tx, waits for receipt, returns address
    """
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    constructed = contract.constructor() if not contract_args else contract.constructor(*contract_args)
    tx = constructed.buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
    })
    print ("Signing and sending raw tx ...")
    signed = acct.signTransaction(tx)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    print ("tx_hash = {} waiting for receipt ...".format(tx_hash.hex()))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
    contractAddress = tx_receipt["contractAddress"]
    print ("Receipt accepted. gasUsed={gasUsed} contractAddress={contractAddress}".format(**tx_receipt))
    return contractAddress

if __name__ == '__main__':
    compile_source("contract Foo { function Foo() {} }") # , output_values=["abi", "bin-runtime"]
    # cname, cinterface = compile_contract(os.path.join(os.path.dirname(__file__), "test.sol"))
    # print(cname)
    # print(cinterface)
