# Generated by Django 4.1.4 on 2023-05-03 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_thanksherring'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaderboard',
            options={'ordering': ['-score', '-average_score']},
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='average_score',
            field=models.FloatField(default=0.0),
        ),
    ]
