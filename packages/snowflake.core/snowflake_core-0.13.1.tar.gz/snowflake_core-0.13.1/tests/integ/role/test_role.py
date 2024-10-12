import pytest

from tests.utils import random_string

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import ConflictError, NotFoundError
from snowflake.core.role import Role


@pytest.mark.use_accountadmin
def test_create(roles, root, session):
    role_name = random_string(4, "test_create_role_")
    try:
        test_role = Role(name=role_name, comment="test_comment")
        created_role = roles.create(test_role)
        assert created_role.name == role_name

        # create role with already existing name with mode or_replace
        replaced_role = roles.create(test_role, mode=CreateMode.or_replace)
        assert replaced_role.name == role_name

        with pytest.raises(ConflictError):
            # throws error if test_role is already present.
            roles.create(test_role, mode=CreateMode.error_if_exists)

        # will succeed without any errors.
        roles.create(test_role, mode=CreateMode.if_not_exists)

    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_name}").collect()


@pytest.mark.use_accountadmin
def test_drop(roles, root, session):
    role_name = random_string(4, "test_drop_role_")
    try:
        test_role = Role(
            name=role_name,
            comment="test drop role"
        )

        created_role = roles.create(test_role)
        assert created_role.name == role_name
        roles[role_name].drop()

        with pytest.raises(NotFoundError):
            # throws error as test_role is already dropped
            roles[role_name].drop()
    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_name}").collect()
