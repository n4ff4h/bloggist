# Generated by Django 4.0.5 on 2022-06-19 15:37

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_quill.fields.QuillField(),
        ),
    ]