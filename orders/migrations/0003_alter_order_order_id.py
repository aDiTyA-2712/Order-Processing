# Generated by Django 5.1.3 on 2025-02-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_id_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
