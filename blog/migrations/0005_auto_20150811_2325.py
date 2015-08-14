# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150811_2249'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImageUpload',
        ),
        migrations.AddField(
            model_name='entries',
            name='Image',
            field=models.ImageField(default=b'blog/image/no-img.jpg', upload_to=b'blog/image'),
        ),
    ]
