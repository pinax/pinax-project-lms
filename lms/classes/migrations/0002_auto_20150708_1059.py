# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('classes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='course_version',
            field=models.ForeignKey(related_name='modules', to='courses.CourseVersion'),
        ),
        migrations.AddField(
            model_name='module',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='documents',
            field=models.ForeignKey(related_name='module_documents', to='documents.Folder', help_text=b'A folder containing documents associated with this module.'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='course_instance',
            field=models.ForeignKey(related_name='lectures', to='courses.CourseInstance'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lecture',
            name='module',
            field=models.ForeignKey(related_name='lectures', to='classes.Module'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='room',
            field=models.ForeignKey(to='classes.Room'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='trainees_team',
            field=models.ForeignKey(to='teams.Team'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='module',
            order_with_respect_to='course_version',
        ),
    ]
