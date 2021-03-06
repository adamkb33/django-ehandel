# Generated by Django 3.0.2 on 2020-05-26 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebutikk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produkt',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='orderelement',
            name='antall',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='produkt',
            name='pris',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
