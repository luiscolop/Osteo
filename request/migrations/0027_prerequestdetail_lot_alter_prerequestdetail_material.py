# Generated by Django 4.2.7 on 2024-08-08 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0026_prerequest_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='prerequestdetail',
            name='lot',
            field=models.ForeignKey(blank=True, null=b'I01\n', on_delete=django.db.models.deletion.PROTECT, to='request.lot', verbose_name='Lote'),
            preserve_default=b'I01\n',
        ),
        migrations.AlterField(
            model_name='prerequestdetail',
            name='material',
            field=models.ForeignKey(blank=True, null=b'I01\n', on_delete=django.db.models.deletion.PROTECT, to='request.material', verbose_name='Material'),
        ),
    ]
