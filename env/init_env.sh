# Set SGX SDK environment variables
# e.g. source /opt/intel/sgxsdk/environment
source /PATH/TO/TOUR/environment

# Set the SDK source code path, which is required to compile the Runtime
# e.g. export ENV_SGX_SDK_CODE_PATH=/home/Alice/linux-sgx-sgx_2.1
export ENV_SGX_SDK_CODE_PATH=/PATH/TO/TOUR/SGX-SDK-SOURCE-CODE

# Set the control val used for Runtime
sudo sysctl vm.mmap_min_addr=0

# Enable the fsgsbase bit in CR4
cd ./kmodule/enablefsgs
make clean; make
sudo insmod enablefsgs.ko

cd ../../kmodule/cr
make clean; make
sudo insmod cr.ko

cd ../../
cat /proc/enablefsgs
cat /proc/cr
