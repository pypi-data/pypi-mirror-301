import decimal
from typing import Optional, Tuple

import inquirer
from colorama import Fore

from tons.tonclient._client._base import AddressState
from tons.tonclient.utils import Record
from tons.tonsdk.contract.wallet import SendModeEnum, NetworkGlobalID
from tons.tonsdk.crypto._payload_encryption import encrypt_message
from tons.ui._utils import network_global_id_mismatch
from ..._modified_inquirer import ModifiedConfirm
from ._keystore_mixin import KeyStoreMixin
from ._wait_mixin import WaitForResultAndEchoMixin
from ..._task_params import TransferParams
from ..._utils import processing, echo_success, echo_error
from ..._validators import ignore_if_transfer_all, number_greater_than_or_equal_to_zero


class WalletMixin(KeyStoreMixin, WaitForResultAndEchoMixin):

    def _handle_transfer(self):
        self._handle_transfers_with_retry(is_simple=True)

    def _handle_advanced_transfer(self):
        self._handle_transfers_with_retry(is_simple=False)

    def _handle_transfers_with_retry(self, is_simple, transfer_params: Optional[TransferParams] = None):
        while True:
            result = self.__handle_transfer(is_simple=is_simple, transfer_params=transfer_params)
            if result is None:
                return

            exit_code, transfer_params = result
            if exit_code == 0:
                return

            else:
                is_sure = self._prompt([
                    ModifiedConfirm(
                        "is_sure", message="Transaction failed. Edit and retry?", default=False),
                ])["is_sure"]
                if not is_sure:
                    echo_success("Action canceled.")
                    return

    def __handle_transfer(self, is_simple, transfer_params: TransferParams = None) -> (
            Optional)[Tuple[int, TransferParams]]:
        if transfer_params is None:
            transfer_params = TransferParams()

        from_wallet = self.select_wallet("Transfer from", verbose=True, default=transfer_params.sender)
        if from_wallet is None:
            return

        record = self.ctx.keystore.get_record_by_name(
            from_wallet, raise_none=True)

        contact = self.select_contact("Send to", show_balance=True, default=transfer_params.recipient)
        if contact is None:
            return

        with processing():
            contact_info = self.ctx.ton_client.get_address_information(contact.address)

        if network_global_id_mismatch(record.network_global_id, self.ctx.config):
            network = 'mainnet' if record.network_global_id == NetworkGlobalID.main_net else 'testnet'

            is_sure = self._prompt([
                ModifiedConfirm(
                    "is_sure", message=f"{Fore.RED}{record.name} is intended for use in {network}. Send anyway?{Fore.RESET}", default=False),
            ])["is_sure"]
            if not is_sure:
                echo_success("Action canceled.")
                return

        if contact_info.state != AddressState.active:
            is_sure = self._prompt([
                ModifiedConfirm(
                    "is_sure", message="Sending to not active address. Send anyway?", default=False),
            ])["is_sure"]
            if not is_sure:
                echo_success("Action canceled.")
                return

        questions = [
            ModifiedConfirm("transfer_all", message='Transfer all remaining coins?',
                            default=transfer_params.transfer_all, ignore=is_simple),
            inquirer.Text("amount", message='Amount in TON coins to transfer',
                          ignore=ignore_if_transfer_all,
                          validate=number_greater_than_or_equal_to_zero,
                          default=transfer_params.amount),
            ModifiedConfirm(
                "destroy_if_zero", message='Destroy if balance becomes zero?',
                default=transfer_params.destroy_if_zero, ignore=is_simple, ),
            inquirer.Text(
                "message", message='Message (press \'Enter\' to skip)', default=transfer_params.message or contact.default_message),
            ModifiedConfirm("encrypt_payload", message='Encrypt payload?',
                            default=transfer_params.encrypt_payload, ignore=is_simple or (not contact_info.is_wallet)
            ),
            ModifiedConfirm(
                "wait_for_result", message="Wait until transaction will be completed?", default=True),
        ]
        ans = self._prompt(questions)
        transfer_all = ans["transfer_all"]
        amount = 0 if transfer_all else decimal.Decimal(ans["amount"])
        message = ans["message"]
        destroy_if_zero = ans["destroy_if_zero"]
        wait_for_result = ans["wait_for_result"]
        encrypt_payload = ans["encrypt_payload"]

        send_mode = SendModeEnum.ignore_errors | SendModeEnum.pay_gas_separately
        if destroy_if_zero:
            send_mode |= SendModeEnum.destroy_account_if_zero
        if transfer_all:
            send_mode |= SendModeEnum.carry_all_remaining_balance

        wallet, secret = self.get_wallet_from_record(record)

        transfer_params = TransferParams(
            sender=from_wallet,
            recipient=contact,
            transfer_all=transfer_all,
            amount=amount,
            message=message,
            destroy_if_zero=destroy_if_zero,
            encrypt_payload=encrypt_payload
        )

        with processing():
            if encrypt_payload:
                if not contact_info.is_wallet:
                    echo_error(f"Contact cannot receive encrypted messages")
                    return

                message = encrypt_message(message, secret.public_key, contact_info.public_key, secret.private_key,
                                          wallet.address)

            task_id = self.ctx.background_task_manager.transfer_task(from_wallet=wallet,
                                                                     to_addr=contact.address,
                                                                     amount=amount,
                                                                     payload=message,
                                                                     send_mode=send_mode,
                                                                     transfer_params=transfer_params
                                                                     )
        if not wait_for_result:
            echo_success('Task has been added to the queue.')
            return

        result = self._wait_for_result_and_echo(task_id)
        return result, transfer_params

    def _handle_init_wallet_with_retry(self, record: Record, wait_for_result: bool):
        while True:
            result = self._init_wallet(record, wait_for_result)
            if result is None:
                return

            exit_code = result
            if exit_code == 0:
                return

            else:
                is_sure = self._prompt([
                    ModifiedConfirm(
                        "is_sure", message="Transaction failed. Edit and retry?", default=False),
                ])["is_sure"]
                if not is_sure:
                    echo_success("Action canceled.")
                    return

    def _init_wallet(self, record: Record, wait_for_result: bool) -> Optional[int]:
        wallet, _ = self.get_wallet_from_record(record)
        with processing():
            task_id = self.ctx.background_task_manager.deploy_wallet_task(wallet)
        if not wait_for_result:
            echo_success("Transaction has been queued.")
            return
        return self._wait_for_result_and_echo(task_id)

    def _select_network_global_id(self) -> int:
        if self.ctx.config.provider.dapp.network == 'mainnet':
            default = 'Mainnet'
        else:
            default = 'Testnet'

        answer = self._prompt([
            inquirer.List(
                'network_global_id',
                message='Network global ID (affects address since v5r1)',
                choices=['Mainnet', 'Testnet'],
                default=default
            )
        ])

        result = {
            'Mainnet': int(NetworkGlobalID.main_net),
            'Testnet': int(NetworkGlobalID.test_net)
        }[answer['network_global_id']]

        return result