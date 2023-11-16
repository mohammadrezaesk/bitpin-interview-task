# Generated by Django 4.2.7 on 2023-11-16 10:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_userprofile_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rater_uuid', models.UUIDField()),
                ('post_uuid', models.UUIDField()),
                ('score', models.IntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')])),
                ('rated_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['post_uuid'], name='posts_postr_post_uu_dcd049_idx'), models.Index(fields=['post_uuid', 'rater_uuid'], name='post_rater_idx')],
                'unique_together': {('rater_uuid', 'post_uuid', 'expired_at')},
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('content', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.userprofile')),
            ],
        ),
    ]