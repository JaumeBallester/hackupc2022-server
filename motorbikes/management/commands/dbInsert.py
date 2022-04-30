from django.core.management.base import BaseCommand
import csv
from motorbikes.models import Motorbikes, Brands

brandsMapping = {
    'cakeMotorbikes': 'cake',
    'fkm': 'fkMotors'
}

licencesMapping = {
    'a1' : 'a1b',
    'a / a2': 'a'
}

def camelCase(text):
    splited = text.replace('-', ' ').split()
    return splited[0].lower() + ''.join(s.title() for s in splited[1:])


def insertBrands(brands):
    brandsDic = {}
    for brand in brands:
        brandsDic[brand], _ = Brands.objects.get_or_create(name=brand)
    return brandsDic

def insertMotorbikes(brandsDic, bikes):
    for bike in bikes:
        b,_ = Motorbikes.objects.get_or_create(bike_id=bike['id'])
        b.name      = bike['name']
        b.brand     = brandsDic[bike['brand']]
        b.year      = bike['year']
        b.km        = bike['km']
        b.type      = bike['type']
        b.licence   = bike['licence']
        b.old_price = int(bike['old_price'].replace('.','')) if bike['old_price'] else None
        b.price     = int(bike['price'].replace('.',''))
        b.cc        = bike['cc']
        b.url       = bike['url']
        b.image     = bike['image']
        b.save()         


class Command(BaseCommand):
    help = ("""
        Everything and nothing
        """)

    def add_arguments(self, parser):
        parser.add_argument('--filePath', type=str, default="", help="Path to CSV to insert into db")

    def handle(self, *args, **options):
        if options["filePath"]:
            with open(options["filePath"]) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='#')
                line_count = 0
                bikes = []
                brands = set()
                licences = set()
                i = 0
                for row in csv_reader:
                    if i == 0:
                        i+=1
                        continue
                    i+=1
                    #['id', 'brand', 'year', 'c.c.', 'kms', 'type', 'license', 'Old Price', 'New Price', 'name', 'url', 'image']
                    bikes.append(
                        {
                            'id': row[0],
                            'name': row[9],
                            'brand': brandsMapping[camelCase(row[1])] if camelCase(row[1]) in brandsMapping else camelCase(row[1]),
                            'year': row[2],
                            'km': row[4],
                            'type': camelCase(row[5]),
                            'licence': licencesMapping[row[6].lower()] if row[6].lower() in licencesMapping else row[6].lower(),
                            'old_price': row[7],
                            'price': row[8],
                            'cc': row[3],
                            'url': row[10],
                            'image': row[11],
                        }
                    )

                    brands.add(bikes[-1]['brand'])
                brandsDic = insertBrands(brands)
                insertMotorbikes(brandsDic, bikes)
            return
       