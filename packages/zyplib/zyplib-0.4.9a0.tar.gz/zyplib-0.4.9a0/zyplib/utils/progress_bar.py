from typing import Iterable

from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from tqdm import tqdm


def tqdm_progress(iterable: Iterable, description: str):
    return tqdm(iterable, desc=description)


def rich_progress(iterable: Iterable, description: str, color: str = 'green'):
    with Progress(
        TextColumn('[progress.description]{task.description}'),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        task = progress.add_task(f'[{color}]{description}', total=len(iterable))
        for item in iterable:
            yield item
            progress.update(task, advance=1)
