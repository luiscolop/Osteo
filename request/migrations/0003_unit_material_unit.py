# Generated by Django 4.2.7 on 2024-06-19 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_material_name_alter_material_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True, verbose_name='Unidad')),
            ],
            options={
                'verbose_name': 'Unidad',
                'verbose_name_plural': 'Unidades',
                'db_table': 'unit',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='material',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='request.unit', verbose_name='Unidad'),
        ),
    ]
