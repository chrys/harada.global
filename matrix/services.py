from __future__ import annotations

from dataclasses import dataclass

from charts.models import HaradaChart, Pillar, Task


CENTER = (4, 4)  # 0-based (row, col) for a 9x9 grid

# Positions around a center cell:
# 1 2 3
# 8   4
# 7 6 5
RING_OFFSETS = {
    1: (-1, -1),
    2: (-1, 0),
    3: (-1, 1),
    4: (0, 1),
    5: (1, 1),
    6: (1, 0),
    7: (1, -1),
    8: (0, -1),
}

# Where each pillar is placed around the core goal (center 3x3).
PILLAR_POS_TO_CENTER_RING = {
    1: (3, 3),
    2: (3, 4),
    3: (3, 5),
    4: (4, 5),
    5: (5, 5),
    6: (5, 4),
    7: (5, 3),
    8: (4, 3),
}

# Where each pillar is mirrored as the center of its outer 3x3.
PILLAR_POS_TO_OUTER_CENTER = {
    1: (1, 1),
    2: (1, 4),
    3: (1, 7),
    4: (4, 7),
    5: (7, 7),
    6: (7, 4),
    7: (7, 1),
    8: (4, 1),
}


def build_matrix_grid(chart: HaradaChart):
    """Return a 9x9 list-of-lists of cell dicts for rendering.

    This grid is fully deterministic and follows the Harada mapping:
    - Core goal at (4,4)
    - 8 pillars around the core goal (center 3x3 ring)
    - 8 outer 3x3 blocks, each centered on a mirrored pillar, surrounded by its 8 tasks

    Missing tasks are represented as `task_empty` placeholder cells.
    """

    grid: list[list[dict | None]] = [[None for _ in range(9)] for _ in range(9)]

    # Core goal at exact center
    grid[CENTER[0]][CENTER[1]] = {
        "type": "core_goal",
        "content": chart.core_goal,
        "title": "Core Goal",
    }

    pillars = list(chart.pillar_set.all().order_by("position"))
    pillars_by_pos: dict[int, Pillar] = {p.position: p for p in pillars}

    # Place pillars in center ring and mirrored outer centers
    for pos in range(1, 9):
        pillar = pillars_by_pos.get(pos)
        if not pillar:
            continue

        r, c = PILLAR_POS_TO_CENTER_RING[pos]
        grid[r][c] = {
            "type": "pillar",
            "id": pillar.id,
            "content": pillar.name,
            "color": pillar.color,
            "title": pillar.name,
            "position": pos,
        }

        orow, ocol = PILLAR_POS_TO_OUTER_CENTER[pos]
        grid[orow][ocol] = {
            "type": "pillar",
            "id": pillar.id,
            "content": pillar.name,
            "color": pillar.color,
            "title": pillar.name,
            "position": pos,
            "mirrored": True,
        }

    # Place tasks around each mirrored pillar center
    for pos in range(1, 9):
        pillar = pillars_by_pos.get(pos)
        if not pillar:
            continue

        tasks = list(pillar.task_set.all().order_by("position"))
        tasks_by_pos: dict[int, Task] = {t.position: t for t in tasks}
        center_r, center_c = PILLAR_POS_TO_OUTER_CENTER[pos]

        for task_pos in range(1, 9):
            dr, dc = RING_OFFSETS[task_pos]
            r, c = center_r + dr, center_c + dc
            task = tasks_by_pos.get(task_pos)
            if task:
                grid[r][c] = {
                    "type": "task",
                    "id": task.id,
                    "content": task.title,
                    "status": task.status,
                    "frequency": task.frequency,
                    "color": pillar.color,
                    "title": task.title,
                    "pillar_id": pillar.id,
                    "pillar_position": pos,
                    "position": task_pos,
                    "task_obj": task,  # Pass the actual task object
                }
            else:
                grid[r][c] = {
                    "type": "task_empty",
                    "content": "+ Add",
                    "color": pillar.color,
                    "pillar_id": pillar.id,
                    "pillar_position": pos,
                    "position": task_pos,
                }

    return grid
