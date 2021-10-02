# Generated by Django 3.1.1 on 2021-01-05 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_learningmodel_training_interval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictonary',
            name='users_words',
        ),
        migrations.AddField(
            model_name='users',
            name='users_words',
            field=models.ManyToManyField(through='teacher.WorkTable', to='teacher.Dictonary'),
        ),
        migrations.AlterField(
            model_name='worktable',
            name='training_date',
            field=models.DateField(verbose_name='training date'),
        ),
    ]
