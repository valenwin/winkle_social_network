# Generated by Django 3.0.5 on 2020-04-30 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200424_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='account.Contact', to=settings.AUTH_USER_MODEL),
        ),
    ]
