# -*- coding: utf-8 -*-

from django.db import migrations, transaction
from django.db.models import Case, When, F
from django.db.models.lookups import GreaterThanOrEqual
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_populate'),
    ]

    def update_percent(apps, schema_editor):

        UserLesson = apps.get_model("pages", "UserLesson")
        ul_entries = UserLesson.objects.select_for_update()
        with transaction.atomic():
            for ul in ul_entries:
                view_percent = ul.length_viewed / ul.lesson_length
                if view_percent >= settings.TO_VIEW:
                    ul.is_viewed = True
                    ul.save()
            """
            is_viewed=Case(
                When(
                    GreaterThanOrEqual(F("length_viewed")/F("lesson_length"), 0.8),
                    then=True),
                default=False
                )
            """


    operations = [
        migrations.RunPython(update_percent)
    ]
