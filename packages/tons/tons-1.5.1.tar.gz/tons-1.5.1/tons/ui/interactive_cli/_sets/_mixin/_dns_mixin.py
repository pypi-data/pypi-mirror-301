from typing import Sequence, Set, List, Iterator, Dict, Tuple
from uuid import UUID

from tons.tonclient._client._base import NftItemInfoResult
from tons.tonsdk.utils import Address, InvalidAddressError
from ...._utils import shorten_dns_domain, batches
from ..._utils import echo_success, echo_error, processing
from ..._background import DNSRefreshBackgroundTask
from ._misc import keystore_sensitive_area
from ._keystore_mixin import KeyStoreMixin


class DnsMixin(KeyStoreMixin):
    @keystore_sensitive_area
    def __refresh_ownership(self, dns_items: Sequence[NftItemInfoResult], wait_for_result: bool):
        pending_tasks: Set[UUID] = set()

        dns_address_map = self.__get_dns_address_map(dns_items)

        for raw_address, address_dns_items in dns_address_map.items():
            record = self.ctx.keystore.get_record_by_address(Address(raw_address))
            with processing():
                wallet, _ = self.ctx.keystore.get_wallet_from_record(record)
                for dns_item_batch in self.__dns_batches(address_dns_items, wallet.max_internal_messages()):
                    task_id = self.ctx.background_task_manager.dns_refresh_task(from_wallet=wallet,
                                                                                dns_items=dns_item_batch)
                    pending_tasks.add(task_id)

        if not wait_for_result:
            echo_success("Transactions have been queued.")
            return

        while len(pending_tasks) > 0:
            with processing():
                task_id, task = self.__get_next_finished_task(pending_tasks)
            _echo = echo_success if not task.result_is_bad else lambda msg: echo_error(msg, only_cross=True)

            for idx, dns_item in enumerate(task.dns_items):
                if isinstance(task.result_description, str):
                    result_description = task.result_description
                else:
                    result_description = task.result_description[idx]

                _echo(f"{shorten_dns_domain(dns_item.dns_domain)}.ton: {result_description}. "
                      f"Wallet address: {dns_item.owner_or_max_bidder}")

            pending_tasks.remove(task_id)

    def _refresh_ownership(self, dns_items: Sequence[NftItemInfoResult], wait_for_result: bool):
        if len(dns_items) == 0:
            echo_success('No domain needs to update ownership.')
            return
        self.__refresh_ownership(dns_items, wait_for_result)

    @classmethod
    def __dns_batches(cls, dns_items: List[NftItemInfoResult], batch_size: int) -> Iterator[List[NftItemInfoResult]]:
        yield from batches(dns_items, batch_size)

    def __get_dns_address_map(self, dns_items: Sequence[NftItemInfoResult]) -> Dict[str, List[NftItemInfoResult]]:
        dns_address_map: Dict[str, List[NftItemInfoResult]] = dict()
        for dns_item in dns_items:
            try:
                raw_address = Address.raw_id(dns_item.owner_or_max_bidder)
            except InvalidAddressError:
                echo_error(f"{shorten_dns_domain(dns_item.dns_domain)}.ton: Invalid NFT data.")
                continue
            try:
                dns_address_map[raw_address].append(dns_item)
            except KeyError:
                dns_address_map[raw_address] = [dns_item]
        return dns_address_map

    def __get_next_finished_task(self, pending_tasks: Set[UUID]) -> \
            Tuple[UUID, DNSRefreshBackgroundTask]:
        while True:
            for task_id in pending_tasks:
                if not (task := self.ctx.background_task_manager.get_task(task_id)).is_pending:
                    assert isinstance(task, DNSRefreshBackgroundTask)
                    return task_id, task
