from enum import Enum


class AccountPlan(str, Enum):
    FREE = 'free'
    PRO = 'pro'
    ENTERPRISE = 'enterprise'


class UserRole(str, Enum):
    SUPERUSER = 'superuser'
    ADMIN = 'admin'
    MANAGER = 'manager'
    AGRONOMIST = 'agronomist'
    WORKER = 'worker'
