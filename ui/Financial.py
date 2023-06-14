from typing import Any
from rich.console import RenderableType  # type: ignore
from textual import on  # type: ignore
from textual.app import ComposeResult  # type: ignore
from textual.widgets import Button, Input, Pretty, Static  # type: ignore

from ui.utils.Base import Base
from data.financial import Financial as FinancialService


class Financial(Base):
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
            user,
            renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        financial_service = FinancialService()
        financial_info = financial_service.find(self.user["id"])
        if not financial_info:
            financial_info = financial_service.insert_base_financial(self.user["id"])
            self.inventory = int(financial_info["inventory"])
            self.debt = int(financial_info["debt"])
        else:
            self.inventory = int(financial_info["inventory"])
            self.debt = int(financial_info["debt"])

    def compose(self) -> ComposeResult:
        yield Static(
            "Financial Info for user {}".format(
                self.user["first_name"] + " " + self.user["last_name"]
            ),
            classes="m-1",
        )
        yield Pretty("", id="financial_errors", classes="m-1")
        yield Static(
            "Your inventory amout: {}".format(self.inventory),
            classes="m-1",
            id="inventory_amount",
        )
        yield Static(
            "Your debt amout: {}".format(self.debt), classes="m-1", id="debt_amount"
        )
        yield Button("Checkout your debt", id="checkout", variant="primary")
        yield Input(
            placeholder="enter amount to increase your inventory",
            id="charge_amount",
        )
        yield Button("Charge the account", id="charge", variant="success")

    @on(Button.Pressed, "#checkout")
    def checkout(self):
        financial_service = FinancialService()
        try:
            financial_info = financial_service.checkout(self.user["id"])

            self.inventory = int(financial_info["inventory"])
            self.debt = int(financial_info["debt"])

            self.query_one("#inventory_amount", expect_type=Static).update(
                "Your inventory amout: {}".format(self.inventory),
            )
            self.query_one("#debt_amount", expect_type=Static).update(
                "Your debt amout: {}".format(self.debt)
            )

            self.query_one("#financial_errors", expect_type=Pretty).update(
                "Debt Checkout Successfully"
            )
        except Exception as err:
            self.query_one("#financial_errors", expect_type=Pretty).update(str(err))

    @on(Button.Pressed, "#charge")
    def charge(self):
        financial_service = FinancialService()
        try:
            amount = int(self.query_one("#charge_amount", expect_type=Input).value)
            financial_info = financial_service.increase_inventory(
                self.user["id"], amount
            )

            self.inventory = int(financial_info["inventory"])
            self.debt = int(financial_info["debt"])

            self.query_one("#inventory_amount", expect_type=Static).update(
                "Your inventory amout: {}".format(self.inventory),
            )
            self.query_one("#debt_amount", expect_type=Static).update(
                "Your debt amout: {}".format(self.debt)
            )

            self.query_one("#financial_errors", expect_type=Pretty).update(
                "Account Charged Successfully"
            )
        except ValueError:
            self.query_one("#financial_errors", expect_type=Pretty).update(
                "Make sure entered amount is a number"
            )
        except Exception as err:
            self.query_one("#financial_errors", expect_type=Pretty).update(str(err))
