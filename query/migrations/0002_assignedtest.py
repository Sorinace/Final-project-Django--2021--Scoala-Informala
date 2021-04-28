# Generated by Django 3.0.5 on 2021-04-28 10:28

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedTest',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('data', models.DateField()),
                ('message', models.TextField()),
            ],
        ),
    ]
