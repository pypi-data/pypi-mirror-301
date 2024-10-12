#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from snowflake.core.compute_pool import (
    ComputePool,
)
from tests.utils import random_string


def test_fetch(compute_pools, temp_cp, instance_family):
    cp_ref = compute_pools[temp_cp.name]

    # testing with correct instance name
    cp = cp_ref.fetch()
    assert (
        cp.name == temp_cp.name.upper()  # for upper/lower case names
    )
    assert cp.min_nodes == 1
    assert cp.max_nodes == 1
    assert cp.created_on
    assert cp.comment == "created by temp_cp"

    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=5,
        comment="created by test_cp",
        auto_resume=False,
        auto_suspend_secs=500,
    )
    try:
        cp_ref = compute_pools.create(test_cp)
        cp = cp_ref.fetch()
        assert cp.name == test_cp.name.upper()
        assert cp.min_nodes == 1
        assert cp.max_nodes == 5
        assert cp.created_on
        assert cp.comment == "created by test_cp"
        assert not cp.auto_resume
        assert cp.state == "STARTING"
        assert cp.auto_suspend_secs == 500
    finally:
        cp_ref.drop()
