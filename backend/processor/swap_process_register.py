import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))


from pyzil.account import Account
from pyzil.contract import Contract

DEFAULT_REGISTER_STAKE = 2


class SwapProcessRegister:
    def __init__(self, contract_addr):
        self.contract_addr = contract_addr

    def register_to_process(self, sk, request_id):
        pass


class ZilliqaSwapProcessRegister(SwapProcessRegister):
    def register_to_process(self, sk, request_id):
        account = Account(private_key=sk)
        contract = Contract.load_from_address(self.contract_addr)
        contract.account = account
        resp = contract.call(method="register_to_process", params=[
            Contract.value_dict("verify_request_id", "Uint32", request_id)
        ], amount=DEFAULT_REGISTER_STAKE)
        if not resp:
            return False
        if resp['receipt']['success']:
            if "event_logs" in resp['receipt']:
                event_logs = resp['receipt']["event_logs"]
                for event_log in event_logs:
                    if event_log['_eventname'] == 'register success':
                        return True
        return False
