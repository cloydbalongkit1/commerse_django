from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_ending = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listings")


    def __str__(self):
        return self.item_name
    

    class Meta:
        verbose_name_plural = "Auction Listings"



class Bids(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.bid_by.username}: {self.bid_amount}"
    

    class Meta:
        verbose_name_plural = "Bids"



class Comments(models.Model):
    comment = models.CharField(max_length=500)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_time = models.DateTimeField(auto_now_add=True)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")


    def __str__(self):
        return f"{self.comment_by.username}: {self.comment}"
    

    class Meta:
        verbose_name_plural = "Comments"
    

