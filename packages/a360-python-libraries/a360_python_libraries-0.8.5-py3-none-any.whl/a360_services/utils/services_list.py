from enum import Enum

from ..settings import settings


class Services(str, Enum):
    dict = settings.PROJECT_HOST_SERVICE_DICT
    patient = settings.PROJECT_HOST_SERVICE_PATIENTS
    practice = settings.PROJECT_HOST_SERVICE_PRACTICES
    ml = settings.PROJECT_HOST_SERVICE_ML
