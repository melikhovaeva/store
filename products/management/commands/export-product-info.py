from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Export product information'

    def handle(self, *args, **options):
        products = Product.objects.all()

        if products:
            for product in products:
                self.stdout.write(self.style.SUCCESS(f"Product: {product.name}"))
                self.stdout.write(f"  Description: {product.description}")
                self.stdout.write(f"  Price: {product.price} rub")
                self.stdout.write(f"  Quantity: {product.quantity}")
                self.stdout.write(f"  Category: {product.category}")
                self.stdout.write("\n")
        else:
            self.stdout.write(self.style.WARNING("No products found"))
