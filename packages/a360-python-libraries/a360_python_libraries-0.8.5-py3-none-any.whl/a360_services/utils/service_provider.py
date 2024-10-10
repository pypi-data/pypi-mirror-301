from typing import Union

import httpx
from fastapi import Request

from ..settings import settings
from .services_list import Services


class ServiceProvider:
    def __init__(
            self,
            client: httpx.Client,
            token: str = None,
            service: Services = None):
        self.client = client
        self.token = token
        self.service = service

    def fetch_data(self, request_path: str) -> dict:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = self.client.get(
            f"{settings.PROJECT_HOST_SCHEME}://{self.service.value}/services/{self.service.name}{request_path}",
            headers=headers)
        response.raise_for_status()
        return response.json()


def get_dictionary_service_provider(request: Request) -> ServiceProvider:
    client = httpx.Client()
    return ServiceProvider(
        client=client,
        token=get_token(request),
        service=Services.dict
    )


def get_practice_service_provider(request: Request) -> ServiceProvider:
    client = httpx.Client()
    return ServiceProvider(
        client=client,
        token=get_token(request),
        service=Services.practice
    )


def get_token(request: Request) -> Union[str, None]:
    authorization = request.headers.get("Authorization")
    if authorization and authorization.lower().startswith("bearer"):
        return authorization.split(" ")[1]
    return None
