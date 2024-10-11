from typing import Union
from urllib.parse import urlencode

from ..utils.service_provider import ServiceProvider


class DictionaryService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_allergies(self, icd10_codes: list[str]) -> dict:
        query_params = {'icd10_code': icd10_codes}
        request_path = f"/allergies?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)
        return response.data.get('items')

    def get_medical_conditions(self, icd10_codes: list[str]) -> dict:
        query_params = {'icd10_code': icd10_codes}
        request_path = f"/medical_conditions?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)
        return response.data.get('items')

    def get_countries(self, iso_codes: list[str]) -> dict:
        query_params = {'iso_code': iso_codes}
        request_path = f"/countries?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)
        return response.data.get('items')

    def get_states(self,
                   iso_codes: list[str],
                   country_iso_code: Union[None,
                                           str] = None) -> dict:
        query_params = {'iso_code': iso_codes}
        request_path = f"/states?{urlencode(query_params, doseq=True)}"
        if country_iso_code:
            request_path = f"/countries/{country_iso_code}/states?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)
        return response.data.get('items')

    def get_cities(self, city_ids: list[str]) -> dict:
        query_params = {'id': city_ids}
        request_path = f"/cities?{urlencode(query_params, doseq=True)}"
        response = self.service_provider.fetch_data(request_path)
        return response.data.get('items')

    def get_tag_categories(
            self,
            search: str = None,
            is_core: bool = None,
            is_active: bool = None) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if is_core is not None:
            query_params['is_core'] = is_core
        if is_active is not None:
            query_params['is_active'] = is_active

        request_path = f"/tag_categories?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_tag_category(self, tag_category_id: str) -> dict:
        request_path = f"/tag_categories/{tag_category_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_tags(self, search: str = None, is_active: bool = None) -> dict:
        query_params = {}

        if search is not None:
            query_params['search'] = search
        if is_active is not None:
            query_params['is_active'] = is_active

        request_path = f"/tags?{urlencode(query_params, doseq=True)}"

        response = self.service_provider.fetch_data(request_path)
        return response.data

    def get_tag(self, tag_id: str) -> dict:
        request_path = f"/tags/{tag_id}"
        response = self.service_provider.fetch_data(request_path)
        return response.data
