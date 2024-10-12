import dataclasses
import decimal
from typing import Optional

from tons.tonclient.utils import WhitelistContact


@dataclasses.dataclass
class TransferParams:
    sender: str = ""
    recipient: Optional[WhitelistContact] = None

    transfer_all: bool = False
    amount: Optional[decimal.Decimal] = None
    message: str = ""
    destroy_if_zero: bool = False
    encrypt_payload: bool = False

    def is_advanced(self) -> bool:
        return self.transfer_all or self.destroy_if_zero or self.encrypt_payload
