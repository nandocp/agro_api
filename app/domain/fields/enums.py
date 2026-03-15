from enum import Enum


class FieldTransitionType(str, Enum):
    MERGE = 'merge'  # Multiple fields → One field
    SPLIT = 'split'  # One field → Multiple fields
