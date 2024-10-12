from rich.console import Console
from rich.progress import Progress, TaskID, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn, TimeElapsedColumn
from rich.panel import Panel

SPLASH_LOGO ="""
_______
|  __  |░        _       _      __                          
|  |_| |░__ __ _| |_ ___| |__  / _|_ __ __ _ _ __ ___   ___ 
|  __    |░/ _` | __/ __| '_ \| |_| '__/ _` | '_ ` _ \ / _ \\
|  |_|   |░ (_| | || (__| | | |  _| | | (_| | | | | | |  __/
|________|░\__,_|\__\___|_| |_|_| |_|  \__,_|_| |_| |_|\___|\
"""

class _BatchframeProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks))

class ProgressIndicator:

    _console: Console
    _progress: Progress
    _task_id: TaskID
    _nr_succeeded: int
    _nr_failed: int

    def __init__(self, nr_total_items: int) -> None:
        # TODO: Override styling in progress columns (create PR with rich library)
        self._progress = _BatchframeProgress( 
            TextColumn("[progress.description]{task.description}"),
            BarColumn(style="grey50", complete_style="cyan"),
            MofNCompleteColumn(),
            TaskProgressColumn(style="[grey50]"),
            TextColumn("Succeeded/Failed: [grey50]{task.fields[succeeded]}/{task.fields[failed]}"),
            TextColumn("Elapsed:", justify="right"),
            TimeElapsedColumn(),
            "Remaining:",
            TimeRemainingColumn(),
            expand=True
        )

        self._nr_succeeded = 0
        self._nr_failed = 0

        self._task_id = self._progress.add_task("Processing...", total=nr_total_items, failed=0, succeeded=0)

    def start(self):
        self._progress.start()

    def stop(self):
        self._progress.stop()

    def increment_succeeded(self, steps: int = 1):
        self._nr_succeeded += steps
        self._progress.update(self._task_id, advance=steps, succeeded=self._nr_succeeded)

    def increment_failed(self, steps: int = 1):
        self._nr_failed += steps
        self._progress.update(self._task_id, advance=steps, failed=self._nr_failed)