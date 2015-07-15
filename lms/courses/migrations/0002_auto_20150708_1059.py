# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationprogram',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='organizationprogram',
            name='program',
            field=models.ForeignKey(to='courses.Program'),
        ),
        migrations.AddField(
            model_name='organizationcourseinstance',
            name='course_instance',
            field=models.ForeignKey(to='courses.CourseInstance'),
        ),
        migrations.AddField(
            model_name='organizationcourseinstance',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organizationcourseinstance',
            name='organization',
            field=models.ForeignKey(to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='courseversion',
            name='administrators_team',
            field=models.ForeignKey(related_name='courseversion_admins', to='teams.Team', help_text=b'For those who administer the course.'),
        ),
        migrations.AddField(
            model_name='courseversion',
            name='course',
            field=models.ForeignKey(to='courses.Course'),
        ),
        migrations.AddField(
            model_name='courseversion',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseversion',
            name='documents',
            field=models.ForeignKey(related_name='courseversion_documents', to='documents.Folder', help_text=b'A folder containing documents associated with this version of the course.'),
        ),
        migrations.AddField(
            model_name='courseversion',
            name='instructors_team',
            field=models.ForeignKey(related_name='courseversion_instructors', to='teams.Team', help_text=b'For those who create the course content.'),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='assessors_team',
            field=models.ForeignKey(related_name='courseinstance_assessors', to='teams.Team', help_text=b'For those assessing the trainees taking the course.'),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='course_version',
            field=models.ForeignKey(to='courses.CourseVersion'),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='instructors_team',
            field=models.ForeignKey(related_name='courseinstance_instructors', to='teams.Team', help_text=b'For those who deliver the course.'),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='teaching_assistants_team',
            field=models.ForeignKey(related_name='courseinstance_teaching_assistants', to='teams.Team', help_text=b'For those assisting in the delivery of the course.'),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='trainees_team',
            field=models.ForeignKey(related_name='courseinstance_trainees', to='teams.Team', help_text=b'For those taking the course.'),
        ),
        migrations.AddField(
            model_name='course',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='organizationprogram',
            unique_together=set([('organization', 'program')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationcourseinstance',
            unique_together=set([('organization', 'course_instance')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseversion',
            unique_together=set([('created_at', 'version_name')]),
        ),
    ]
