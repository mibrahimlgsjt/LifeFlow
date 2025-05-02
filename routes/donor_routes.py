# donors_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
import os

donors_bp = Blueprint('donors', __name__)

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Predefined dropdowns (you can load these from a table if needed)
PROVINCES = ['Punjab', 'Sindh', 'KPK', 'Balochistan', 'Islamabad']
BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

@donors_bp.route('/register/donors', methods=['GET', 'POST'])
def register_donors():
    if request.method == 'POST':
        form = request.form

        # Extract donors details from form
        donors_data = {
            'first_name': form.get('first_name'),
            'last_name': form.get('last_name'),
            'dob': form.get('dob'),
            'gender': form.get('gender'),
            'email': form.get('email'),
            'phone': form.get('phone'),
            'address': form.get('address'),
            'city': form.get('city'),
            'province': form.get('province'),
            'postal_code': form.get('postal_code'),
            'preferred_contact_method': form.get('contact_method'),
            'blood_type': form.get('blood_type'),
            'last_donation_date': form.get('last_donation_date') or None,
            'medical_condition': True if form.get('medical_condition') == 'yes' else False,
            'medical_details': form.get('medical_details')
        }

        # Optional: Also add to "User" table if needed
        # supabase.table("User").insert({ ... }).execute()

        # Insert into Supabase donors table
        result = supabase.table("donors").insert(donors_data).execute()

        if result.status_code == 201:
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))  # Replace with your actual homepage route
        else:
            flash('Error: Registration failed. Please try again.', 'danger')
            print(result)
            return redirect(request.url)

    return render_template("register-donor.html", provinces=PROVINCES, blood_types=BLOOD_TYPES)
