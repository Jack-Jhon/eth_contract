- 复制Crypto Application Token.sol 代码到 http://remix.ethereum.org/ 编译，得到字节码。

- 根据实际情况，配置 contract.json。

- 在线环境执行 python develop_contract.py -c 生成创建合约交易，复制生成的文件 transaction.json 到离线签名环境。

- 在线环境执行 python develop_contract.py -p 合约地址 生成暂停合约交易，复制生成的文件 transaction.json 到离线签名环境。

- 在线环境执行 python develop_contract.py -u 合约地址 生成恢复合约交易，复制生成的文件 transaction.json 到离线签名环境。

- 离线环境执行 python develop_contract.py -s 签名交易，复制生成的文件 transaction.json 到在线环境广播。

- 在线环境执行 python develop_contract.py -b 广播交易


=====================================================================================
- python 合约分析器 https://kauri.io/analyze-solidity-smart-contracts-with-slither/4f4dcf7d105d4714b212a86da742baf6/a
- python 编译发布 https://yohanes.gultom.id/2018/11/28/compiling-deploying-and-calling-ethereum-smartcontract-using-python/
- 本地路径 F:\doc2020\eth\合约
- erc合约库 https://openzeppelin.com/



-------------
获取余额：https://api-rinkeby.etherscan.io/api?module=account&action=balance&address=0xD9d73f325BdF1af2C76437b95CE72574D56E3232&tag=latest&apikey=GD9QKFXITCACKIMMU5QKK54A53YYYAXE4Z

-------------
MainNet: chain-id 1, network-id 1
Rinkeby: chain-id 4, network-id 4
Ropsten: chain-id 3, network-id 3
Dev: chain-id 2018, network-id 2018



------------------------------------------------------------------
安装pyweb3错误
ERROR: After October 2020 you may experience errors when installing or updating packages. This is because pip will change the way that it resolves dependency conflicts.

We recommend you use --use-feature=2020-resolver to test your packages with the new resolver before it becomes the default.

pythonmiddleware 1.0.0 requires ecdsa==0.13.3, but you'll have ecdsa 0.15 which is incompatible.
pythonmiddleware 1.0.0 requires requests==2.20.0, but you'll have requests 2.22.0 which is incompatible.
pythonmiddleware 1.0.0 requires websockets==6.0, but you'll have websockets 8.1 which is incompatible.