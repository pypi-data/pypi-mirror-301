from __future__ import annotations

from typing import Callable, TypeVar, List

import rich
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

T = TypeVar("T")
R = TypeVar("R")


def parallel_track(
    func: Callable[[T], R],
    args: List[T],
    num_workers: int = 8,
    description: str = "Processing",
) -> List[R]:
    from multiprocessing import Pool

    columns = [
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(elapsed_when_finished=True),
    ]
    progress = Progress(*columns, console=rich.get_console())
    with progress:
        task = progress.add_task(description, total=len(args))
        results = []
        with Pool(processes=num_workers) as p:
            for result in p.imap(func, args):
                results.append(result)
                progress.update(task, advance=1)
    return results


__all__ = ["parallel_track"]
