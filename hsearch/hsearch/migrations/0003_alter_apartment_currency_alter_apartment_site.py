# Generated by Django 4.2.3 on 2023-07-15 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsearch', '0002_auto_20210908_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='currency',
            field=models.IntegerField(choices=[(0, '-'), (1, 'USD'), (2, 'KGS')], default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='site',
            field=models.CharField(choices=[('', 'Undefined'), ('diesel', 'diesel'), ('lalafo', 'lalafo'), ('house', 'house')], default='', max_length=20),
        ),
    ]