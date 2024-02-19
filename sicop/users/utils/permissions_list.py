import pandas as pd
from django.contrib.auth.models import Permission


def generate_permissions_list():
    permissions = Permission.objects.all()
    permissions_list = []
    permissions_names_list = []
    counter = 1
    for permission in permissions:
        permissions_names_list.append(f"permission_{counter} = _('{permission.name}')")
        counter += 1
        app_label = permission.content_type.app_label
        codename = permission.codename
        permission_text = f"{app_label}.{codename}"
        permissions_list.append(
            [
                app_label,
                codename,
                permission_text,
            ]
        )
    permissions_list.sort()
    df = pd.DataFrame(
        permissions_list,
        columns=[
            "app_label",
            "codename",
            "permission_text",
        ],
    )
    df.to_csv("permissions_list.csv", index=False)
    permissions_names_list.sort()
    df_name = pd.DataFrame(
        permissions_names_list,
        columns=[
            "permission_name",
        ],
    )
    df_name.to_csv("permissions_names_list.csv", index=False)
    print("permissions_list.csv generated successfully")
