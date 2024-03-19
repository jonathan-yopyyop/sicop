from django.core.management.base import BaseCommand
from sicop.project.models import ProjectStatus
from sicop.project.data.project_statuses import STATUSES


class Command(BaseCommand):
    help = "Populate Project Statuses."

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE("Project Statuses creation process started..."))
            for status in STATUSES:
                if ProjectStatus.objects.filter(id=status["id"]).count() == 0:
                    ProjectStatus.objects.create(
                        id=status["id"],
                        code=status["code"],
                        name=status["name"],
                    )
                    self.stdout.write(self.style.SUCCESS(f"Project Status {status['name']} created"))
                else:
                    ProjectStatus.objects.filter(id=status["id"]).update(
                        code=status["code"],
                        name=status["name"],
                    )
                    self.stdout.write(self.style.SUCCESS(f"Project Status {status['name']} updated"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
