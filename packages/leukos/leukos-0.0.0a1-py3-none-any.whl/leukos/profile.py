import reflex as rx

from .components.navbar import navbar
from .state import FormInputState, State

def profile() -> rx.Component:
    return rx.vstack(
            rx.section(
                navbar()
            ),
            rx.separator(size="4"),
        rx.heading("Profile", color_scheme="lime", padding="16px"),
        rx.flex(
            rx.data_list.root(
                rx.card(
                    rx.data_list.item(
                        rx.hstack(
                        rx.data_list.label(rx.text("Name", weight="bold")),
                            rx.data_list.value(
                                rx.hstack(
                                    rx.badge(
                                        State.username_state,
                                        color_scheme="lime",
                                        style=rx.Style( {
                                            "font_weight": "bold",
                                            }
                                        )
                                    ),
                                    rx.popover.root(
                                        rx.popover.trigger(
                                            rx.badge(
                                                "Edit",
                                                color_scheme="gray",
                                                style=rx.Style({
                                                    "_hover": {
                                                        "cursor": "pointer"
                                                        }
                                                    }
                                                ),
                                            ),
                                        ),
                                        rx.popover.content(
                                            rx.heading(
                                                "Edit Name",
                                                color_scheme="lime",
                                                padding_bottom="16px",
                                            ),
                                            rx.form(
                                                rx.hstack(
                                                    rx.input(
                                                        placeholder="Name...",
                                                        color_scheme="lime",
                                                        name="username",
                                                    ),
                                                    rx.button(
                                                        "Edit",
                                                        color_scheme="lime",
                                                        radius="small",
                                                        type="submit"
                                                    )
                                                ),
                                                on_submit=State.handle_edit_username,
                                                reset_on_submit=True,
                                            ),
                                        )
                                    ),
                                    spacing="2"
                                ),
                            ),
                        ),
                    ),
                )
            ),
        size="4",
        color_scheme="lime",
        align="left",
        padding="16px",
        ),
    )