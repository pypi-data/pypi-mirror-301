from datetime import datetime

event = EventMessage(
    event_id="12345",
    aggregate_id="abc123",
    aggregate_type="plugin",
    version=2,
    event_type="PLUGIN_RUN",
    event_schema_version="1.1",
    source="PluginService",
    timestamp=datetime.now(),  # Pass a datetime object
    payload={"key": "value"},
    user_id="user123"
)

print(event)
