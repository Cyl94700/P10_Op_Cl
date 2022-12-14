# Generated by Django 4.1.3 on 2022-12-02 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_alter_issue_assignee_alter_issue_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
