#### 3. Python Executor

##### Step 0: Commit your script

* You can commit your scripts by invoking the **deployScript** transition in the **ToraGeneral** contract. The example code is in **backend/tests/executor_deploy_test.py**

  * The example script is as the following:

    * **inp** is a reserved word, which is an array composed of the inputs of your script in order.
    * **outp** is another reserved word, which represents the result you want.
    * In the example case, the inputs are **two integers**, the result of the script is the sum of the two integers which are respectively added 1. 

    ```
    x = inp[0] + 1
    y = inp[1] + 1
    
    outp = x + y
    ```

  After committing your script successfully, the **scriptId** will be returned to you:

  ```
  $ python3 executor_deploy_test.py
  Terminal:
  ----------
  Script committed successfully, the script id is 1
  ```

#####Step 1: Invoke your script

* Write the user contract，the example contract is in **contracts/ExecutorRequest.scilla** which invoking the **executeScript** transition defined in the **ToraGeneral** contract.

    ```
    transition request()
        accept;
        msg = { _tag : "executeScript"; _recipient : oracle_address; _amount : _amount;
        ...(other params); scriptId: Uint32 1; inputs: "[1, 2]" };
        msgs = one_msg msg;
        send msgs
    end
    ```

* ExecutorRequest.scilla is for the trial to get the result of the above script defined in **Step 0** with the**inputs** 1 and 2. 

* In addition to the **inputs** required to be designated, you should designate the **scriptId** returned in **Step 0**.

* After deploying your user contract, you can invoke it by the example code in **backend/tests/executor_request_test.py**.

    You can achieve the result as the following:

    ```
    $ python3 executor_request_test.py
    Terminal:
    ----------
    {'_eventname': 'callback', 'address': '0x0dcca194fa156e388f01b3c4b9993d031d596699', 'params': [{'type': 'String', 'value': '5', 'vname': 'msg'}]}
    ```

    

    