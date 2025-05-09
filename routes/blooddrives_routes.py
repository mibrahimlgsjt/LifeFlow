# blooddrives_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
import os

blood_drives_bp = Blueprint('blood_drives', __name__)

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@blood_drives_bp.route('/add-blood-drive', methods=['GET', 'POST'])
def add_blood_drive():
    if request.method == 'POST':
        form = request.form

        # Extract blood drive details from form
        blood_drive_data = {
            'organizer_name': form.get('organizerName'),
            'organizer_email': form.get('organizerEmail'),
            'drive_name': form.get('driveName'),
            'location': form.get('location'),
            'date': form.get('date'),
            'time': form.get('time'),
            'description': form.get('description')
        }

        # Insert into Supabase blooddrives table
        result = supabase.table("blooddrives").insert(blood_drive_data).execute()

        if result.status_code == 201:
            flash('Blood drive added successfully!', 'success')
            return redirect(url_for('home'))  # Redirect to the homepage or a relevant page
        else:
            flash('Error: Could not add blood drive. Please try again.', 'danger')
            print(result)
            return redirect(request.url)

    return render_template("add-blood-drives.html")

@blood_drives_bp.route('/blood-drives')
def view_blood_drives():
    # Fetch all blood drives from Supabase
    response = supabase.table("blooddrives").select("*").execute()
    blood_drives = response.data
    return render_template("blood-drives.html", blood_drives=blood_drives)