import dataclasses
import time
import typing as t
from enum import IntEnum
from typing import List, Optional

from .. import InternalMessage
from .._wallet_contract import WalletContract
from ... import Contract
from ....boc import Cell, begin_cell, begin_dict, Slice, Builder

from ._constants import _WALLET_V5R1_CODE, _BitSize, _PUBLIC_KEY_SIZE, _Op, _WALLET_V5R1_CODE_HASH
from ....boc.dict.deserialize_dict import parse_dict
from ....utils import sign_message


@dataclasses.dataclass
class WalletV5Data:
    public_key: bytes
    signature_allowed: bool
    seqno: int
    wallet_id: int
    extensions: t.Dict[int, int]  # [BigUint(256), BigInt(1)]

    def __post_init__(self):
        if len(self.public_key) != _PUBLIC_KEY_SIZE:
            raise ValueError(f"Public key length should be {_PUBLIC_KEY_SIZE}")


    @classmethod
    def from_cell(cls, data: Cell):
        s = data.begin_parse()
        signature_allowed = s.read_bit()
        seqno = s.read_uint(_BitSize.SEQNO)
        wallet_id = s.read_uint(_BitSize.WALLET_ID)
        public_key = s.read_bytes(_PUBLIC_KEY_SIZE)
        extensions_cell = s.read_maybe_ref()
        extensions = cell_to_extensions(extensions_cell)

        return cls(
            signature_allowed=signature_allowed,
            seqno=seqno,
            wallet_id=wallet_id,
            public_key=public_key,
            extensions=extensions
        )

    def to_cell(self) -> Cell:
        cell = (begin_cell()
                .store_bit(self.signature_allowed)
                .store_uint(self.seqno, _BitSize.SEQNO)
                .store_uint(self.wallet_id, _BitSize.WALLET_ID)
                .store_bytes(self.public_key)
                .store_maybe_ref(extensions_to_cell(self.extensions))
                .end_cell())
        return cell


class NetworkGlobalID(IntEnum):
    main_net = -239
    test_net = -3


def wallet_v5_wallet_id(workchain: int,
                        subwallet_id: int = 0,
                        network_global_id: int = int(NetworkGlobalID.main_net),
                        wallet_version: int = 0) -> int:
    def tohex(val, nbits):
        return (val + (1 << nbits)) % (1 << nbits)

    context_id = 1 << 31
    context_id |= tohex(workchain, 8) << 23
    context_id |= tohex(wallet_version, 8) << 15
    context_id |= tohex(subwallet_id, 15)

    wallet_id = context_id ^ tohex(network_global_id, 32)

    return wallet_id


def extensions_to_cell(extensions: t.Dict[int, int]) -> t.Optional[Cell]:
    if not extensions:
        return None

    d = begin_dict(_BitSize.EXTENSIONS_DICT_KEY)
    for k, v in extensions.items():
        d.store(k, v)

    def serializer(src, dest: Cell):
        dest.bits.write_int(src, _BitSize.EXTENSIONS_DICT_VALUE)

    return d.end_cell(serializer=serializer)


def cell_to_extensions(cell: Cell) -> t.Dict[int, int]:
    if cell is None:
        return dict()

    def deserializer(s: Slice) -> int:
        return s.read_int(_BitSize.EXTENSIONS_DICT_VALUE)

    return parse_dict(cell.begin_parse(), _BitSize.EXTENSIONS_DICT_KEY, deserializer)


