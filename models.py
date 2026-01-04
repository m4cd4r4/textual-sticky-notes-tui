from dataclasses import dataclass

@dataclass
class Note:
    noteTitle:str
    content:str= " "
    tags: str = " "
    priority:int = 0
    pinned:bool = False