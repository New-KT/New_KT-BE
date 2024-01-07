# Generated by Django 4.2 on 2024-01-03 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_alter_event_user'),
        ('meeting', '0003_alter_meeting_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.event'),
        ),
        migrations.AlterField(
            model_name='news',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.event'),
        ),
        migrations.DeleteModel(
            name='Meeting',
        ),
    ]
