"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import datetime
import logging
import reflex as rx
import sys
import time
from dataclasses import dataclass
from datetime import (datetime,
                      timedelta,
                      timezone
                      )
from enum import Enum, auto
from os import getenv
from rxconfig import config
from typing import Dict, List, Protocol, Set, TypeAlias

from .about import about
from .components.navbar import navbar
from .profile import profile
from .proteins import proteins
from .state import State

# Aliases
dt = datetime

@rx.page(route="/", title="Leukos | Home")
def index() -> rx.Component():
    return rx.vstack(
        rx.section(
            navbar()
        ),
        rx.separator(),
        rx.box(
            rx.card(
                rx.hstack(
                    rx.text(
                        f"Good {State.current_part_of_day}, ",
                        size="6"
                        ),
                        rx.text(
                            State.username_state + ".",
                            color_scheme="lime",
                            size="6",
                            weight="bold",
                        ),
                        spacing="1",
                        padding_bottom="16px",
                    ),
                rx.separator(size="3"),
                rx.heading(
                    "Dashboard",
                    color=rx.color("white"),
                    padding_top="16px",
                    size="7"
                ),
                align="start",
                color="#aaaaaa",
                padding="16px",
            ),
            size="5",
            width="70%",
            align="start",
            padding="16px",
        ),
    )



app = rx.App(
    theme=rx.theme(
        accentColor="lime",
        color_mode="dark"
    )
)
app.add_page(about, title="Leukos | About")
app.add_page(proteins, title="Leukos | Proteomics")
app.add_page(profile, title="Leukos | Profile")
