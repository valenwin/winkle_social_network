# Generated by Django 3.0.5 on 2020-05-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]