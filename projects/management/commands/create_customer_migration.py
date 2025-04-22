from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Creates migrations for the Customer model'

    def handle(self, *args, **options):
        call_command('makemigrations', 'projects')
        self.stdout.write(self.style.SUCCESS('Successfully created migrations'))