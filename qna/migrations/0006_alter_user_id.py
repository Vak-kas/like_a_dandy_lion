# Generated by Django 5.0 on 2023-12-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("qna", "0005_alter_answer_author_alter_answer_question_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
