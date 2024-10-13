from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime

@dataclass
class Author:
    """Information about the plugin's author."""
    name: str
    email: str

@dataclass
class PluginMetadata:
    """Represents the metadata for a plugin."""

    id: UUID
    version: str
    executableFile: str
    author: Author
    inputs: Dict[str, Optional[str]]
    outputs: Dict[str, Optional[str]]
    description: str
    status: str  # Should be one of ['active', 'deprecated', 'pending']
    createdAt: datetime
    updatedAt: datetime
    tags: List[str]
    thumbnailUrl: str
    imageUrls: List[str]
