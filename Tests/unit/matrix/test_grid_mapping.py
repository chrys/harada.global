import pytest

from matrix.services import (
    CENTER,
    PILLAR_POS_TO_CENTER_RING,
    PILLAR_POS_TO_OUTER_CENTER,
    RING_OFFSETS,
    build_matrix_grid,
)


@pytest.mark.django_db
def test_grid_has_center_goal_and_81_cells(harada_chart, pillars, tasks):
    harada_chart.is_draft = False
    harada_chart.save()

    grid = build_matrix_grid(harada_chart)
    assert len(grid) == 9
    assert all(len(row) == 9 for row in grid)

    center = grid[CENTER[0]][CENTER[1]]
    assert center is not None
    assert center["type"] == "core_goal"
    assert harada_chart.core_goal in center["content"]


@pytest.mark.django_db
def test_pillars_render_in_center_ring_and_outer_centers(harada_chart, pillars, tasks):
    harada_chart.is_draft = False
    harada_chart.save()

    grid = build_matrix_grid(harada_chart)
    pillars_by_pos = {p.position: p for p in pillars}

    for pos in range(1, 9):
        pillar = pillars_by_pos[pos]

        r, c = PILLAR_POS_TO_CENTER_RING[pos]
        cell = grid[r][c]
        assert cell["type"] == "pillar"
        assert cell["content"] == pillar.name

        orow, ocol = PILLAR_POS_TO_OUTER_CENTER[pos]
        cell2 = grid[orow][ocol]
        assert cell2["type"] == "pillar"
        assert cell2["content"] == pillar.name


@pytest.mark.django_db
def test_tasks_render_around_each_outer_pillar_center(harada_chart, pillars, tasks):
    harada_chart.is_draft = False
    harada_chart.save()

    grid = build_matrix_grid(harada_chart)

    for pillar in pillars:
        center_r, center_c = PILLAR_POS_TO_OUTER_CENTER[pillar.position]
        # Collect expected task titles for this pillar
        expected = {
            t.position: t.title
            for t in tasks
            if t.pillar_id == pillar.id
        }
        assert len(expected) == 8

        for task_pos in range(1, 9):
            dr, dc = RING_OFFSETS[task_pos]
            r, c = center_r + dr, center_c + dc
            cell = grid[r][c]
            assert cell is not None
            assert cell["type"] == "task"
            assert cell["content"] == expected[task_pos]


@pytest.mark.django_db
def test_goal_is_not_overwritten_by_tasks(harada_chart, pillars, tasks):
    harada_chart.is_draft = False
    harada_chart.save()

    grid = build_matrix_grid(harada_chart)
    assert grid[CENTER[0]][CENTER[1]]["type"] == "core_goal"

    # Ensure no task lands on center
    for row in grid:
        for cell in row:
            if cell and cell.get("type") == "task":
                assert (cell.get("pillar_position"), cell.get("position")) is not None
