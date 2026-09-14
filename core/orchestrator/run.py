from agents.handlers import default_handlers
from core.orchestrator.worker import WorkerRunner


def run_ready_tasks():
    runner = WorkerRunner(default_handlers())
    return runner.run_once()


if __name__ == '__main__':
    for result in run_ready_tasks():
        print(result)
