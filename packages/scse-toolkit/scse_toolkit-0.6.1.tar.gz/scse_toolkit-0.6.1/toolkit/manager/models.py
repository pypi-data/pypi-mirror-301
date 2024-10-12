from enum import Enum

from pydantic import BaseModel, ConfigDict


class DjangoBaseModel(BaseModel):
    id: int

    @classmethod
    def from_django_fixture(cls, fixture: dict):
        pk = fixture.get("pk")

        if pk is None:
            raise ValueError

        return cls(id=pk, **fixture.get("fields"))


class Root(BaseModel):
    model_config = ConfigDict(extra="allow")

    messages: dict[str, list[str]]


class User(DjangoBaseModel):
    username: str
    email: str
    is_staff: bool = False
    is_superuser: bool = False
    is_verified: bool = False
    is_authenticated: bool = True
    groups: list[int]


class Accessibility(str, Enum):
    PUBLIC = "PUBLIC"
    GATED = "GATED"
    PRIVATE = "PRIVATE"

    def __str__(self) -> str:
        return self.value


class PermittedGroup(BaseModel):
    id: int
    name: str
    user_count: int


class ServiceInstance(DjangoBaseModel):
    name: str
    slug: str
    description: str | None = None
    management_group: int
    access_group: int

    permitted_groups: list[PermittedGroup] | None = None

    is_mutable: bool = False
    is_viewable: bool = False

    accessibility: Accessibility


class Ixmp4Instance(ServiceInstance):
    url: str
    dsn: str
    notice: str | None = None


class AccessType(str, Enum):
    VIEW = "VIEW"
    EDIT = "EDIT"
    SUBMIT = "SUBMIT"

    def __str__(self) -> str:
        return self.value


class ModelPermission(DjangoBaseModel):
    instance: int
    group: int
    access_type: AccessType
    model: str
