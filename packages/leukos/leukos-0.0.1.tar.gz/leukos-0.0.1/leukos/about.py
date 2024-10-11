import reflex as rx

from .components.navbar import navbar

def about() -> rx.Component:
    return rx.vstack(
            rx.section(
                navbar()
            ),
            rx.separator(size="4"),
        rx.box(
            rx.card(
                rx.heading("About", color_scheme="lime"),
                "Leukos is the frontend for the Immunonaut \
                biochemical assaying toolkit.",
                width="100%",
                ),
            spacing="5",
            color_scheme="lime",
            align="left",
            padding="16px",
            width="70%"
        )
    )

