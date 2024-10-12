import pytest


pytestmark = [pytest.mark.min_sf_ver("8.35.0")]


def test_fetch_pipe(pipes, template_pipe):
    try:
        pipe_resource = pipes.create(template_pipe)
        fetched_pipe = pipe_resource.fetch()
        assert fetched_pipe.name == template_pipe.name.upper()
        assert fetched_pipe.comment == template_pipe.comment
        assert fetched_pipe.copy_statement == template_pipe.copy_statement

        # create pipe with the same name but with or_replace
        template_pipe.comment = "new comment"
        pipe_resource = pipes.create(template_pipe, mode="or_replace")
        fetched_pipe = pipe_resource.fetch()
        assert fetched_pipe.comment == template_pipe.comment
    finally:
        pipe_resource.drop(if_exist=True)
