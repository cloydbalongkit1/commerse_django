# Generated by Django 5.1.1 on 2024-10-04 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_auctionlisting_winner"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="winner_notified",
            field=models.BooleanField(default=False),
        ),
    ]
