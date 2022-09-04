from django.db import models
from bots.models import BotListing, BotBidding
from django.contrib.auth.models import User

# Create your models here.
class ItemInCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, default='')
    listing = models.ManyToManyField(BotListing,default='')
    bidding = models.ManyToManyField(BotBidding,default='')
    use_points = models.FloatField(default=0.0)
    use_balance = models.FloatField(default=0.0)