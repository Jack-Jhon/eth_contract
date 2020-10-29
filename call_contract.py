#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os, sys, traceback, json
from web3.auto import w3

if __name__ == '__main__':
    abifile = open(os.path.join(os.path.dirname(__file__), "sol/build/abi.json"), "r")
    abi = json.load(abifile)
    abifile.close()
    key = "0x620b0c04de671567431e962c6d0eadc28b9f25d672d0a036044c5a259c27ad9b"
    contract_address = w3.toChecksumAddress("0x70988a12797aff8c063a72bebcaf897175c590c3")
    erc721 = w3.eth.contract(address=contract_address, abi=abi)

    # tx = erc721.functions.mintTo("0x005Ea2533D25B74BE9F774c79Fa4E0D219912B41").buildTransaction()
    # print(tx)

    ##########################################
    transaction = {
        "from": "0xD9d73f325BdF1af2C76437b95CE72574D56E3232",
        "to": "0x70988a12797AFf8c063a72BebCaf897175C590C3",
        "value": 0,
        "gas": 200000,
        "gasPrice": 10 ** 9,
        "nonce": 6,
        "chainId": 4,
        "data": "0x755edd17000000000000000000000000005ea2533d25b74be9f774c79fa4e0d219912b41"
    }
    signed = w3.eth.account.sign_transaction(transaction, key)
    print(signed.rawTransaction.hex())
    print(signed.hash.hex())
