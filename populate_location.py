# You can use this file to populate your django data with the data if you're using Django like I am.

import os
from django.core.management.base import BaseCommand
import json
from location_management.models import City, SubRegion, Region, Country

class Command(BaseCommand):
    help = 'Populate your location models'

    def handle(self, *args, **options):
        self.populate_location()

    def populate_location(self):
        country, created = Country.objects.get_or_create(name="Iraq")
        with open("regions_data.json", "r") as regions_file:
            regions_data = json.load(regions_file)
            country = Country.objects.get(name="Iraq")
            for region in regions_data:
                Region.objects.create(
                    name=region['name'],
                    slug=region['slug'],
                    country=country,
                )

        with open("sub_regions_data.json", "r") as sub_regions_file:
            sub_regions_data = json.load(sub_regions_file)
            country = Country.objects.get(name="Iraq")
            for sub_region in sub_regions_data:
                region = Region.objects.get(name=sub_region['region'])
                SubRegion.objects.create(
                    name=sub_region['name'],
                    slug=sub_region['slug'],
                    region=region,
                    country=country,
                )

        with open("cities_data.json", "r") as cities_file:
            cities_data = json.load(cities_file)
            for city in cities_data:
                region = Region.objects.get(name=city['region'])
                subregion = SubRegion.objects.get(name=city['subregion'])
                City.objects.create(
                    name=city['name'],
                    slug=city['slug'],
                    country=country,
                    region=region,
                    subregion=subregion,
                    longitude=city['longitude'],
                    latitude=city['latitude'],
                    population=city['population'],
                    timezone=city['timezone'],
                )
                

        self.stdout.write(self.style.SUCCESS('Location data has been populated successfully.'))
