# Generated by Django 3.2 on 2021-05-09 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0003_auto_20210507_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answertest',
            old_name='chosse',
            new_name='choose',
        ),
        migrations.AlterField(
            model_name='assignedtest',
            name='answer',
            field=models.ManyToManyField(blank=True, to='query.AnswerTest'),
        ),
    ]
