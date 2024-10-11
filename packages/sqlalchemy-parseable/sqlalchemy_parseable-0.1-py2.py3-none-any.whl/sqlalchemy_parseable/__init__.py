__version__ = "0.1"

from .db import Connection, connect
from sqlalchemy.dialects import registry

# Register the Flight end point
registry.register("parseable+flight", "sqlalchemy_parseable.flight", "ParseableDialect_flight")