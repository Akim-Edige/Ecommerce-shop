# Generated by Django 4.2.16 on 2024-12-26 15:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_is_verified_emailverification"),
    ]

    operations = [
        migrations.RenameField(
            model_name="emailverification",
            old_name="expirated_at",
            new_name="expire_at",
        ),
    ]
