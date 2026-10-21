"""
Seed script — populates the CampusShare database with demo data.

IMPORTANT: The accounts and data created here are for DEVELOPMENT / DEMO
purposes only. Change all passwords before deploying to production.

Usage:
    python seed.py
"""
import os
from datetime import datetime

from app import create_app, db
from app.models.user import User
from app.models.category import Category
from app.models.item import Item, ItemImage

app = create_app()

DEFAULT_CATEGORIES = [
    ("Uniform", "bi-person-badge"),
    ("Books", "bi-book"),
    ("Notes", "bi-journal-text"),
    ("Lab Coat", "bi-eyedropper"),
    ("Calculator", "bi-calculator"),
    ("Electronics", "bi-laptop"),
    ("Stationery", "bi-pencil"),
    ("Hostel Essentials", "bi-house-door"),
    ("Sports Equipment", "bi-trophy"),
    ("Other", "bi-box-seam"),
]

SAMPLE_STUDENTS = [
    dict(full_name="Rahul Sharma", email="rahul", student_id="MCA2401", department="MCA", year="1", semester="1", phone="9876500001"),
    dict(full_name="Priya Verma", email="priya", student_id="MCA2402", department="MCA", year="1", semester="2", phone="9876500002"),
    dict(full_name="Aman Khan", email="aman", student_id="BCA2312", department="BCA", year="3", semester="5", phone="9876500003"),
    dict(full_name="Sneha Patil", email="sneha", student_id="BSCIT2298", department="B.Sc IT", year="2", semester="4", phone="9876500004"),
    dict(full_name="Rohan Deshmukh", email="rohan", student_id="MBA2455", department="MBA", year="2", semester="3", phone="9876500005"),
]

SAMPLE_LISTINGS = [
    dict(owner="rahul", category="Uniform", title="Engineering Uniform (Size L)", listing_type="RENT",
         condition="Good", rental_price_per_day=20, security_deposit=200, quantity=1,
         description="Clean, well-maintained engineering uniform set, size L. Available for short-term rent during practicals."),
    dict(owner="priya", category="Books", title="DBMS Textbook - Korth", listing_type="SELL",
         condition="Like New", price=350, quantity=1,
         description="Database Management Systems by Korth, 6th edition. Barely used, no markings."),
    dict(owner="aman", category="Notes", title="Python Programming Handwritten Notes", listing_type="DONATE",
         condition="Good", price=0, quantity=1,
         description="Complete semester notes for Python programming, neatly handwritten with examples."),
    dict(owner="sneha", category="Lab Coat", title="Chemistry Lab Coat (Size M)", listing_type="RENT",
         condition="Good", rental_price_per_day=15, security_deposit=100, quantity=2,
         description="White lab coat, size M, washed and ready to use for lab sessions."),
    dict(owner="rohan", category="Calculator", title="Casio FX-991ES Plus Calculator", listing_type="SELL",
         condition="Used", price=550, quantity=1,
         description="Scientific calculator in working condition, all functions tested."),
    dict(owner="rahul", category="Stationery", title="Drawing Kit (Engineering Drawing)", listing_type="EXCHANGE",
         condition="Good", exchange_for="Looking for a Data Structures textbook or lab manual.", quantity=1,
         description="Complete engineering drawing kit with compass, set squares and scale."),
    dict(owner="priya", category="Sports Equipment", title="Badminton Racket + Shuttlecocks", listing_type="RENT",
         condition="Good", rental_price_per_day=10, security_deposit=50, quantity=1,
         description="Yonex racket in good condition, comes with a pack of shuttlecocks."),
    dict(owner="aman", category="Hostel Essentials", title="Study Table Lamp", listing_type="SELL",
         condition="Like New", price=180, quantity=1,
         description="LED study lamp with adjustable brightness, perfect for hostel rooms."),
    dict(owner="sneha", category="Electronics", title="USB Mouse (Wired)", listing_type="DONATE",
         condition="Used", price=0, quantity=1,
         description="Basic wired USB mouse, works fine, giving away since I upgraded to wireless."),
    dict(owner="rohan", category="Books", title="Operating Systems - Galvin", listing_type="RENT",
         condition="Good", rental_price_per_day=8, security_deposit=100, quantity=1,
         description="Operating System Concepts by Galvin, useful for OS coursework."),
    dict(owner="rahul", category="Notes", title="Data Structures Notes + Practice Problems", listing_type="SELL",
         condition="Like New", price=120, quantity=1,
         description="Semester notes with solved practice problems for Data Structures."),
    dict(owner="priya", category="Uniform", title="Formal Blazer (Size 40)", listing_type="EXCHANGE",
         condition="Good", exchange_for="Would like a formal blazer in size 38 or a lab coat.", quantity=1,
         description="Formal blazer, worn a few times for seminars, good condition."),
    dict(owner="aman", category="Electronics", title="Scientific Graphing Calculator", listing_type="RENT",
         condition="Good", rental_price_per_day=25, security_deposit=300, quantity=1,
         description="Graphing calculator useful for statistics and data science coursework."),
    dict(owner="sneha", category="Hostel Essentials", title="Iron Box (Travel Size)", listing_type="DONATE",
         condition="Used", price=0, quantity=1,
         description="Compact travel iron box, works well, no longer needed."),
    dict(owner="rohan", category="Sports Equipment", title="Cricket Bat (Kashmir Willow)", listing_type="SELL",
         condition="Used", price=400, quantity=1,
         description="Kashmir willow cricket bat, used for a season, still in good hitting condition."),
]


