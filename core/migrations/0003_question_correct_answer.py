# Generated by Django 3.0.5 on 2020-04-16 15:52

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0002_question_answer')]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(default=core.models.get_choice, max_length=2),
        )
    ]
