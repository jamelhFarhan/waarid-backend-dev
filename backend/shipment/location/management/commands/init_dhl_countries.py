from django.core.management.base import BaseCommand
from django.conf import settings

from location.models import CountryCode, ServiceProvider, CityCountryServiceProvider


class Command(BaseCommand):
    help = "Initialize countries with countries codes and bound them with \"DHL\" ServiceProvider if one exists"

    def handle(self, *args, **options):
        dhl_city_country_file = "/usr/src/app/ESDadd_Q1_4_2022.txt"
        self.stdout.write(self.style.WARNING(f"Start process"))

        dhl_service_provider = ServiceProvider.objects.filter(name="DHL").first()

        country_code_offset = 0
        country_name_offset = 1
        city_name_offset = 4
        post_code1_offset = 6
        post_code2_offset = 7

        done_countries = set()

        with open(dhl_city_country_file) as opened_file:
            for string in opened_file:
                splitted_string = string.split('|')

                if splitted_string[country_code_offset] not in settings.SHIPPING_COUNTRIES:
                    continue

                if splitted_string[country_name_offset] not in done_countries:
                    self.stdout.write(self.style.WARNING(f"{splitted_string[country_name_offset]} is being processed"))
                    done_countries.add(splitted_string[country_name_offset])

                country_code_object = CountryCode.objects.filter(country_code=splitted_string[country_code_offset])\
                    .first()

                if country_code_object:
                    city_name = splitted_string[city_name_offset].title()
                    city_country_object = CityCountryServiceProvider.objects.filter(country=country_code_object,
                                                                                    city_name__iexact=city_name).first()

                    if not city_country_object:
                        city_country_object = CityCountryServiceProvider.objects.create(country=country_code_object,
                                                                                        city_name=city_name)

                    CityCountryServiceProvider.objects.filter(pk=city_country_object.pk)\
                        .update(post_code1=splitted_string[post_code1_offset],
                                post_code2=splitted_string[post_code2_offset])
                else:
                    country_name_titled = splitted_string[country_name_offset].title()
                    priority = 1 if splitted_string[country_code_offset] == 'SA' else 0
                    country_code_object = CountryCode.objects.create(country_code=splitted_string[country_code_offset],
                                                                     country_name=country_name_titled,
                                                                     priority=priority)

                    country_code_object.service_provider.add(dhl_service_provider)

                    city_name = splitted_string[city_name_offset].title()

                    city_country_object = CityCountryServiceProvider.objects.create(country=country_code_object,
                                                                                    city_name=city_name)

                    CityCountryServiceProvider.objects.filter(pk=city_country_object.pk)\
                        .update(post_code1=splitted_string[post_code1_offset],
                                post_code2=splitted_string[post_code2_offset])

                country_code_object.service_provider.add(dhl_service_provider)
                city_country_object.service_provider.add(dhl_service_provider)

        self.stdout.write(self.style.SUCCESS('Countries and their codes are successfully initialized'))
