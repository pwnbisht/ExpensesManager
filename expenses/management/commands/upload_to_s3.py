from django.core.management import BaseCommand
from expenses.tasks import export_data_to_s3


class Command(BaseCommand):
    help = 'Export data to Amazon S3'

    def handle(self, *args, **options):
        export_data_to_s3.delay()
        self.stdout.write(self.style.SUCCESS('Data upload to Amazon S3 initiated successfully'))
