from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with sample Listings, Bookings, and Reviews"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create fake users
        for _ in range(5):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='testpass123'
            )

        users = User.objects.all()

        # Create listings
        for _ in range(10):
            listing = Listing.objects.create(
                title=fake.company(),
                description=fake.paragraph(),
                location=fake.city(),
                price_per_night=random.randint(50, 300),
                max_guests=random.randint(1, 5),
                host=random.choice(users)
            )

            # Create bookings for this listing
            for _ in range(random.randint(1, 3)):
                start = fake.date_between(start_date='-30d', end_date='today')
                end = start + timedelta(days=random.randint(1, 7))
                Booking.objects.create(
                    listing=listing,
                    user=random.choice(users),
                    start_date=start,
                    end_date=end,
                    guests=random.randint(1, listing.max_guests),
                    status=random.choice(['pending', 'confirmed', 'cancelled'])
                )

            # Create reviews
            for _ in range(random.randint(0, 2)):
                Review.objects.create(
                    listing=listing,
                    user=random.choice(users),
                    rating=random.randint(1, 5),
                    comment=fake.sentence()
                )

        self.stdout.write(self.style.SUCCESS("✅ Seed data successfully added."))