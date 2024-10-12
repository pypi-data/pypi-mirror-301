import re
from contextlib import AbstractContextManager
from typing import ClassVar

import polars as pl

from toolkit.manager.client import ManagerClient
from toolkit.manager.models import Accessibility, Ixmp4Instance, User


class AuthorizationContext(AbstractContextManager):
    contexts: ClassVar[list["AuthorizationContext"]] = []

    @classmethod
    def enter_context(cls, ctx: "AuthorizationContext"):
        cls.contexts.append(ctx)

    @classmethod
    def exit_context(cls) -> "AuthorizationContext":
        return cls.contexts.pop()

    @classmethod
    def get_current_context(cls) -> "AuthorizationContext | None":
        try:
            return cls.contexts[-1]
        except IndexError:
            return None

    def __init__(self, user: User | None, manager_client: ManagerClient):
        self.user = user
        self.manager_client = manager_client

    def __enter__(self):
        self.__class__.enter_context(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__class__.exit_context()
        return None

    def __repr__(self):
        return f"<{self.__class__.__name__} user={self.user.username} manager={self.manager_client.url}>"

    def tabulate_permissions(self, platform: Ixmp4Instance):
        if self.user is not None:
            df = self.manager_client.model_permissions.cached_tabulate(
                instance=platform.id,
                group__users=self.user.id,
            )
        else:
            df = pl.DataFrame()
        if platform.accessibility != Accessibility.PRIVATE:
            group_df = self.manager_client.model_permissions.cached_tabulate(
                instance=platform.id, group=platform.access_group
            )
            if df.is_empty() and group_df.is_empty():
                pass
            elif df.is_empty():
                df = group_df
            else:
                df = pl.concat([df, group_df])

        if df.is_empty():
            return df

        df = df.with_columns(
            pl.col("model")
            .map_elements(re.escape, pl.String)
            .str.replace_all(r"\\\*", ".*")
            .alias("regex"),
            pl.col("model").replace("*", "%").replace("_", "[_]").alias("like"),
        )
        return df
