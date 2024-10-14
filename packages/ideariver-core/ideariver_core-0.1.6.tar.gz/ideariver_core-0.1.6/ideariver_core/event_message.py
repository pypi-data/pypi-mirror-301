from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

@dataclass
class EventMessage:
    """Represents an event message for event sourcing."""

    event_id: str  # Unique identifier for the event
    aggregate_id: str  # ID of the entity (aggregate) related to the event
    aggregate_type: str  # Type of aggregate, e.g., 'plugin', 'user', etc.
    version: int  # Version of the aggregate's state after this event
    event_type: str  # Type of the event, e.g., 'PLUGIN_RUN', 'USER_ACTION'
    event_schema_version: str  # Version of the event schema
    source: str  # Origin or source of the event, typically the service name
    timestamp: datetime  # Timestamp for when the event occurred (ISO 8601)
    payload: Dict[str, Any]  # Event data, this varies depending on event type
    user_id: str  # ID of the user initiating the event
