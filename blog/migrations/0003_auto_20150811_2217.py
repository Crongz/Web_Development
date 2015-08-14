# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_examplemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examplemodel',
            old_name='model_pic',
            new_name='image',
        ),
    ]
