# Generated by Django 4.0.3 on 2022-03-21 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friendshiptest', '0003_alter_useranswers_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_choice_set', to='friendshiptest.question'),
        ),
    ]
