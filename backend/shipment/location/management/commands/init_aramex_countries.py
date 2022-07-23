import logging

import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from location.models import CountryCode, ServiceProvider, CityCountryServiceProvider


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Initialize countries with countries codes and bound them with \"Aramex\" ServiceProvider if one exists"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(f"Start process"))

        aramex_service_provider = ServiceProvider.objects.filter(name__iexact="aramex").first()

        country_request_body = {
            "ClientInfo": {
                "UserName": settings.ARAMEX_USERNAME,
                "Password": settings.ARAMEX_PASSWORD,
                "Version": "v1",
                "AccountNumber": settings.ARAMEX_ACCOUNT_NUMBER,
                "AccountPin": settings.ARAMEX_ACCOUNT_PIN,
                "AccountEntity": settings.ARAMEX_ACCOUNT_ENTITY,
                "AccountCountryCode": "JO",
                "Source": 24
            },
            "Code": "JO",
            "Transaction": {"Reference1": "", "Reference2": "", "Reference3": "", "Reference4": "", "Reference5": ""}
        }

        headers = {
            "Accept": "application/json"
        }

        response = requests.post("https://ws.dev.aramex.net/ShippingAPI.V2/Location/Service_1_0.svc/"
                                 "json/FetchCountries",
                                 json=country_request_body,
                                 headers=headers)

        try:
            response.raise_for_status()
        except Exception as e:
            logger.warning(f"{e}")
            self.stdout.write(self.style.WARNING(f"{e}"))
            return

        if response.json()["HasErrors"]:
            for n in response.json()["Notifications"]:
                code = n["Code"]
                message = n["Message"]
                logger.warning(f"{code} - {message}")
                self.stdout.write(self.style.WARNING(f"{code} - {message}"))
                return

        for country in response.json()["Countries"]:
            if country["Code"] not in settings.SHIPPING_COUNTRIES:
                continue

            country_code_object = CountryCode.objects.filter(country_code=country["Code"]).first()

            if not country_code_object:
                priority = 1 if country["Code"] == 'SA' else 0
                country_code_object = CountryCode.objects.create(country_name=country["Name"],
                                                                 country_code=country["Code"],
                                                                 priority=priority)

            if aramex_service_provider:
                country_code_object.service_provider.add(aramex_service_provider)

        city_request_body = {
            "ClientInfo": {
                "UserName": settings.ARAMEX_USERNAME,
                "Password": settings.ARAMEX_PASSWORD,
                "Version": "v1",
                "AccountNumber": settings.ARAMEX_ACCOUNT_NUMBER,
                "AccountPin": settings.ARAMEX_ACCOUNT_PIN,
                "AccountEntity": settings.ARAMEX_ACCOUNT_ENTITY,
                "AccountCountryCode": "JO",
                "Source": 24},
            "CountryCode": None,
            "NameStartsWith": "",
            "State": "",
            "Transaction": {"Reference1": "", "Reference2": "", "Reference3": "", "Reference4": "", "Reference5": ""}
        }

        for cc in CountryCode.objects.filter(service_provider=aramex_service_provider):
            city_request_body["CountryCode"] = cc.country_code
            response = requests.post("https://ws.dev.aramex.net/ShippingAPI.V2/Location/Service_1_0.svc/"
                                     "json/FetchCities",
                                     json=city_request_body,
                                     headers=headers)

            try:
                response.raise_for_status()
            except Exception as e:
                logger.warning(f"{e}")
                self.stdout.write(self.style.WARNING(f"{e}"))
                continue

            if response.json()["HasErrors"]:
                for n in response.json()["Notifications"]:
                    code = n["Code"]
                    message = n["Message"]
                    logger.warning(f"{code} - {message}")
                    self.stdout.write(self.style.WARNING(f"{code} - {message}"))
                    continue

            for r_city_name in response.json()["Cities"]:
                city_country_object = CityCountryServiceProvider.objects.filter(country=cc,
                                                                                city_name__iexact=r_city_name).first()
                if not city_country_object:
                    city_country_object = CityCountryServiceProvider.objects.create(country=cc, city_name=r_city_name)

                if aramex_service_provider:
                    city_country_object.service_provider.add(aramex_service_provider)

            self.stdout.write(self.style.WARNING(f"{cc.country_code} is done"))

        self.stdout.write(self.style.SUCCESS('Countries and their codes are successfully initialized'))
