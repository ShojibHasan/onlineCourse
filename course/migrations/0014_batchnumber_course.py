# Generated by Django 3.2.3 on 2021-07-25 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_batchnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchnumber',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.course'),
        ),
    ]
