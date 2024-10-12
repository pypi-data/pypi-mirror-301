from typing import Protocol

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QWidget

from ._model import TransactionContextMenuModel
from ...utils import macos, windows


class Presenter(Protocol):
    def on_cancel_selected_transaction(self): ...
    def on_edit_and_retry_selected_transaction(self): ...
    def on_check_in_scanner_selected_transaction(self): ...


class TransactionContextMenuView(QMenu):
    def __init__(self, *, parent: QWidget):
        super().__init__(parent=parent)
        self.action_cancel = QAction('Cancel')
        self.action_edit_and_retry = QAction('Edit and retry...')
        self.action_check_in_scanner = QAction('Check in scanner')
        self._add_actions()
        self._set_stylesheet()

    def setup_signals(self, presenter: Presenter):
        self.action_cancel.triggered.connect(presenter.on_cancel_selected_transaction)
        self.action_edit_and_retry.triggered.connect(presenter.on_edit_and_retry_selected_transaction)
        self.action_check_in_scanner.triggered.connect(presenter.on_check_in_scanner_selected_transaction)

    def _add_actions(self):
        self.addAction(self.action_cancel)
        self.addAction(self.action_edit_and_retry)
        self.addSeparator()
        self.addAction(self.action_check_in_scanner)

    def _set_stylesheet(self):
        if macos() or windows():
            self.setStyleSheet("""QMenu::item:disabled {
                                      color: grey;
                                  }""")

    def display_model(self, model: TransactionContextMenuModel):
        self.action_cancel.setEnabled(model.cancel_enabled)
        self.action_edit_and_retry.setEnabled(model.edit_and_retry_enabled)
        self.action_check_in_scanner.setEnabled(model.check_in_scanner_enabled)
