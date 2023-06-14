from typing import Any
from rich.console import RenderableType  # type: ignore
from textual.widgets import Static  # type: ignore


class Base(Static):
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
