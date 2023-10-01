# -*- coding: utf-8 -*-

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    def populate(apps, schema_editor):

        Owner, User, Product, Lesson, UserLesson = [
            apps.get_model("pages", x) for x in
            ("Owner", "User", "Product", "Lesson", "UserLesson")
            ]

        owner = Owner(
            code='[S1TH] -=LordVader=-',
            name='Anakin Skywalker'
            )
        owner.save()

        users = [
            User(
                username=f"user{i}",
                name=f"Test User {i}"
                )
            for i in range(3)
            ]
        [x.save() for x in users]

        lessons = [
            Lesson(
                code=f'l{i}',
                length='212',
                name=f"Lesson {i}",
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ) for i in range(3)]
        [x.save() for x in lessons]

        products = [
            Product(
                code=f"p{i}",
                name=f"Product {i}",
                owner=owner
            ) for i in range(2)]
        [x.save() for x in products]

        products[0].lesson.add(lessons[0], lessons[2])
        products[1].lesson.add(lessons[1], lessons[2])

        products[0].user.add(users[0], users[2])
        products[1].user.add(users[1], users[2])

        lessons_dict = {0: (0, 2), 1: (1, 2), 2: (0, 1, 2)}

        for user, lesson_ids in lessons_dict.items():
            for lesson in lesson_ids:
                ul = UserLesson(
                    user=users[user],
                    lesson=lessons[lesson],
                    lesson_length=212,
                    length_viewed=lesson*100
                    )
                ul.save()

    operations = [
        migrations.RunPython(populate)
    ]
