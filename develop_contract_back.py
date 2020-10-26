#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import sys
import json
import subprocess

from py3mylib.base import *

def CmdCall(cmd, isJson=True):
    try:
        print("cmdCall==> request: {} ".format(cmd))
        respone = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8')
        print("cmdCall==> respone: {}".format(respone))
        if isJson:
            respone = json.loads(respone)
        return respone
    except Exception as err:
        print(err)
        return False

def GetNonce(rpchost, address):
    print("获取nonce值 [address={}][rpchost={}]".format(address, rpchost))
    getnonce = """curl --data '{"method":"eth_getTransactionCount","params":["{{address}}","latest"],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST {{rpchost}}"""
    getnonce = getnonce.replace("{{address}}", address).replace("{{rpchost}}", rpchost)
    respone = CmdCall(getnonce)
    if respone:
        return respone["result"]

def GetChainid(rpchost):
    print("获取chainid [rpchost={}]".format(rpchost))
    getchainid = """curl --data '{"method":"eth_chainId","params":[],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST {{rpchost}}"""
    getchainid = getchainid.replace("{{rpchost}}", rpchost)
    respone = CmdCall(getchainid)
    if respone:
        return respone["result"]

def UnlockAccount(rpchost, address, password, unlocktime):
    print("解锁账户 [rpchost={}][address={}][password={}][unlocktime={}]".format(rpchost, address, password, unlocktime))
    unlock = """curl --data '{"method":"personal_unlockAccount","params":["{{address}}","{{password}}",{{unlocktime}}],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST {{rpchost}}"""
    unlock = unlock.replace("{{address}}", address).replace("{{password}}", password).replace(
        "{{unlocktime}}", unlocktime).replace("{{rpchost}}", rpchost)
    CmdCall(unlock)

def SignTranscation(rpchost, tran):
    """

    :param rpchost:
    :param tran: json
    :return:
    """
    print("签名交易 [rpchost={}][tran={}]".format(rpchost, tran))
    signtran = """curl --data '{"method":"eth_signTransaction","params":[{{tran}}],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST {{rpchost}}"""
    signtran = signtran.replace("{{tran}}", tran).replace("{{rpchost}}", rpchost)
    respone = CmdCall(signtran)
    if respone:
        return respone["result"]["raw"]

def BroadcastTransaction(rpchost, raw):
    print("广播交易 [raw={}][rpchost={}]".format(raw, rpchost))
    sendrawtran = """curl --data '{"method":"eth_sendRawTransaction","params":["{{raw}}"],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST {{rpchost}}"""
    sendrawtran = sendrawtran.replace("{{raw}}", raw).replace("{{rpchost}}", rpchost)
    CmdCall(sendrawtran)

def GenerateContractTransaction(rpchost, contractaddress=None, **kwargs):
    print("生成合约交易并写入transaction.json文件 [rpchost={}][kwargs={}]".format(rpchost, kwargs))
    nonce = GetNonce(rpchost, kwargs["from"])
    chainid = GetChainid(rpchost)
    if not nonce or not chainid:
        print("Get nonce or chain id failed...")
        sys.exit(1)
    contract_tran = {
        "from": kwargs["from"],
        "gas": kwargs["gas"],
        "gasPrice": kwargs["gasPrice"],
        "value": "0x0",
        "nonce": nonce,
        "data": kwargs["data"],
        "chainId": chainid
    }
    if contractaddress:
        contract_tran["to"] = contractaddress
    jsontran = {
        "transaction": contract_tran
    }
    tranfile = open("./transaction.json", "w")
    json.dump(jsontran, tranfile)
    tranfile.close()
    return True


##########
def sign_develop_contract_tx(data, key):
    pass


if __name__ == '__main__':
    f = open("./contract.json", "r")
    paras = json.load(f)

    if len(sys.argv)<2:
        print("use -c <createtransaction> -s <sign> -b <broadcast>")
        sys.exit(1)

    if sys.argv[1]=="-c":
        print("生成创建合约交易...")
        tran = {
            "from": paras["from"],
            "gas": paras["gas"],
            "gasPrice": paras["gasPrice"],
            "value": "0x0",
            "data": paras["bytecode"]
        }
        ret = GenerateContractTransaction(paras["online_rpc"], **tran)
        print(ret)

    elif sys.argv[1]=="-s":
        print("交易签名...")
        # 解锁账户
        UnlockAccount(paras["offline_rpc"], paras["from"], paras["password"], paras["unlocktime"])

        # 签名
        tranfile = open("./transaction.json", "r")
        jsontran = json.load(tranfile)
        jsontran["raw"] = SignTranscation(paras["offline_rpc"], json.dumps(jsontran["transaction"]))
        tranfile.close()
        tranfile = open("./transaction_signed.json", "w")
        json.dump(jsontran, tranfile)
        tranfile.close()

    elif sys.argv[1]=="-b":
        print("广播交易...")
        tranfile = open("./transaction.json", "r")
        jsontran = json.load(tranfile)
        BroadcastTransaction(paras["online_rpc"], jsontran["raw"])

    elif sys.argv[1]=="-p" and len(sys.argv)>2:
        print("生成暂停合约交易...")
        contractaddress = sys.argv[2]
        tran = {
            "from": paras["from"],
            "gas": paras["gas"],
            "gasPrice": paras["gasPrice"],
            "value": "0x0",
            "data": paras["pause"]
        }
        ret = GenerateContractTransaction(paras["online_rpc"], contractaddress, **tran)
        print(ret)

    elif sys.argv[1]=="-u" and len(sys.argv)>2:
        print("生成恢复合约交易...")
        contractaddress = sys.argv[2]
        tran = {
            "from": paras["from"],
            "gas": paras["gas"],
            "gasPrice": paras["gasPrice"],
            "value": "0x0",
            "data": paras["unpause"]
        }
        ret = GenerateContractTransaction(paras["online_rpc"], contractaddress, **tran)
        print(ret)

    f.close()
    print("Done...")




