import json
import logging
import os
import reflex as rx

from datetime import datetime as dt
from enum import Enum, auto
from pathlib import Path
from typing import Any, List, TypeAlias

import immunonaut
from immunonaut.core.coretypes import CoreType, Enzyme, Protein, TypeRegistry, UniProtEntity

# Configuring logger
logging.basicConfig(level=logging.INFO,
                       format="LOGGER - %(levelname)s - %(message)s"
                       )
logger = logging.getLogger(__name__)

# Custom typing
Page: TypeAlias = rx.Component

class Pages(Enum):
    index: Page = auto()
    about: Page = auto()
    profile: Page = auto()
    proteins: Page = auto()

class State(rx.State):
    # State constants
    PROJECT_TITLE: str = "Leukos"

    # Base state variables
    current_page: Page = None
    current_datetime: dt = None
    symbol: str = ""
    form_data: dict = {}
    app_state_file: Path = Path("~/leukos_config.json").expanduser()
    if not app_state_file.exists():
        app_state_file.touch()
    username: str

    def nothing(self) -> None:
        """
        A placeholder function
        """
        return

    def handle_edit_username(self, form_data: dict):
        self.username = form_data["username"]

        if not self.app_state_file.exists():
            logger.info("Did not find previously existing app state file... Creating now.")
            self.app_state_file.touch()
            logger.info("Initialized app state file")

        with open(self.app_state_file, "w") as f:
            logger.info("Dumping app state data to JSON")
            json.dump(form_data, f, indent=4)
            logger.info("Dumped app state data to JSON")

        return

    def load_data(self):
        self.username = self.app_state_data["username"] if "username" in self.app_state_data else "Admin"
        return

    @rx.var
    def app_state_data(self) -> dict:
        try:
            return json.loads(self.app_state_file.read_text()) if self.app_state_file.exists() else {}
        except Exception as e:
            logger.error("Failed to load and parse app state data: " + str(e))

    @rx.var
    def current_part_of_day(self) -> str:
        def get_current_time() -> dt:
            self.current_datetime = dt.now()
            return self.current_datetime

        now = get_current_time().strftime("%H")
        logger.info(f"Current time is {now}")

        if 6 <= int(now) < 12:
            current_part_of_day: str = "morning"
        elif 12 <= int(now) < 17:
            current_part_of_day: str = "afternoon"
        else:
            current_part_of_day: str = "evening"

        return str(current_part_of_day)

    @rx.var
    def username_state(self) -> str:
        self.load_data()
        return self.username

    def save_data(self):
        with open(self.app_state_file, "w") as f:
            json.dump(self.state_data, f)

class FormInputState(rx.State):
    query: str = ""
    queries: List[str] = []
    names: List[str] = []
    organisms: List[str] = []
    sequences: List[str] = []
    functions: List[str] = []

    def search(self):
        if self.query:
            # Assuming Protein.from_uniprot returns an object with name and organism attributes
            protein = Protein.from_uniprot(self.query.upper())
            self.queries.append(self.query)
            self.names.append(protein.name)
            self.organisms.append(protein.organism)
            self.sequences.append(protein.sequence)
            self.functions.append(protein.function)
            self.query = ""
