# Generated by Django 4.2.13 on 2024-07-01 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_created_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_ordered',
            new_name='reservation_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('CANCELED', 'Canceled')], default='PENDING', max_length=20),
        ),
    ]