from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from sicop.area.models import AreaRole


class Command(BaseCommand):
    help = "Create default roles for areas"

    def handle(self, *args, **options):
        roles = [
            {"code": _("director"), "name": _("Director")},
            {"code": _("chief"), "name": _("Jefe")},
            {"code": _("executor"), "name": _("Ejecutor")},
            {"code": _("administrator"), "name": _("Administrador")},
            {"code": _("president"), "name": _("Presidente")},
            {"code": _("administrative_director"), "name": _("Director administrativo")},
        ]
        for role in roles:
            if AreaRole.objects.filter(code=role["code"], name=role["name"]).count() == 0:
                try:
                    if AreaRole.objects.filter(code=role["code"]).count() > 0:
                        self.stdout.write(self.style.WARNING(f'Role {role["name"]} already exists'))
                    else:
                        AreaRole.objects.create(**role)
                        self.stdout.write(self.style.SUCCESS(f'Role {role["name"]} created successfully'))
                except Exception as e:
                    self.stdout.write(f"Error: {str(e)}")
            else:
                self.stdout.write(self.style.WARNING(f'Role {role["name"]} already exists'))
