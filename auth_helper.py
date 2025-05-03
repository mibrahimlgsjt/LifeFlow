from supabase_client import supabase

def register_user(email, password, user_type):
    """Register a new user with Supabase Auth"""
    try:
        # Register user with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            # Add user metadata to users table
            user_data = {
                "id": auth_response.user.id,
                "email": email,
                "user_type": user_type,
                "is_active": True
            }
            
            # Insert into custom users table
            supabase.table("users").insert(user_data).execute()
            
            return auth_response.user
        return None
    except Exception as e:
        print(f"Error registering user: {e}")
        return None

def login_user(email, password):
    """Login existing user with Supabase Auth"""
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return auth_response.user
    except Exception as e:
        print(f"Error logging in: {e}")
        return None