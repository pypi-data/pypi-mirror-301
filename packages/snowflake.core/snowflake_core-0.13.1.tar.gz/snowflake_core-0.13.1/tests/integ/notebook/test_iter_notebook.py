from operator import attrgetter

import pytest


@pytest.mark.min_sf_ver("8.37.0")
def test_iter(notebooks, executable_notebook, temp_stage_case_sensitive):
    notebook_names = tuple(
        map(
            attrgetter("name"),
            notebooks.iter(),
        )
    )
    assert any(
        map(
            notebook_names.__contains__,
            (
                executable_notebook.name.upper(),  # for upper/lower case names
            ),
        )
    )


@pytest.mark.min_sf_ver("8.37.0")
def test_iter_like(notebooks, executable_notebook):
    notebook_names = tuple(
        map(
            attrgetter("name"),
            notebooks.iter(like="test_notebook%"),
        )
    )
    assert any(
        map(
            notebook_names.__contains__,
            (
                executable_notebook.name.upper(),  # for upper/lower case names
            ),
        )
    )

