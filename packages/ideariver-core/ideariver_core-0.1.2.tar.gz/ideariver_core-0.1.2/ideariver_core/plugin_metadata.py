from dataclasses import dataclass, field
from typing import Optional, Dict, List
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
    outputs: Optional[Dict[str, Optional[str]]] = field(default_factory=dict)
    description: str
    status: str  # Must be one of ['active', 'deprecated', 'pending']
    createdAt: datetime
    updatedAt: datetime
    tags: Optional[List[str]] = field(default_factory=list)
    thumbnailUrl: Optional[str] = None
    imageUrls: Optional[List[str]] = field(default_factory=list)
