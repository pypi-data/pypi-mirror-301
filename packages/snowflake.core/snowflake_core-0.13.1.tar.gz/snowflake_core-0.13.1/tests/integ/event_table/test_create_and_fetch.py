

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.event_table import EventTable
from snowflake.core.exceptions import ConflictError, NotFoundError
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.35.0")
def test_create_and_fetch(event_tables):
    event_table_name = random_string(10, "test_create_event_table_")

    event_table_created = event_tables.create(
        EventTable(
            name=event_table_name,
            data_retention_time_in_days = 1,
            max_data_extension_time_in_days = 1,
            change_tracking = True,
            default_ddl_collation = 'EN-CI',
            comment="ThIs (*)@#$ is CoM%t"
        )
    )

    try:
        event_table_handle = event_table_created.fetch()
        assert event_table_handle.name.upper() == event_table_name.upper()
        assert event_table_handle.comment == "ThIs (*)@#$ is CoM%t"
        assert event_table_handle.data_retention_time_in_days == 1
        assert event_table_handle.max_data_extension_time_in_days == 1
        assert event_table_handle.change_tracking is True
        assert event_table_handle.default_ddl_collation == 'EN-CI'

        created_time =  event_table_handle.created_on

        with pytest.raises(ConflictError):
            event_tables.create(EventTable(name=event_table_name))

        assert created_time ==\
            event_tables.create(
                EventTable(name=event_table_name),
                mode = CreateMode.if_not_exists
            ).fetch().created_on


        with pytest.raises(NotFoundError):
            event_tables["dummy"].fetch()

    finally:
        event_table_created.drop()
