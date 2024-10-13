"""
This file supports Inventory Pattern for krakenit
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

from .base import *

# TODO: extend model corpus classes, a.k.a: the pydantic based thesaurus foundations classes
# TODO: this classes may be included in the main thesaurus when project is stable
# TODO: and others projects can benefit from them, making the thesaurus bigger and more powerful

# ---------------------------------------------------------
# KrakenitItem
# ---------------------------------------------------------
# TODO: Inherit from smartmodels.model.app (or similar) 
class KrakenitItem(Item):
    """A Krakenit Item model"""
    pass

# ---------------------------------------------------------
# A base KrakenitRequest
# ---------------------------------------------------------
class KrakenitRequest(Request):
    """A Krakenit request to task manager.
    Contains all query data and search parameters.
    """
    pass

# ---------------------------------------------------------
# A base KrakenitResponse
# ---------------------------------------------------------
class KrakenitResponse(Response):
    """A Krakenit response to task manager.
    Contains the search results given by a request.
    """
    data: Dict[UID_TYPE, Item] = {}


    
# ---------------------------------------------------------
# KrakenitApp
# ---------------------------------------------------------
# TODO: Inherit from smartmodels.model.app (or similar) 
class KrakenitApp(Item):
    """A Krakenit App model"""
    pass

