# Import BasePlugin so that users can access it directly from the package
from .base_plugin import BasePlugin

# Import the OpenAPI-generated models and APIs for convenient access
from .plugin_metadata import PluginMetadata, Author
from .topic_mapping import TopicMapping, Topics
from .event_message import EventMessage  # Import the new class

# Define what will be available when importing the package
__all__ = [
    "BasePlugin",
    "PluginMetadata",
    "Author",
    "TopicMapping",
    "Topics",
    "EventMessage"  # Include EventMessage in the exports
]
