# Generated by Django 3.2.8 on 2021-11-22 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_comment_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='dashboard.post'),
        ),
    ]
