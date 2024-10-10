from enum import Enum


class ServiceName(str, Enum):
    dict = 'dict'
    patient = 'patients'
    practice = 'practices'
    ml = 'ml'
