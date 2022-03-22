# Generated by Django 4.0.3 on 2022-03-21 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('T1', 'Single Select'), ('T2', 'Multiple Select')], default='T1', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='TestPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_on', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_applicant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ManyToManyField(to='friendshiptest.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='friendshiptest.question')),
                ('test_paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='friendshiptest.testpaper')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='que_choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='friendshiptest.questiontype'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='friendshiptest.question'),
        ),
    ]
