# Generated by Django 3.1 on 2020-09-06 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendreq', 'createsuperuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequest',
            name='friend_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]