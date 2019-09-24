# Tora Tutorial

## For master TEE

* `cd /home/Python-KMS`
* Run the master TEE
  * `~/Zilliqa/build/matroska /usr/local/bin/python3 -B server.py main --host 0.0.0.0 --port 1234` 
  * Explanation
    * -B option is for loading the files without pyc files. If pyc files already generated, can delete the pyc files by`find . -name "*.pyc" -exec rm -f {} \;`
    * When the new machine run the master TEE for the first time, master_tee_address will be generated and print on the console

* Tora contract deployment

  * Modify contracts/Tora.scilla，set the according master_tee_address

    ```
    let master_tee_address = 0x...
    ```

  * Deploy the Tora contract, the example code is in tests/deploy_contract_test.py
  * Publish the Tora contract address

## For Oracle Node

* `cd /home/Tora-Zilliqa`

* config.ini

  ```
  [auth]
     master-host = ""
     account = "zil10h9339zp277h8gmdhds6zuq0elgpsf5qga4qvh"

  [BaseChain]
     [[zilliqa]]
        rpc-server = "https://dev-api.zilliqa.com/"
        network-id = "333"
        version = "21823489"
        contract-address = "zil165m736j7ht0x6chwsg096rdnrfhu9r8a7r7e4r"

  [KMS]
     host = 192.168.1.19
     port = 1234

  [debug]
     level = DEBUG
     log-file = stdout
  ```

  Parameter Explanation

  * account = oracle node account address
  * contract-address = Tora contract address
  * host, port = The host and port of the kms server
  * level, log-file = Log option

* Launch the oracle node

  `~/Zilliqa/build/matroska /usr/local/bin/python3 -B tora.py launch —config config.ini`

* Withdraw reward

  `~/Zilliqa/build/matroska /usr/local/bin/python3 -B tora.py withdraw —config config.ini --sk ( ) —address ( zil… )`

  It needs about a few minutes to process the withdraw on chain

## For User

* First, you can download the **Tora-Zilliqa** project to your machine from <https://github.com/TEEXIO/Tora-Zilliqa>, and for user, you don't need the Intel SGX environment but you need **python3.6** to execute the python script.

* Second, you need ```cd {YOURPATH}/Tora-Zilliqa/backend/lib/pyzil``` . Then `pip3 install -r requirements.txt` and `python3 setup.py install` . If there are some errors, please check if you have installed **gmp**. 

  You can install **gmp** with`brew install gmp`and`export LDFLAGS="-L/usr/local/opt/openssl/lib -L /usr/local/opt/gmp/lib" && export CPPFLAGS="-I/usr/local/opt/openssl/include -I/usr/local/opt/gmp/include"`

* Write the user contract，the example contract is in **contracts/Request.scilla** and **contracts/GeneralRequest.scilla**

  *  Request.scilla is for the trial to fetch data on the top 100 trading pairs from the top 10 exchanges. GeneralRequest.scilla is for the general request to  fetch data from a general web api.

  * Parameter Explanation

    * Tora contract address ```let oracle_address = 0x...```

      Tip: You can transfer the oracle address in zil… format to hex format with this function

      ```
      oracle_address = '0x' + zilkey.to_valid_address("zil...")
      ```

    * set the gas price and gas limit of the response

      ```
      let gas_price_set = Uint128 1000000000
      let gas_limit_set = Uint128 10000
      ```

* Deploy the user contract with your account sk and find the contract address on Zilliqa Explorer, the example code is in tests/deploy_contract_test.py

* Invoke the user contract, the example code is in tests/request_test.py

  ```
  # user account
  account = Account(private_key="Your account sk")
  # request contract address
  contract_addr = "User contract address(Zil...)"
  contract = Contract.load_from_address(contract_addr)
  contract.account = account
  # invoke the contract
  resp = contract.call(method="request", params=[], amount=15)
  ```

  The amount include four parts of fee：

  * The reward for oracle node(>=1ZIL)
  * The gas fee for response(gas_price_set*gas_limit_set)
  * The gas fee for refunding remain response gas fee(0.001ZIL)
  * The gas fee for oracle node withdraw(about 1ZIL)

  If amount< the least fee, an event 'No enough money' will return

