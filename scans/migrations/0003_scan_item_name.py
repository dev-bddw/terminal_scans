# Generated by Django 3.2.12 on 2022-05-10 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scans", "0002_alter_scan_origin"),
    ]

    operations = [
        migrations.AddField(
            model_name="scan",
            name="item_name",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
