# Generated by Django 5.0.3 on 2024-06-11 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comptes', '0003_utilisateur_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='fcm_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]