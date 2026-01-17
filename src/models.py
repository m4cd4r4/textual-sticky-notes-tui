from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid

@dataclass
class Note:
    noteTitle: str
    content: str = " "
    tags: str = " "
    priority: int = 0
    pinned: bool = False
    note_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    attachments: List[str] = field(default_factory=list)  # List of file paths
