# Generated by Django 3.2.3 on 2021-07-24 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_student_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('-id',), 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AddField(
            model_name='student',
            name='payment_method',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]