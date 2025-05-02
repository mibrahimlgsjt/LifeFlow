# request_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
import os

request_bp = Blueprint('request', __name__)

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@request_bp.route('/request', methods=['GET'])
def request_form():
    return render_template('request.html')

@request_bp.route('/submit/request', methods=['POST'])
def submit_request():
    if request.method == 'POST':
        form = request.form

        # Extract request details from form
        request_data = {
            "patient_name": form.get('patientName'),
            "patient_age": form.get('patientAge'),
            "gender": form.get('gender'),
            "hospital": form.get('hospital'),
            "blood_type": form.get('bloodType'),
            "units_needed": form.get('unitsNeeded'),
            "required_by": form.get('requiredBy'),
            "urgency": form.get('urgency'),
            "contact_name": form.get('contactName'),
            "relationship": form.get('relationship'),
            "phone": form.get('phone'),
            "email": form.get('email'),
            "address": form.get('address'),
            "city": form.get('city'),
            "state": form.get('state'),
            "zipcode": form.get('zipcode'),
            "additional_info": form.get('additionalInfo')
        }

        # Insert data into Supabase blood_requests table
        result = supabase.table("blood_requests").insert(request_data).execute()

        if result.status_code == 201:
            flash('Request submitted successfully!', 'success')
            return redirect(url_for('home'))  # Replace 'home' with your actual homepage route
        else:
            flash('Error: Could not submit request. Please try again.', 'danger')
            print(result)
            return redirect(request.url)

    return render_template('request.html') # This line should ideally not be reached in a POST-only route for submission