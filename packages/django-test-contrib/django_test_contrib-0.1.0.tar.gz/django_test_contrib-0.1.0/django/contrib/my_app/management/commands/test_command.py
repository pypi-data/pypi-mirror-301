from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('This is a test command')
