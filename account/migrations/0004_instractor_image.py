# Generated by Django 3.2.3 on 2021-05-18 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_student_course_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='instractor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d'),
        ),
    ]
