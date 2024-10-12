from uuid import UUID

from tons.tonclient import TonError
from tons.ui._utils import SharedObject, truncate
from ..._utils import echo_error, echo_success, processing


class WaitForResultAndEchoMixin:
    ctx: SharedObject

    def _wait_for_result_and_echo(self, task_id: UUID) -> int:
        with processing():
            while (task := self.ctx.background_task_manager.get_task(task_id)).is_pending:
                pass

        result = str(task.result.broadcast_result)

        if isinstance(task.result.broadcast_result, TonError):
            if not self.ctx.debug_mode:
                result = truncate(result)
            echo_error(result)
            return 1
        else:
            echo_success(result)
            return 0
