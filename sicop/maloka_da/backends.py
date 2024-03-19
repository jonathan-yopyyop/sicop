from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from sicop.maloka_da.utils.da_util import ActiveDirectoryUtil, ActiveDirectoryUser
from sicop.area.models import Area, AreaRole, AreaMember
from django.contrib.auth.models import Group
from sicop.users.models import User


class CustomAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        user_model = get_user_model()
        user_count = User.objects.filter(email=username).count()
        if user_count > 0:
            return user
        active_directory_util = ActiveDirectoryUtil()
        domain = active_directory_util.get_domian()
        domain_extension = active_directory_util.get_domain_extension()
        credential = active_directory_util.get_credential()
        ad_username_split = username.split("@")
        if len(ad_username_split) > 1:
            ad_username_splited = ad_username_split[0].split(".")
            ad_username = ad_username_splited[0]

        else:
            ad_username_splited = ad_username_split[0].split(".")
            ad_username = ad_username_splited[0]
        da_email = f"{ad_username}@{domain}.{domain_extension}"
        user_model = get_user_model()
        if ldap_authenticate(f"{domain}\{ad_username}", password, active_directory_util):
            active_directory_user = ActiveDirectoryUser.objects.filter(
                user=ad_username,
                organizational_unit__credential=credential,
            ).first()
            group = None
            if Group.objects.filter(name=active_directory_user.security_group).count() > 0:
                group = Group.objects.filter(name=active_directory_user.security_group).first()
            area = None
            if Area.objects.filter(name=active_directory_user.area).count() > 0:
                area = Area.objects.filter(name=active_directory_user.area).first()
            role = None
            if AreaRole.objects.filter(name=active_directory_user.role).count() > 0:
                role = AreaRole.objects.filter(name=active_directory_user.role).first()
            try:
                user = user_model.objects.get(email=da_email)

            except user_model.DoesNotExist:
                user = user_model.objects.create_user(
                    password=password,
                    name=active_directory_user.name,
                    email=da_email,
                    is_staff=True,
                    is_active=True,
                )
                if group is not None:
                    user.groups.add(group)
                if area is not None and role is not None:
                    if AreaMember.objects.filter(user=user, area=area, role=role).count() == 0:
                        AreaMember.objects.create(
                            user=user,
                            area=area,
                            role=role,
                            job_title=active_directory_user.position,
                        )

            return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


def ldap_authenticate(username, password, active_directory_util: ActiveDirectoryUtil):
    credenteials_are_valid = active_directory_util.validate_credentials(
        username,
        password,
    )
    return credenteials_are_valid
