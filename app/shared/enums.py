from enum import Enum


class Resource(str, Enum):
    ACCOUNT = 'account'
    ACTIVITY = 'activity'
    ESTATE = 'estate'
    FIELD = 'field'
    USER = 'user'


class Action(str, Enum):
    # CRUD
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
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
    survey = 'survey'
    satellite = 'satellite'
    manual = 'manual'
    imported = 'imported'


# E no seed, a permissão activity:execute é atribuída aos roles que podem
# transitar uma Activity de PLANNED para ACTIVE — distinto de activity:approve,
# que seria a aprovação do planejamento antes da execução.
# Se não implementar isso, MANAGE vira uma action comum sem semântica especial
# o que torna o nome enganoso.
# EXECUTE pode fazer falta
# Para o domínio agrícola, APPROVE cobre aprovação de planejamento,
# mas iniciar uma atividade (PLANNED → ACTIVE) é semanticamente diferente de
# aprovar. Se um MEMBER pode executar mas não aprovar, você vai precisar de
#  EXECUTE eventualmente. Não é urgente — adiciona quando o caso aparecer.
# Fora isso está completo para o estágio atual.
