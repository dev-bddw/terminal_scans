# Generated by Django 3.2.12 on 2022-07-06 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scans", "0007_alter_scan_scan_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="scan",
            options={"ordering": ["-time_scan"]},
        ),
    ]
