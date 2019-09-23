# Tora Install

## Prerequisites

* Hardware Requirement:
  * 6th Generation Intel(R) Core(TM) Processor or newer
  * Configure the system with the SGX hardware enabled option
* Operating System Requirement:
  * Ubuntu 16.04
* Software Requirement:
  * [Intel SGX Driver v1.9](https://github.com/intel/linux-sgx-driver/tree/sgx_driver_1.9)
  * [Intel SGX SDK v2.1](https://github.com/intel/linux-sgx/tree/sgx_2.1)
  * [Docker](https://www.docker.com/)


## Installation

The following steps describe the installation for Tora.

Before the installation. Make sure you have installed intel-sgx driver and  /dev/isgx should appear.


<!-- Make sure again that you have installed intel-sgx driver, sdk and psw. To verify that you were successful, build the sample code in HW mode and run it.

```
  $ cd /PATH/TO/sgx-sdk-sourcecode/SampleCode/LocalAttestation
  $ make
  $ ./app
``` -->


###  Environment Initialization

Then switch to Tora source code directory and go to the env folder, enter the following command:

```
  $ ./init_env.sh  
```
### Pull Docker Image

First, pull the image.

```
  $ docker pull teexio/tora-zilliqa
```

Second, start a docker with sgx device support

```
  $  sudo docker run --device /dev/isgx -it teexio/tora-zilliqa /bin/bash
```

Third, run the init script inside the docker

```
  $ cd /root
  $ ./init.sh
```

Finally, check if the sample code work

```
  $ cd ~/linux-sgx/linux/SampleCode/LocalAttestation
  $ make 
  $ ./app
```
