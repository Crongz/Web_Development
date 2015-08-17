# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_auto_20150813_0941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='Name',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='Password',
        ),
        migrations.AddField(
            model_name='comments',
            name='User',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
