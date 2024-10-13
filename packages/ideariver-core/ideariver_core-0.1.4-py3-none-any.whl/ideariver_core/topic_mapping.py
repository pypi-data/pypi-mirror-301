from dataclasses import dataclass

@dataclass
class Topics:
    """Holds the topic queues."""
    taskQueue: str
    responseQueue: str

@dataclass
class TopicMapping:
    """Represents the mapping of topics to their queues."""
    topics: Topics
