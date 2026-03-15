from enum import Enum


class FieldTransitionKind(str, Enum):
    MERGE = 'merge'  # Multiple fields → One field
    SPLIT = 'split'  # One field → Multiple fields


class FieldProtectionKind(str, Enum):
    ENVIRONMENTAL = 'environmental'  # APP, APA, ARL, Reserva Legal
    EMBARGO = 'embargo'  # IBAMA, órgão estadual
    QUARANTINE = 'quarantine'  # fitossanitária
    HERITAGE = 'heritage'  # histórico, arqueológico, indígena
    CONTRACT = 'contract'  # arrendamento, comodato, penhor
    EASEMENT = 'easement'  # servidão
