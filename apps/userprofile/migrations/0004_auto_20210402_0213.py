# Generated by Django 3.1.4 on 2021-04-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/avatars/'),
        ),
    ]