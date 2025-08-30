from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# In-memory list of emails
emails = []

# Simple regex for basic email validation
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@app.route("/emails", methods=["GET"])
def get_emails():
    """
    Returns all stored emails
    """
    return jsonify({"emails": emails, "count": len(emails)}), 200


@app.route("/emails", methods=["POST"])
def add_email():
    """
    Adds a new email via POST request
    Example JSON:
    {
        "email": "user@example.com"
    }
    """
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({"error": "Request must contain 'email'"}), 400

    email = data["email"].strip().lower()

    # Validate email format
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    # Prevent duplicates
    if email in emails:
        return jsonify({"error": "Email already exists"}), 409

    emails.append(email)

    return jsonify({"message": "Email added successfully", "email": email}), 201


@app.route("/")
def home():
    return "Welcome to the Mailing List API! Use /emails endpoint."


if __name__ == "__main__":
    app.run(debug=True)
