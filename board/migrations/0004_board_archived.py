# Generated by Django 4.2 on 2023-04-20 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("board", "0003_alter_board_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="archived",
            field=models.BooleanField(default=False),
        ),
    ]