def run_seed():
    with app.app_context():
        db.create_all()

        domain = app.config["COLLEGE_EMAIL_DOMAIN"]

        # --- Admin -------------------------------------------------------
        if not User.query.filter_by(email=f"admin@{domain}").first():
            admin = User(
                full_name="Admin",
                email=f"admin@{domain}",
                role="ADMIN",
                department="Administration",
                year="-",
                semester="-",
            )
            admin.set_password("Admin@123")
            db.session.add(admin)
            print(f"Created admin: admin@{domain} / Admin@123")

        # --- Categories ----------------------------------------------------
        for name, icon in DEFAULT_CATEGORIES:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name, icon=icon))
        db.session.commit()
        print(f"Seeded {len(DEFAULT_CATEGORIES)} categories.")

        # --- Sample students -------------------------------------------------
        for s in SAMPLE_STUDENTS:
            email = f"{s['email']}@{domain}"
            if not User.query.filter_by(email=email).first():
                user = User(
                    full_name=s["full_name"],
                    email=email,
                    student_id=s["student_id"],
                    department=s["department"],
                    year=s["year"],
                    semester=s["semester"],
                    phone=s["phone"],
                    role="STUDENT",
                )
                user.set_password("Student@123")
                db.session.add(user)
        db.session.commit()
        print(f"Created {len(SAMPLE_STUDENTS)} sample student accounts (password: Student@123).")

        # --- Sample listings -------------------------------------------------
        created = 0
        for listing in SAMPLE_LISTINGS:
            owner = User.query.filter_by(email=f"{listing['owner']}@{domain}").first()
            category = Category.query.filter_by(name=listing["category"]).first()
            if not owner or not category:
                continue
            if Item.query.filter_by(title=listing["title"], owner_id=owner.id).first():
                continue

            item = Item(
                owner_id=owner.id,
                category_id=category.id,
                title=listing["title"],
                description=listing["description"],
                listing_type=listing["listing_type"],
                condition=listing["condition"],
                price=listing.get("price", 0) or 0,
                rental_price_per_day=listing.get("rental_price_per_day", 0) or 0,
                security_deposit=listing.get("security_deposit", 0) or 0,
                exchange_for=listing.get("exchange_for"),
                quantity=listing.get("quantity", 1),
                pickup_location="Main Campus Block",
                status="AVAILABLE",
            )
            db.session.add(item)
            created += 1
        db.session.commit()
        print(f"Created {created} sample listings.")

        print("\nSeeding complete!")
        print("=" * 60)
        print("DEMO CREDENTIALS (development only - change before deployment):")
        print(f"  Admin:   admin@{domain} / Admin@123")
        print(f"  Student: rahul@{domain} / Student@123 (and 4 more)")
        print("=" * 60)


if __name__ == "__main__":
    run_seed()
