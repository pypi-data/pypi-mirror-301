"""
This file supports Base Items Pattern for krakenit
"""

from datetime import datetime, timedelta
import random
import uuid
from dateutil.parser import parse

from typing import Union, List, Tuple, Dict
from typing_extensions import Annotated


from syncmodels.model import BaseModel, field_validator, Field
from syncmodels.mapper import *

# from models.generic.price import PriceSpecification
# from models.generic.schedules import OpeningHoursSpecificationSpec

from krakenit.definitions import UID_TYPE

# =========================================================
# A base Krakenit classes
# =========================================================
# TODO: extend model corpus classes, a.k.a: the pydantic based thesaurus foundations classes
# TODO: this classes may be included in the main thesaurus when project is stable
# TODO: and others projects can benefit from them, making the thesaurus bigger and more powerful

# ---------------------------------------------------------
# A base Item
# ---------------------------------------------------------
# TODO: Inherit from smartmodels.model.base (or similar) 
class Item(BaseModel):
    """A Krakenit InventoryItem model"""

    id: UID_TYPE = Field(
        "101_krakenit",
        description="krakenit unique identifier",
        examples=[
            "11111-222222-333333-44444",
            "11111-222222-333333-55555",
            "11111-222222-333333-66666",
        ],
    )
    name: str | None = Field(
        "krakenit no name",
        description="krakenit name",
        examples=[
            "nice-item",
        ],
    )
    description: str | None = Field(
        "a nice krakenit object",
        description="krakenit human more descriptive name",
        examples=[
            "A Nice Item",
        ],
    )

    @field_validator("id")
    def convert_id(cls, value):
        if not isinstance(value, UID_TYPE):
            value = UID_TYPE(value)
        # TODO: make some validations here
        return value

# ---------------------------------------------------------
# A base Request
# ---------------------------------------------------------
class Request(BaseModel):
    """A Krakenit request to task manager.
    Contains all query data and search parameters.
    """
    pass

# ---------------------------------------------------------
# A base Response
# ---------------------------------------------------------
class Response(BaseModel):
    """A Krakenit response to task manager.
    Contains the search results given by a request.
    """
    data: Dict[UID_TYPE, Item] = {}


# =========================================================
# A base KrakenitInventory
# =========================================================

# ---------------------------------------------------------
# A base KrakenitTask
# ---------------------------------------------------------
class Inventory(Item):
    pass


# =========================================================
# A base KrakenitTask
# =========================================================

# ---------------------------------------------------------
# A base KrakenitTask
# ---------------------------------------------------------
class Task(Inventory):
    pass

# =========================================================
# A base KrakenitScript
# =========================================================

# ---------------------------------------------------------
# A base KrakenitScript
# ---------------------------------------------------------
class Script(Inventory):
    pass


