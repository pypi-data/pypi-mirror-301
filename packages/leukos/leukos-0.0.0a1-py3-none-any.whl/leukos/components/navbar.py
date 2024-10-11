import reflex as rx

def navbar_link(text: str, url: str):
    return (
        rx.button(
            text,
            align="center",
            color_scheme="lime",
            on_click=rx.redirect(
                path=url
            ),
            radius="medium",
            size="3",
            style=rx.Style({
                "_hover": {
                    "cursor": "pointer"
                }
            })
        )
    )

def navbar() -> rx.Component():
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.heading(
                            "Leukos", size="9", weight="bold"
                        ),
                        href="/",
                        color_scheme="lime"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("About", "/about"),
                    navbar_link("Proteomics", "/proteins"),
                    navbar_link("Profile", "/profile"),
                    rx.badge(
                        rx.container(
                            rx.color_mode.button(color_scheme="lime", radius="medium"),
                            radius="medium",
                            alignment="center",
                            size="1",
                            padding="2px"
                        ),
                        color_scheme="lime"
                    ),
                    justify="end",
                    spacing="3",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                    rx.heading(
                        "Leukos", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("Home"),
                        rx.menu.item("About"),
                        rx.menu.item("Pricing"),
                        rx.menu.item("Contact"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        padding="1em",
        position="fixed",
        top="0px",
        width="100%",
    )
