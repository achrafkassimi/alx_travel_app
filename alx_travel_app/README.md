# ALX Travel App – 0x00

This is a Django-based backend application for a travel listings service.  
It includes models for Listings, Bookings, and Reviews, along with API serializers and a custom database seeding command.

---

## 🚀 Features

- Django Models: `Listing`, `Booking`, and `Review`
- REST API serialization for Listing and Booking
- Management command to seed the database with sample data

---

## 🗂️ Project Structure

```bash
alx_travel_app_0x00/
├── listings/
│   ├── models.py           # Models for Listing, Booking, Review
│   ├── serializers.py      # Serializers for Listing and Booking
│   └── management/
│       └── commands/
│           └── seed.py     # Command to seed the database
├── manage.py
└── README.md