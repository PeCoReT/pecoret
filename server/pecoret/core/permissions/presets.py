from backend.models.membership import Roles
from .project import ProjectPermission
from .group import GroupPermission, Groups

PRESET_PENTESTER_OR_READONLY = ProjectPermission(
    read_write_roles=[Roles.OWNER, Roles.CONTRIBUTOR, Roles.PROJECT_LEADER],
    read_only_roles=[Roles.READ_ONLY],
)

PRESET_OWNER_OR_READ_ONLY = ProjectPermission(
    read_write_roles=[Roles.OWNER],
    read_only_roles=[Roles.READ_ONLY, Roles.CONTRIBUTOR, Roles.PROJECT_LEADER],
)

PRESET_GROUP_SUPERUSER_OR_READ_ONLY = GroupPermission(
    read_only_groups=[Groups.GROUP_MANAGEMENT, Groups.GROUP_PENTESTER]
)

PRESET_GROUP_MANAGEMENT = GroupPermission(
    read_write_groups=[Groups.GROUP_MANAGEMENT], read_only_groups=[]
)

PRESET_GROUP_PENTESTER_MANAGEMENT = GroupPermission(
    read_write_groups=[Groups.GROUP_MANAGEMENT, Groups.GROUP_PENTESTER],
    read_only_groups=[],
)
