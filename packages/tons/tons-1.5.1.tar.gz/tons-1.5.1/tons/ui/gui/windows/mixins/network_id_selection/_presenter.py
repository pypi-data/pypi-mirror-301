from typing import Protocol, Sequence, Optional, Any


class Model(Protocol):
    @property
    def available_network_ids(self) -> Sequence[str]: ...
    @property
    def available_network_id_hints(self) -> Sequence[str]: ...
    @property
    def default_network_id(self) -> str: ...


class View(Protocol):
    def set_network_ids(self, available_network_ids: Sequence[str],
                       default_network_id: str,
                       hints: Optional[Sequence[Any]] = None): ...


class NetworkIDSelectPresenter:
    _model: Model
    _view: View

    def _display_network_ids(self):
        self._view.set_network_ids(self._model.available_network_ids, 
                                  self._model.default_network_id, 
                                  self._model.available_network_id_hints)


__all__ = ['NetworkIDSelectPresenter']
