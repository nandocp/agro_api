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
    UNDER_REVIEW = 'under_review'
    ACTIVE = 'active'
    PENDING = 'pending'
    ANALYZING = 'analyzing'
    SUSPENDED = 'suspended'
    CANCELED = 'canceled'
    REJECTED = 'rejected'
    NEEDS_CORRECTION = 'needs_correction'
