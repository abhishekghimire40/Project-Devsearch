# Generated by Django 3.2.6 on 2021-08-15 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_review_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.CharField(choices=[('up', 'Up Vote'), ('down', 'Down vVote')], max_length=200),
        ),
    ]