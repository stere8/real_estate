# Generated by Django 5.0.6 on 2024-06-04 16:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_listing_reserved_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='listing',
            name='main_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='reserved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
