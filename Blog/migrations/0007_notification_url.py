# Generated by Django 5.1.2 on 2024-12-08 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_alter_notification_options_alter_notification_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
