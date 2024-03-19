from django.core.management.base import BaseCommand
from sicop.maloka_da.utils.da_util import ActiveDirectoryUtil
from sicop.maloka_da.models import ActiveDirectoryUser
from sicop.area.models import Area


class Command(BaseCommand):
    help = "Import Areas from Directory OUs to the database."

    def handle(self, *args, **kwargs):
        try:
            areas = ActiveDirectoryUser.objects.exclude(area="").values("area")
            for area in areas:
                Area.objects.get_or_create(
                    name=area["area"],
                    description=area["area"],
                )
                self.stdout.write(self.style.SUCCESS(f"Area {area['area']} created successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
