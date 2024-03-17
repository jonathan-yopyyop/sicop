from django.core.management.base import BaseCommand
from sicop.maloka_da.utils.da_util import ActiveDirectoryUtil


class Command(BaseCommand):
    help = "Import Active Directory users to the database."

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE("DA users importation process started..."))
            active_directory_util = ActiveDirectoryUtil()
            active_directory_util.get_ldap_users()
            self.stdout.write(self.style.NOTICE("DA users importation process finished..."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
