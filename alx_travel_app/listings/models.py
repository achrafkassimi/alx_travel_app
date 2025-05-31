from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    """
    Represents a travel listing (e.g. house, apartment, hotel).
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} in {self.location}"


class Booking(models.Model):
    """
    Represents a booking made by a user for a listing.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.PositiveIntegerField()
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(guests__gt=0), name="guests_positive"),
            models.CheckConstraint(check=models.Q(end_date__gt=models.F('start_date')), name="valid_booking_dates"),
        ]

    def __str__(self):
        return f"Booking by {self.user.username} for {self.listing.title}"


class Review(models.Model):
    """
    Represents a user review for a listing.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listing', 'user')  # A user can review a listing only once
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name="valid_rating_range"),
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.listing.title} - {self.rating}★"