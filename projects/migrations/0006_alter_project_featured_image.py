# Generated by Django 3.2.6 on 2021-08-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
