# Generated by Django 4.0.4 on 2022-06-13 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TIS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='rating',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='rating_str',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
