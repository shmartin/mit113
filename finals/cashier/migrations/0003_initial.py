# Generated by Django 5.1.7 on 2025-05-02 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cashier', '0002_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sprice', models.IntegerField()),
                ('sdate', models.DateField(auto_now_add=True)),
                ('ssub_total', models.FloatField()),
                ('sgrand_total', models.FloatField()),
                ('stax_amount', models.FloatField()),
                ('stax_percentage', models.FloatField()),
                ('samount_payed', models.FloatField()),
                ('samount_change', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashier.sale')),
            ],
        ),
    ]
