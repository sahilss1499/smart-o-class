# Generated by Django 3.1.7 on 2021-05-08 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20210509_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_link', models.URLField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('token1', models.CharField(max_length=1500)),
                ('token2', models.CharField(max_length=1500)),
                ('token3', models.CharField(max_length=1500)),
            ],
        ),
    ]
