from typing import Sequence
from tons.ui.gui.promoted_widgets import RichComboBox
from tons.ui.gui.utils._error_handling import slot_exc_handler

from PyQt6.QtCore import pyqtSignal


class WalletVersionSelectView:
    _combo_box_version: RichComboBox
    _version_changed = pyqtSignal(str)
    
    def init_wallet_version_select_view(self):
        self.__setup_signals()
           
    def __setup_signals(self):
        self._combo_box_version.currentIndexChanged.connect(self._on_version_combo_box_index_changed)
        
    @slot_exc_handler()
    def _on_version_combo_box_index_changed(self, current_index: int):
        txt = self._combo_box_version.itemText(current_index).strip()
        self._version_changed.emit(txt)

    @property
    def version(self) -> str:
        return self._combo_box_version.current_data()

    def set_wallet_versions(self, available_versions: Sequence[str], default_version: str,
                            add_default_version_hint: bool = True):
        combo_box = self._combo_box_version
        available_versions = list(available_versions)
        combo_box.clear()
        for idx, version in enumerate(available_versions):
            hint = '(Default)' if (add_default_version_hint and version == default_version) else ''
            combo_box.add_item(version, hint)

        default_idx = available_versions.index(default_version)
        combo_box.setCurrentIndex(default_idx)


__all__ = ['WalletVersionSelectView']
