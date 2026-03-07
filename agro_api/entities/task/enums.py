from enum import Enum


class TaskStatus(str, Enum):
    PENDING = 'pending'          # Created but not started
    IN_PROGRESS = 'in_progress'  # Work has begun
    COMPLETED = 'completed'      # Done successfully
    CANCELLED = 'cancelled'      # Won't be done
    BLOCKED = 'blocked'          # Can't proceed
    DEFERRED = 'deferred'        # Postponed


class TaskPriority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'
