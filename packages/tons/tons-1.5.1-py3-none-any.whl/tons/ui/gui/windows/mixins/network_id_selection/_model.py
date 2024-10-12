from typing import Optional, Tuple

from tons.config import Config

from tons.tonsdk.contract.wallet import NetworkGlobalID


class NetworkIDSelectModel:
    _config: Config

    @property
    def available_network_ids(self):
        return 'Mainnet', 'Testnet'

    @property
    def available_network_id_hints(self) -> Tuple[str, ...]:
        return f'({int(NetworkGlobalID.main_net)})', f'({int(NetworkGlobalID.test_net)})'
    

    @property
    def default_network_id(self):
        if self._config.provider.dapp.network == 'mainnet':
            return 'Mainnet'
        return 'Testnet'
    
    def network_id_from_str(self, txt: str) -> Optional[int]:
        if txt == 'Mainnet':
            return int(NetworkGlobalID.main_net)
        elif txt == 'Testnet':
            return int(NetworkGlobalID.test_net)


__all__ = ['NetworkIDSelectModel']
