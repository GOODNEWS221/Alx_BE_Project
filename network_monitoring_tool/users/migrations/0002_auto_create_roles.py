from django.db import migrations

def create_roles(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    roles = [
        {"name": "Admin", "description": "Full access to manage users, roles, devices, metrics, and alerts"},
        {"name": "Editor", "description": "Can add/update devices, metrics, and resolve alerts but not manage users/roles"},
        {"name": "Viewer", "description": "Read-only access to view devices, metrics, alerts, and logs"},
    ]
    for role in roles:
        Role.objects.get_or_create(name=role["name"], defaults={"description": role["description"]})

def delete_roles(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    Role.objects.filter(name__in=["Admin", "Editor", "Viewer"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),  # adjust to match your first migration
    ]

    operations = [
        migrations.RunPython(create_roles, delete_roles),
    ]