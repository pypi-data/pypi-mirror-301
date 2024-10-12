from collections import OrderedDict
import typing as t

from colorama import Fore

from tons.tonclient._client._base import NftItemInfoResult
from tons.tonsdk.utils import Address
from tons.ui._utils import SharedObject, md_table, truncate, shorten_dns_domain
from ._base import BaseSet, MenuItem
from ._mixin import DnsMixin, WalletMixin
from ._utils import add_menu_item
from .._background import BackgroundTask, TransferBackgroundTask, DNSRefreshBackgroundTask, DeployWalletBackgroundTask
from .._modified_inquirer import ListWithFilter, ModifiedConfirm
from .._task_params import TransferParams
from .._utils import echo_success


class OngoingSet(BaseSet, WalletMixin, DnsMixin):
    def __init__(self, ctx: SharedObject):
        super().__init__(ctx)
        self._menu_message = f"Pick command [{self.ctx.keystore.name}]"

    def _handlers(self) -> t.OrderedDict[str, MenuItem]:
        ord_dict = OrderedDict()
        add_menu_item(ord_dict, "View", "v", self._handle_view_pending)
        add_menu_item(ord_dict, "Edit and retry", "e", self._handle_edit_and_retry_pending)
        add_menu_item(ord_dict, "Back", 'b', self._handle_exit)

        return ord_dict

    def _handle_view_pending(self):
        table = md_table()
        table.field_names = ["Task", "Initiated", "Finished", "Status"]
        table.align["Task"] = 'l'
        for background_task in self.ctx.background_task_manager.tasks_list(unsafe=True):
            rows = self.__get_task_rows(background_task)

            for row in rows:
                table.add_row(row)
        echo_success(str(table), only_msg=True)

    @classmethod
    def __get_task_rows(cls, background_task: BackgroundTask) -> t.List[t.List[str]]:
        rows = []
        for result_description, description in zip(background_task.result_descriptions,
                                                   background_task.descriptions):
            row = cls.__get_subtask_row(background_task, description, result_description)
            rows.append(row)
        return rows

    @classmethod
    def __get_subtask_row(cls, background_task: BackgroundTask, description: str, result_description: str) -> t.List[str]:
        result_description = truncate(result_description, max_len=100)
        result_description += Fore.RESET
        row = [description,
               background_task.time_start.strftime("%H:%M:%S"),
               'in progress' if background_task.time_finish is None
               else background_task.time_finish.strftime("%H:%M:%S"),
               result_description]
        return row

    def _handle_edit_and_retry_pending(self):
        tasks_list = self.ctx.background_task_manager.tasks_list(unsafe=True)
        if len(tasks_list) == 0:
            echo_success("No ongoing tasks")
            return

        choices = []
        values = []

        for task in tasks_list:
            if isinstance(task, TransferBackgroundTask):
                choice = []
                for desc, res in zip(task.descriptions, task.result_descriptions):
                    choice.append(f'{desc} [{res or "..."}]')
                choice = ', '.join(choice)

                value = 'transfer', task.transfer_params

                choices.append(choice)
                values.append(value)

            elif isinstance(task, DNSRefreshBackgroundTask):
                for dns, res in zip(task.dns_items, task.result_descriptions):
                    choice = f'Refresh {shorten_dns_domain(dns.dns_domain)}.ton [{res or "..."}]'
                    value = 'refresh_dns', dns

                    choices.append(choice)
                    values.append(value)

            elif isinstance(task, DeployWalletBackgroundTask):
                choice = task.description
                value = 'init_wallet', task.wallet_addr

                choices.append(choice)
                values.append(value)

            # TODO other background tasks

        choices.append('(Cancel)')
        values.append(('back', None))

        task_kind, task_params = self._prompt([
            ListWithFilter(
                'task_to_retry',
                message='Select task',
                choices=ListWithFilter.zip_choices_and_values(choices, values)
            )
        ])['task_to_retry']

        if task_kind == 'back':
            return

        if task_kind == 'transfer':
            assert isinstance(task_params, TransferParams)
            self._handle_transfers_with_retry(not task_params.is_advanced(), task_params)

        elif task_kind == 'refresh_dns':
            assert isinstance(task_params, NftItemInfoResult)
            wait = self._prompt([ModifiedConfirm(
                "wait", message="Wait until transaction will be completed?", default=True)])['wait']

            self._refresh_ownership([task_params], wait)

        elif task_kind == 'init_wallet':
            assert isinstance(task_params, Address)

            record = self.ctx.keystore.get_record_by_address(task_params, raise_none=True)

            wait = self._prompt([ModifiedConfirm(
                "wait", message="Wait until transaction will be completed?", default=True)])['wait']

            self._handle_init_wallet_with_retry(record, wait)

        # TODO other background tasks



