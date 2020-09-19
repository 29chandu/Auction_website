from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import decimal


class User(AbstractUser):
    pass


class Category(models.Model):
    content = models.CharField(max_length=64)

    def __str__(self):
        return str(self.content)


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    image = models.ImageField(upload_to="listing_images", blank=True)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                    MinValueValidator(decimal.Decimal('0.01'))])
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="category_listings", blank=True, null=True)

    def __str__(self):
        return "{}, is-active: {}".format(self.title, self.is_active)


class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                    MinValueValidator(decimal.Decimal('0.01'))])
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_bids")
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Value: {}, Bidder: {}, Listing: {}".format(self.value, self.user, self.listing.title)


class Comment(models.Model):
    content = models.CharField(max_length=256)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments")
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.content)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return "{} watchlist".format(self.user)
