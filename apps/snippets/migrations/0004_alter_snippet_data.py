# Generated by Django 3.2 on 2022-04-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_auto_20220422_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
