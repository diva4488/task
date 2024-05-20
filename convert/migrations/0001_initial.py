# Generated by Django 5.0.4 on 2024-05-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("csv_file", models.FileField(upload_to="uploads/")),
                ("gpx_file", models.FileField(blank=True, null=True, upload_to="gpx/")),
            ],
        ),
    ]