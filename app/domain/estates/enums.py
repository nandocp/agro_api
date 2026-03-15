from enum import Enum


class EstateZone(str, Enum):
    RURAL = 'rural'
    INTRAURBAN = 'intraurban'
    PERIURBAN = 'periurban'


class OwnershipType(str, Enum):
    OWNED = 'owned'
    LEASED = 'leased'
    CONTRACTED_MANAGEMENT = 'contracted_management'
    SHARECROPPING = 'sharecropping'
    USUFRUCT = 'usufruct'
    CONCESSION = 'concession'


class EstateStatus(str, Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    REJECTED = 'rejected'
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


class EstateUsage(str, Enum):
    FAMILY_FARM = 'family_farm'
    CORPORATE_FARM = 'corporate_farm'
    SETTLEMENT = 'settlement'
    EXTRACTIVE = 'extractive'
    COOPERATIVE = 'cooperative'
    RESEARCH = 'research'
