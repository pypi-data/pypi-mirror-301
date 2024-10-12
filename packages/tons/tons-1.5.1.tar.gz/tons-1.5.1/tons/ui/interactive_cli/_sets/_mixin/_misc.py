from enum import Enum
from typing import Callable

import inquirer

from tons.tonclient.utils import KeyStoreTypeEnum, KeyStoreInvalidPasswordError
from ..._utils import echo_error


class KeyStoreNotSelected(Exception):
    pass


class KeystoreBackupFormat(str, Enum):
    encrypted = 'Encrypted'
    unencrypted = 'Unencrypted'


def requires_keystore_selected(nonstatic_method: Callable):
    def magic(self: 'KeyStoreMixin', *args, **kwargs):
        if self.ctx.keystore is None:
            raise KeyStoreNotSelected
        return nonstatic_method(self, *args, **kwargs)

    return magic


def keystore_sensitive_area(nonstatic_method: Callable):
    @requires_keystore_selected
    def magic(self: 'KeyStoreMixin', *args, **kwargs):
        if self.ctx.keystore.type == KeyStoreTypeEnum.password:
            while True:
                questions = [inquirer.Password("keystore_password", message=f'{self.ctx.keystore.name} password')]
                try:
                    with self.password(self._prompt(questions)["keystore_password"]):
                        return nonstatic_method(self, *args, **kwargs)
                except KeyStoreInvalidPasswordError as e:
                    echo_error(str(e))
                    continue
        return nonstatic_method(self, *args, **kwargs)

    return magic
