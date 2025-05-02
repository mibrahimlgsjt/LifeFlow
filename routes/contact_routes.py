# contact_routes.py
from flask import Blueprint, request, redirect, url_for, flash
from supabase import create_client, Client
import os

contact_bp = Blueprint('contact', __name__)

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@contact_bp.route('/contactform', methods=['POST'])
def handle_contact():
    if request.method == 'POST':
        form = request.form

        # Extract contact details from form
        contact_data = {
            'name': form.get('name'),
            'email': form.get('email'),
            'subject': form.get('subject'),
            'message': form.get('message')
        }

        # Insert into Supabase contact table
        result = supabase.table("contact").insert(contact_data).execute()

        if result.status_code == 201:
            flash('Message sent successfully!', 'success')
            return redirect(url_for('home'))  # Replace 'home' with your actual homepage route or a thank you page
        else:
            flash('Error: Could not send message. Please try again.', 'danger')
            print(result)
            return redirect(request.url)

    # If it's a GET request (e.g., accessing the contact form page), you might want to render a template
    # return render_template("contact.html") # Assuming you have a contact.html template

    # If you only want to handle POST requests, you can just return a method not allowed error for GET
    return "Method not allowed", 405