# Generated by Django 3.1.1 on 2021-01-04 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictonary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_word', models.CharField(max_length=100)),
                ('translated_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LeaningModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=60)),
                ('user_pass', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='WorkTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_step', models.SmallIntegerField(default=1)),
                ('training_date', models.DateTimeField(verbose_name='training date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.users')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.dictonary')),
            ],
        ),
        migrations.AddField(
            model_name='dictonary',
            name='users_words',
            field=models.ManyToManyField(through='teacher.WorkTable', to='teacher.Users'),
        ),
    ]