# Generated by Django 5.1.5 on 2025-03-17 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronunciation', '0005_alter_pronunciationrecord_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pronunciationrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
