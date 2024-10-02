from django.contrib.auth.models import AbstractUser
from django.db import models



CHOICES = [('fashion', 'Fashion'),
            ('toys', 'Toys'),
            ('electronics', 'Electronics'),
            ('home', 'Home')
        ]


class User(AbstractUser):
    pass



class AuctionListing(models.Model):
    item_name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, blank=True)
    category = models.CharField(max_length=50, blank=True, null=True, choices=CHOICES)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listings")

    def __str__(self):
        return f"{self.item_name} - > Start Price: {self.starting_price}"

    class Meta:
        verbose_name_plural = "Auction Listings"



class Bids(models.Model):
    auction_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_by.username} - Amount: {self.bid_amount}"

    class Meta:
        verbose_name_plural = "Bids"



class Comments(models.Model):
    commented_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comments = models.CharField(max_length=500)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commented By: {self.comment_by}"

    class Meta:
        verbose_name_plural = "Comments"



class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    auction_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlists")
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.auction_item.item_name}"

    class Meta:
        verbose_name_plural = "Watch Lists"