class WalletV5ContractBase(WalletContract):
    def __init__(self, **kwargs):
        def kwget(key: str, default_value):
            if key not in kwargs or kwargs[key] is None:
                return default_value
            return kwargs[key]

        kwargs['signature_allowed'] = kwget('signature_allowed', True)
        kwargs['extensions'] = kwget('extensions', dict())
        kwargs['subwallet_id'] = kwget('subwallet_id', 0)
        kwargs['network_global_id'] = int(kwget('network_global_id', NetworkGlobalID.main_net))
        super().__init__(**kwargs)

    def create_data_cell(self) -> Cell:
        data = WalletV5Data(
            public_key=self.options['public_key'],
            signature_allowed=self.options['signature_allowed'],
            seqno=0,
            wallet_id=self.wallet_id(),
            extensions=self.options['extensions']
        )

        return data.to_cell()

    def wallet_id(self) -> int:
        return wallet_v5_wallet_id(self.options['wc'], self.options['subwallet_id'], self.options['network_global_id'])

    def create_signing_message(self, seqno=None, valid_until: t.Optional[int] = None) -> Cell:
        seqno = seqno or 0
        message = Cell()
        message.bits.write_uint(_Op.AUTH_SIGNED, _BitSize.MESSAGE_OPERATION_PREFIX)
        message.bits.write_uint(self.wallet_id(), _BitSize.WALLET_ID)
        if seqno == 0:
            valid_until = 0xFFFFFFFF
        if valid_until is None:
            raise ValueError('Valid until must be specified if seqno is specified')
        message.bits.write_uint(valid_until, _BitSize.VALID_UNTIL)
        message.bits.write_uint(seqno, _BitSize.SEQNO)

        return message

    def create_init_external_message(self) -> t.Dict:  # TODO refactor: DRY with create_external_message
        create_state_init = self.create_state_init()
        state_init = create_state_init["state_init"]
        address = create_state_init["address"]
        code = create_state_init["code"]
        data = create_state_init["data"]

        signing_message = self.create_signing_message()
        signing_message.write_cell(self.pack_v5_actions([]).end_cell())

        signature = sign_message(
            bytes(signing_message.bytes_hash()), self.options['private_key']).signature

        body = Cell()
        body.write_cell(signing_message)
        body.bits.write_bytes(signature)

        header = Contract.create_external_message_header(address)
        external_message = Contract.create_common_msg_info(
            header, state_init, body)

        return {
            "address": address,
            "message": external_message,
            "body": body,
            "signing_message": signing_message,
            "state_init": state_init,
            "code": code,
            "data": data,
        }

    @classmethod
    def max_internal_messages(cls) -> int:
        return 255

    def create_transfer_message(self, seqno: int, messages: List[InternalMessage], dummy_signature=False,
                                timeout: int = 60, timestamp: Optional[float] = None):
        if len(messages) > self.max_internal_messages():
            raise ValueError(f'Wallet of this type supports a maximum of '
                             f'{self.max_internal_messages()} internal messages')

        timestamp = timestamp or time.time()
        valid_until = int(timestamp) + timeout
        signing_message = self.create_signing_message(seqno, valid_until=valid_until)
        signing_message.write_cell(self.pack_v5_actions(messages).end_cell())

        res = self.create_external_message(signing_message, seqno, dummy_signature)
        res['valid_until'] = valid_until

        return res

    def pack_v5_actions(self, messages: t.List[InternalMessage]) -> Builder:
        list_ = begin_cell().end_cell()
        for message in messages:
            out_msg = Cell()
            self.pack_internal_message(message, out_msg)
            msg = (begin_cell()
                   .store_uint(_Op.ACTION_SEND_MSG, _BitSize.MESSAGE_OPERATION_PREFIX)
                   .store_cell(out_msg))

            list_ = begin_cell().store_ref(list_).store_builder(msg).end_cell()

        return begin_cell().store_maybe_ref(list_).store_uint(0, 1)

    def create_external_message(self, signing_message, seqno, dummy_signature=False) -> t.Dict:
        signature = bytes(64) if dummy_signature else sign_message(
            bytes(signing_message.bytes_hash()), self.options['private_key']).signature  # TODO raise if private key length is not 64

        body = Cell()
        body.write_cell(signing_message)
        body.bits.write_bytes(signature)

        state_init = code = data = None

        if seqno == 0:
            # If seqno == 0 this means that the wallet is not initialized
            deploy = self.create_state_init()
            state_init = deploy["state_init"]
            code = deploy["code"]
            data = deploy["data"]

        self_address = self.address
        header = Contract.create_external_message_header(self_address)
        result_message = Contract.create_common_msg_info(
            header, state_init, body)

        return {
            "address": self_address,
            "message": result_message,
            "body": body,
            "signature": signature,
            "signing_message": signing_message,
            "state_init": state_init,
            "code": code,
            "data": data,
        }


class WalletV5ContractR1(WalletV5ContractBase):
    def __init__(self, **kwargs) -> None:
        self.code = _WALLET_V5R1_CODE
        kwargs["code"] = Cell.one_from_boc(self.code)
        super().__init__(**kwargs)

    @classmethod
    def code_hash(cls) -> str:
        return _WALLET_V5R1_CODE_HASH
