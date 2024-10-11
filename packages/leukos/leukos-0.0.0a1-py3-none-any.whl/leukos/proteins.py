import reflex as rx

from .components.navbar import navbar
from .state import FormInputState, State

def proteins() -> rx.Component:
    return rx.vstack(
            rx.section(
                navbar()
            ),
            rx.separator(size="4"),
            rx.form.root(
                rx.container(
                    rx.hstack(
                        rx.input(
                            placeholder="Uniprot ID...",
                            on_change=FormInputState.set_query,
                            value=FormInputState.query,
                            align="center",
                            width="100%",
                            color_scheme="lime",
                        ),
                        rx.button("Add", on_click=FormInputState.search, color_scheme="lime"),
                    )
                )
            ),
            rx.container(
                rx.heading("Results", padding_top="2%", color_scheme="lime"),
                rx.grid(
                    rx.foreach(
                        FormInputState.queries,
                        lambda query, i: rx.card(
                            rx.data_list.root(
                                rx.data_list.item(
                                    rx.data_list.label("Uniprot ID"),
                                    rx.data_list.value(rx.badge(query.upper(), variant="soft", radius="full", color_scheme="lime"))
                                ),
                                rx.data_list.item(
                                    rx.data_list.label("Name"),
                                    rx.data_list.value(rx.badge(FormInputState.names[i], variant="soft", radius="full", color_scheme="lime"))
                                ),
                                rx.data_list.item(
                                    rx.data_list.label("Organism"),
                                    rx.data_list.value(rx.badge(FormInputState.organisms[i], variant="soft", radius="full", color_scheme="lime"))
                                ),
                                rx.data_list.item(
                                    rx.data_list.label("Sequence"),

                                    rx.data_list.value(
                                        rx.badge(
                                            rx.text_area(
                                                FormInputState.sequences[i],
                                                background_color="#00000000",
                                            ),
                                            color_scheme="lime",
                                            size="3",
                                            radius="medium",
                                        ),
                                        variant="soft",
                                        radius="small",
                                    ),

                                ),
                                rx.data_list.item(
                                    rx.data_list.label("Function"),

                                rx.data_list.value(
                                    FormInputState.functions[i] + "."
                                    ),
                                ),
                            ),
                        ),
                    ),
                    columns="1",
                    spacing="9",
                ),
                height="100%",
                width="100%",
                align="start",
                spacing="5"
            )
        )
