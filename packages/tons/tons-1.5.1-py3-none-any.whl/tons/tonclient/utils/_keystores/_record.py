from typing import Union, Optional

from pydantic import BaseModel, validator, root_validator

from tons.tonsdk.contract.wallet import WalletVersionEnum, NetworkGlobalID
from tons.tonsdk.utils import Address, InvalidAddressError


class Record(BaseModel):
    name: str
    address: Union[str, Address]
    version: WalletVersionEnum
    workchain: int
    subwallet_id: Optional[int]
    network_global_id: Optional[int]
    secret_key: str
    comment: Optional[str] = ""

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True

    @validator('comment')
    def validate_comment(cls, v, values, **kwargs) -> str:
        if v is None:
            return ''
        return v

    @validator('address')
    def validate_address(cls, v, values, **kwargs) -> str:
        if isinstance(v, Address):
            return v.to_string(False, False, False)

        try:
            addr = Address(v)
            return addr.to_string(False, False, False)

        except InvalidAddressError as e:
            raise ValueError(e)

    def _is_testnet_only(self) -> bool:
        return self.version == WalletVersionEnum.v5r1 and self.network_global_id == NetworkGlobalID.test_net


    @property
    def address_to_show(self) -> str:
        return Address(self.address).to_string(True, True, True, self._is_testnet_only())

    @property
    def tep_standard_user_address(self) -> str:
        addr = Address(self.address)
        addr.is_test_only = self._is_testnet_only()
        return addr.tep_standard_user_address

