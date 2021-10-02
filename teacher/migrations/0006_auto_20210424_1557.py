# Generated by Django 3.1.1 on 2021-04-24 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0005_auto_20210107_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictonary',
            name='users',
            field=models.ManyToManyField(through='teacher.WorkTable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='worktable',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
