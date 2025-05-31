from rest_framework import serializers
from .models import Listing, Booking, Review


class ListingSerializer(serializers.ModelSerializer):
    host_username = serializers.CharField(source='host.username', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'description',
            'location',
            'price_per_night',
            'max_guests',
            'host_username',
            'created_at',
            'updated_at'
        ]


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    listing_detail = ListingSerializer(source='listing', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'listing',
            'listing_title',
            'listing_detail',  # Nested listing detail
            'user',
            'user_username',
            'start_date',
            'end_date',
            'guests',
            'status',
            'created_at'
        ]

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        if data['guests'] <= 0:
            raise serializers.ValidationError("Guest count must be at least 1.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    listing_detail = ListingSerializer(source='listing', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'listing',            # ID field for write operations (POST/PUT)
            'listing_detail',     # Nested listing for read operations (GET)
            'user',
            'user_username',
            'rating',
            'comment',
            'created_at'
        ]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value