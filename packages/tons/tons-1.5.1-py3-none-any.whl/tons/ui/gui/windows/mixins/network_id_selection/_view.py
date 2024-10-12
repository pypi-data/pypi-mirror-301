from typing import Optional, Sequence, Any

from PyQt6.QtWidgets import QComboBox, QLabel, QWidget
from PyQt6.QtCore import pyqtSignal

from tons.ui.gui.promoted_widgets import RichComboBox


class NetworkIDSelectView:
    _combo_box_network_id: RichComboBox
    _label_network_id_title: QLabel
    version: str  # property
    _version_changed: pyqtSignal
    
    def init_network_id(self):
        self._version_changed.connect(self._update_network_id_visibility_based_on_wallet_version)
    
    def _update_network_id_visibility_based_on_wallet_version(self, wallet_version: str):
        if wallet_version == 'v5r1':
            self._combo_box_network_id.show()
            self._label_network_id_title.show()
        else:
            self._combo_box_network_id.hide()
            self._label_network_id_title.hide()

    @property
    def network_id(self) -> str:
        return self._combo_box_network_id.current_data()

    def set_network_ids(self, available: Sequence[str],
                       default: str,
                       hints: Optional[Sequence[Any]] = None):
        combo_box = self._combo_box_network_id
        values = list(available)
        combo_box.clear()

        for idx, value in enumerate(values):
            data = str(value)
            hint = hints[idx] if hints is not None else ''
            combo_box.add_item(data, hint)

        default_idx = values.index(default)
        combo_box.setCurrentIndex(default_idx)


__all__ = ['NetworkIDSelectView']
