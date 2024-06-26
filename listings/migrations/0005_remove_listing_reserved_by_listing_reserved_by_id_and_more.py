# Generated by Django 5.0.6 on 2024-06-04 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_rename_create_at_listing_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='reserved_by',
        ),
        migrations.AddField(
            model_name='listing',
            name='reserved_by_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('PENDING', 'Pending'), ('SOLD', 'Sold')], default='ACTIVE', max_length=20),
        ),
    ]
