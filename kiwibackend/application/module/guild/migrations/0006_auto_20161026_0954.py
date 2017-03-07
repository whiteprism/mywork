# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0005_auctionreward'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuctionReward',
            new_name='GuildAuctionReward',
        ),
    ]
