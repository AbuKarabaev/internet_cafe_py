# Generated by Django 5.1.3 on 2024-12-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe_app', '0003_cheesecake'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_url', models.URLField()),
            ],
        ),
    ]
