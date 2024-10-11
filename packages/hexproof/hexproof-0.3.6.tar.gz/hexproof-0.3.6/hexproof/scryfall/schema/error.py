"""
* Scryfall Schema: Error
* https://scryfall.com/docs/api/errors
"""
# Standard Library Imports
from typing import Literal, Optional

# Third Party Imports
from omnitils.schema import Schema


class Error(Schema):
    """An object representing an error returned from the Scryfall API."""
    object: Literal['error'] = 'error'
    status: int
    code: str
    details: str
    type: Optional[str] = None
    warnings: Optional[list[str]] = None
