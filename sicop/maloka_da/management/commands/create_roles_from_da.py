from django.core.management.base import BaseCommand
from sicop.maloka_da.utils.da_util import ActiveDirectoryUtil
from sicop.maloka_da.models import ActiveDirectoryUser
from sicop.area.models import AreaRole


class Command(BaseCommand):
    help = "Import Area Roles from Directory OUs to the database."

    def handle(self, *args, **kwargs):
        try:
            roles = ActiveDirectoryUser.objects.exclude(role="").values("role")

            for role in roles:
                role_snake_case = role["role"].lower().replace(" ", "_")
                if AreaRole.objects.filter(code=role_snake_case).count() == 0:
                    AreaRole.objects.get_or_create(
                        code=role_snake_case,
                        name=role["role"],
                    )
                    self.stdout.write(self.style.SUCCESS(f"Role {role} created successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
