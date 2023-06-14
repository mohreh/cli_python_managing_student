from typing import Any, List
from textual.widgets import DataTable  # type: ignore

from ui.utils.Base import Base  # type: ignore


class BaseTableLoader(Base):
    def load_table(self, table: DataTable, columns: List[Any], rows: List[List[Any]]):
        table.add_columns(*columns)
        table.add_rows(rows)
        table.cursor_type = "row"
        table.zebra_stripes = True
