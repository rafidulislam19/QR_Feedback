# Generated by Django 5.0.6 on 2024-08-22 05:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0004_alter_question_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
