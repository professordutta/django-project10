# Generated by Django 4.1.3 on 2023-03-05 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myntra_app', '0005_alter_order_product_count_alter_order_product_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_image',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]