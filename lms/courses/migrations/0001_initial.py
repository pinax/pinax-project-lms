# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('code', models.CharField(max_length=50, blank=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('institution', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('version_name', models.CharField(help_text=b'A unique descriptive name for this version of the course.', max_length=100)),
            ],
            options={
                'permissions': (('upload_documents', 'Can upload documents to the course version'), ('download_documents', 'Can download documents from a course version'), ('update_documents', 'Can update documents associated with a course version'), ('delete_documents', 'Can delete documents associated with a course version')),
            },
        ),
        migrations.CreateModel(
            name='OrganizationCourseInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('administrators_team', models.ForeignKey(help_text=b'To contain users who administer the program.', to='teams.Team')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('sequence', models.IntegerField(null=True)),
                ('course_version', models.ForeignKey(to='courses.CourseVersion')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('program', models.ForeignKey(to='courses.Program')),
            ],
        ),
    ]
