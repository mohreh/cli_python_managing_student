from typing import Any, List
from rich.console import RenderableType  # type: ignore
from textual.widgets import DataTable, Static  # type: ignore


class BaseTableLoader(Static):
    def __init__(
        self,
        user: dict[str, Any],
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.user = user

    def load_table(self, table: DataTable, columns: List[Any], rows: List[List[Any]]):
        table.add_columns(*columns)
        table.add_rows(rows)
        table.cursor_type = "row"
        table.zebra_stripes = True
