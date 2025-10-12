from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Полностью очищает базу данных и добавляет новые продукты из фикстуры"

    def handle(self, *args, **kwargs):

        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "catalog_fixture.json")

        self.stdout.write(self.style.SUCCESS("Продукты успешно загружены из файла"))
