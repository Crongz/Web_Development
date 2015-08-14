# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150811_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='Image',
            field=models.ImageField(null=True, upload_to=b'blog/image'),
        ),
    ]
