import pandas as pd
from django.contrib.auth.models import Permission


def generate_permissions_list():
    permissions = Permission.objects.all()
    permissions_list = []
    for permission in permissions:
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
    print("permissions_list.csv generated successfully")
