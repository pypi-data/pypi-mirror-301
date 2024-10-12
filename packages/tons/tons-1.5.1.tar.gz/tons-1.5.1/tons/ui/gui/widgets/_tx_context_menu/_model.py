from typing import Optional

from PyQt6.QtCore import pyqtSignal
from pydantic import BaseModel

from tons.ui.gui.widgets import TransactionListItemData


class TransactionContextMenuModel(BaseModel):
    cancel_enabled: bool
    edit_and_retry_enabled: bool
    check_in_scanner_enabled: bool

    item_data: TransactionListItemData

    @classmethod
    def from_transaction_list_item_data(cls, item_data: TransactionListItemData):
        return cls(
            cancel_enabled=item_data.cancellable,
            edit_and_retry_enabled=bool(item_data.edit_and_retry_info),
            check_in_scanner_enabled=bool(item_data.tx_hash),
            item_data=item_data
        )
