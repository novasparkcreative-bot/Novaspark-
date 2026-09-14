from core.orchestrator.engine import Orchestrator


class WorkerRunner:
    """Execute ready local tasks through registered handlers."""

    def __init__(self, handlers=None):
        self.handlers = handlers or {}
        self.engine = Orchestrator()

    def register(self, owner, handler):
        self.handlers[owner] = handler

    def run_once(self):
        results = []
        for task in self.engine.ready_tasks():
            handler = self.handlers.get(task["owner"])
            if handler is None:
                continue
            task_id = task["id"]
            self.engine.start(task_id)
            try:
                output = handler(task)
                self.engine.complete(task_id, str(output or "completed"))
                results.append({"task_id": task_id, "status": "completed", "output": output})
            except Exception as exc:
                self.engine.fail(task_id, str(exc))
                results.append({"task_id": task_id, "status": "failed", "error": str(exc)})
        return results
