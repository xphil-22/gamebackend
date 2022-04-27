# Generated by Django 3.2 on 2022-04-22 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_auto_20220415_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='data',
            field=models.JSONField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='highscore',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
