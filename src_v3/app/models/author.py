# -*- coding: utf-8 -*-

from enum import IntEnum


class Author:
    '''Details of a author of a novel'''

    class Type(IntEnum):
        UNKNOWN = 0
        AUTHOR = 1
        ARTIST = 2
        TRANSLATOR = 3
        EDITOR = 4

    def __init__(self, name: str, author_type: Type = Type.UNKNOWN) -> None:
        super().__init__()
        self.type: Type = author_type
        self.name: str = '-' if name is None else name

    def __str__(self):
        return f"<Author name:'{self.name}' type:{self.type.name}>"

    def __eq__(self, other):
        if isinstance(other, Author):
            return self.name == other.name and self.type == other.type
        else:
            return super().__eq__(other)
