from enum import Enum


class Resource(str, Enum):
    ACCOUNT = 'account'
    ACTIVITY = 'activity'
    ESTATE = 'estate'
    FIELD = 'field'
    USER = 'user'
    TASK = 'task'


class Action(str, Enum):
    # CRUD
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
    LIST = 'list'
    # CUSTOM
    EXPORT = 'export'
    ASSIGN = 'assign'
    EXECUTE = 'execute'
    APPROVE = 'approve'
    CANCEL = 'cancel'
    ARCHIVE = 'archive'
    DEACTIVATE = 'deactivate'


class Role(str, Enum):
    SUPERUSER = 'superuser'
    ADMIN = 'admin'
    MANAGER = 'manager'
    WORKER = 'worker'
    AGRONOMIST = 'agronomist'
    VIEWER = 'viewer'


class EPSG(int, Enum):
    WGS84 = 4326
    WEBM = 3857


class GeometrySource(str, Enum):
    SURVEY = 'survey'
    SATELLITE = 'satellite'
    MANUAL = 'manual'
    IMPORTED = 'imported'


class SlopeClass(str, Enum):
    FLAT = 'flat'  # 0-3%
    GENTLE = 'gentle'  # 3-8%
    MODERATE = 'moderate'  # 8-20%
    STRONG = 'strong'  # 20-45%
    STEEP = 'steep'  # 45-75%
    VERY_STEEP = 'very_steep'  # 75-100%


class MaxSlopePercent(int, Enum):
    FLAT = 3
    GENTLE = 8
    MODERATE = 20
    STRONG = 45
    STEEP = 75
    VERY_STEEP = 100
