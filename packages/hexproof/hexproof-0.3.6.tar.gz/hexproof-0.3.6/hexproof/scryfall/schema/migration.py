"""
* Scryfall Schema: Migration
* https://scryfall.com/docs/api/migrations
"""
# Standard Library Imports
import datetime
from typing import Literal, Optional, Any

# Third Party Imports
from omnitils.schema import Schema


# Local Imports
from hexproof.scryfall.enums import MigrationStrategy
from hexproof.scryfall.schema.list_object import ListObject


class CardMigration(Schema):
    """An object representing a card data migration on Scryfall."""
    object: Literal['migration'] = 'migration'
    uri: str
    id: str
    performed_at: str | datetime.date
    migration_strategy: MigrationStrategy
    old_scryfall_id: str
    new_scryfall_id: Optional[str] = None
    note: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class CardMigrationList(ListObject):
    """Represents a sequence of CardMigration objects.

    Notes:
        Subset of the 'List' Scryfall object.
        See docs: https://scryfall.com/docs/api/lists
    """
    data: list[CardMigration]
