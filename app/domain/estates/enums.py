from enum import Enum


class EstateKind(str, Enum):
    RURAL = 'rural'
    INTRAURBAN = 'intraurban'
    PERIURBAN = 'periurban'


class OwnershipType(str, Enum):
    OWNED = 'owned'
    LEASED = 'leased'
    MANAGED = 'managed'


class EstateStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending_validation'
    ARCHIVED = 'archived'


class RegistryStatus(str, Enum):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    NEEDS_CORRECTION = 'needs_correction'
    REJECTED = 'rejected'
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    EXPIRED = 'expired'
    CANCELLED = 'cancelled'
