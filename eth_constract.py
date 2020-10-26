#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import time

from web3 import Web3
from solc import compile_standard
from binascii import b2a_hex, a2b_hex
import rlp

def getTokenAmount(contract, address, tokenname):
    print(contract.functions.balanceOf(address).buildTransaction())
    amount = int(contract.functions.balanceOf(address).call())
    #amount = Web3.fromWei(amount, "ether")
    print("{}:{} {}".format(address, amount, tokenname))
    return amount

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf8')
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider("http://10.10.12.100:6789"))
    f = open("./contract.json", "r")
    contract = json.load(f)
    bytecode = contract["bytecode"]
    abi = contract["abi"]
    contract_address = Web3.toChecksumAddress("0x19573b68fb5c72117cdfb7f503f4d301ce41653d")

    #合约调用
    #获取token余额
    puberc20 = w3.eth.contract(address=contract_address, abi=abi)
    tokenname = puberc20.functions.symbol().call()
    decimals = puberc20.functions.decimals().buildTransaction()
    print(decimals, tokenname)
    # import sys
    # sys.exit()
    send = Web3.toChecksumAddress("0xe6c7f6d0e8b395da542f06e38c9831cd3cf72eb0")
    recp = Web3.toChecksumAddress("0x1057c320622d0c9b2aad2b7ff1445101ffe02228")
    getTokenAmount(puberc20, send, tokenname)

    #解锁账户
    w3.eth.defaultAccount = send
    result = w3.geth.personal.unlockAccount(send, "1111111", 24*3600)
    print("解锁账户结果：{}".format(result))

    # 暂停合约
    # print("暂停合约...")
    # tx = puberc20.functions.pause().buildTransaction()
    # print(tx)
    # tx_hash = puberc20.functions.pause().transact()
    # print("txhash：{}".format(tx_hash.hex()))
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print("暂停合约调用成功，已上链...")

    #恢复合约
    # print("恢复合约...")
    # # tx = puberc20.functions.unpause().buildTransaction()
    # # print(tx)
    # tx_hash = puberc20.functions.unpause().transact()
    # print("txhash：{}".format(tx_hash.hex()))
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print("恢复合约调用成功，已上链...")

    # 发送token
    sendamount = 100000
    print("发送 {} {} 到 {}...".format(sendamount, tokenname, recp))
    getTokenAmount(puberc20, recp, tokenname)
    value = Web3.toWei(sendamount, "ether")
    print(puberc20.functions.transfer(recp, value).buildTransaction())
    tx_hash = puberc20.functions.transfer(recp, value).transact()
    print("转账 txhash:{}".format(tx_hash.hex()))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("转账交易已上链...")

    getTokenAmount(puberc20, recp, tokenname)
    getTokenAmount(puberc20, w3.eth.defaultAccount, tokenname)


# #
# if __name__ == '__main__':
#     w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:6789"))
#
#     #设置发送账户 && 解锁账户
#     w3.eth.defaultAccount = w3.eth.accounts[0]
#     w3.eth.defaultAccount = Web3.toChecksumAddress("0xe6c7f6d0e8b395da542f06e38c9831cd3cf72eb0")
#
#     print("设置发布账户：{}".format(w3.eth.defaultAccount))
#     result = w3.geth.personal.unlockAccount(w3.eth.defaultAccount, "1111111", 24*3600)
#     print("解锁账户结果：{}".format(result))
#
#     #合约发布
#     f = open("./contract.json", "r")
#     contract = json.load(f)
#     bytecode = contract["bytecode"]
#     abi = contract["abi"]
#     #contract_address = Web3.toChecksumAddress(contract["contract_address"])
#
#     #在线发布
#     erc20 = w3.eth.contract(abi=abi, bytecode=bytecode)
#     # tx_hash = erc20.constructor().transact()
#     # print("合约已发布 txhash:{}".format(tx_hash.hex()))
#
#     #离线签名后发布
#     buildtran = erc20.constructor().buildTransaction()
#     jsontran =  json.dumps(buildtran, cls=DateEncoder)
#     jsontran = json.loads(jsontran)
#     jsontran.pop("to")
#     nonce = w3.eth.getTransactionCount(account=jsontran["from"])
#     print(nonce)
#     jsontran["nonce"] = nonce
#     print(json.dumps(jsontran))
#     raw = w3.eth.signTransaction(jsontran).raw.hex()
#     print(raw)
#     txhash = w3.eth.sendRawTransaction(raw)
#     print(txhash.hex())
#
#     #Wait for the transaction to be mined, and get the transaction receipt
#     print("等待交易上链...")
#     tx_receipt = w3.eth.waitForTransactionReceipt(txhash)
#     print("合约发布成功 合约地址：{}".format(tx_receipt.contractAddress))
#     contract_address = tx_receipt.contractAddress
#
#     #合约调用
#     #获取token余额
#     puberc20 = w3.eth.contract(address=contract_address, abi=abi)
#     tokenname = puberc20.functions.symbol().call()
#
#     getTokenAmount(puberc20, w3.eth.defaultAccount, tokenname)
#
#     #发送token
#     toAddress = Web3.toChecksumAddress("0xe6c7f6d0e8b395da542f06e38c9831cd3cf72eb0")
#     sendamount = 987
#     print("发送 {} {} 到 {}...".format(sendamount, tokenname, toAddress))
#     getTokenAmount(puberc20, toAddress, tokenname)
#     value = Web3.toWei(sendamount, "ether")
#     tx_hash = puberc20.functions.transfer(toAddress, value).transact()
#     print("转账 txhash:{}".format(tx_hash.hex()))
#     tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     print("转账交易已上链...")
#
#     getTokenAmount(puberc20, toAddress, tokenname)
#     getTokenAmount(puberc20, w3.eth.defaultAccount, tokenname)
