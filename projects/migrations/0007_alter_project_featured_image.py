# Generated by Django 3.2.6 on 2021-08-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to=''),
        ),
    ]
