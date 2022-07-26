# Generated by Django 4.0.6 on 2022-07-25 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProperty',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_agent', models.CharField(max_length=1000, verbose_name='ユーザーエージェント')),
                ('os', models.CharField(choices=[('mac', 'Mac'), ('windows', 'Windows')], max_length=20, verbose_name='OS')),
            ],
        ),
    ]
