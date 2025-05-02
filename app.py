from flask import Flask, request, redirect, url_for, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
from supabase_client import supabase
from flask_cors import CORS
import os

# Load environment variables from .env file
load_dotenv()

# Access Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Create Flask application
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY", "dev-default-secret")  # Set secret key for sessions
CORS(app)  # Enable CORS

# Serve index.html as homepage
@app.route("/")
def index():
    return send_from_directory('static/html', 'index.html')

# Serve static HTML files
@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory('static/html', filename)

# Sample API test endpoint
@app.route('/api/test', methods=['GET'])
def api_test():
    return jsonify({"message": "API is working!"})

# donors registration (GET: show form, POST: submit form)
@app.route('/register-donors', methods=['GET', 'POST'])
def register_donors():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Optional: Print for debugging
        print("donors Registration Data Received:", data)

        # Insert donors into Supabase
        response = supabase.table("donors").insert({
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "dob": data.get("dob"),
            "gender": data.get("gender"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "address": data.get("address"),
            "city": data.get("city"),
            "province": data.get("province"),
            "postal_code": data.get("postal_code"),
            "preferred_contact_method": data.get("contact_method"),
            "blood_type": data.get("blood_type"),
            "last_donation_date": data.get("last_donation_date") or None,
            "medical_condition": data.get("medical_condition") == "yes",
            "medical_details": data.get("medical_details"),
            "notes": data.get("notes")
        }).execute()

        if response.data:
            return redirect(url_for('serve_html', filename='thank-you.html'))
        else:
            return "Error registering donors", 500
    else:
        # Render form with provinces and blood types
        return render_template("register-donor.html",
                               provinces=["Punjab", "Sindh", "KPK", "Balochistan", "Islamabad"],
                               blood_types=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

# Blood request handling (GET: show form, POST: submit form)
@app.route('/submit/request', methods=['GET', 'POST'])
def blood_request():
    if request.method == 'POST':
        data = request.form.to_dict()

        gender = data.get("gender")
    # Ensure gender matches the Supabase constraint
        if gender:
            gender = gender.capitalize()

        # Insert blood request into Supabase
        response = supabase.table("blood_requests").insert({
            "patient_name": data.get("patientName"),
            "patient_age": data.get("patientAge"),
            "gender": data.get("gender"),
            "hospital": data.get("hospital"),
            "blood_type": data.get("bloodType"),
            "units_needed": int(data.get("unitsNeeded")),
            "required_by": data.get("requiredBy"),
            "urgency": data.get("urgency"),
            "contact_name": data.get("contactName"),
            "relationship": data.get("relationship"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "address": data.get("address"),
            "city": data.get("city"),
            "state": data.get("state"),
            "zipcode": data.get("zipcode"),
            "additional_info": data.get("additionalInfo")
        }).execute()

        if response.data:
           return redirect(url_for('serve_html', filename='thank-you.html'))
        else:
            return "Error submitting blood request", 500
    else:
        # Render the blood request form
        return render_template("request.html")
    
@app.route('/contactform', methods=['POST'])
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

        print("Result object:", result)  # Inspect the entire result object

        if result.data:
            return redirect(url_for('serve_html', filename='thank-you.html'))
        elif hasattr(result, 'error') and result.error:
            print(f"Supabase error (result.error): {result.error}")
            return f"Error: Could not send message. Please try again. Error: {result.error}", 500
        elif result.status_code >= 400:
            print(f"Supabase error (status code): {result.status_code} - {result.status_text}")
            return f"Error: Could not send message. Please try again. Status: {result.status_code} - {result.status_text}", 500
        else:
            # If there's no data and no explicit error, something unexpected happened
            print("Unexpected response:", result)
            return "Error: Could not send message. Please try again.", 500

    # If it's a GET request
    return "Method not allowed", 405

#find-donors.html route
@app.route('/find-donors')
def find_donors_page():
    return render_template('find-donors.html') # You might still be serving the base HTML this way

@app.route('/search_donors', methods=['POST'])
def search_donors():
    blood_type = request.form.get('blood_type')
    city = request.form.get('city')
    province = request.form.get('province')

    query = supabase.table("donors").select("*")
    if blood_type:
        query = query.eq("blood_type", blood_type)
    if city:
        query = query.ilike("city", f"%{city}%")
    if province and province != "Select Province":
        query = query.eq("province", province)

    try:
        response = query.execute()
        donors_data = response.data
        return jsonify(donors=donors_data) # Return the data as JSON
    except Exception as e:
        print(f"Error fetching donors: {e}")
        return jsonify(error="Failed to retrieve donors."), 500 # Return an error with a status code

# Run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
