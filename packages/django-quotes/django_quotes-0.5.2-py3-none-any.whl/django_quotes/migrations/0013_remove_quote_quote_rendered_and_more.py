# Generated by Django 5.0.4 on 2024-04-25 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "django_quotes",
            "0009_alter_source_text_model_alter_sourcegroup_text_model_squashed_0012_remove_sourcemarkovmodel_source_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quote",
            name="quote_rendered",
        ),
        migrations.RemoveField(
            model_name="source",
            name="description_rendered",
        ),
        migrations.RemoveField(
            model_name="sourcegroup",
            name="description_rendered",
        ),
    ]
