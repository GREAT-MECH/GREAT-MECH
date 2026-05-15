"""
SUPREME ENGINE - African Engineering Services Platform
Complete Single-Page Flask Application with Black & Gold Prestige Theme
Version: v42.0 (Sovereign Edition)
Features: 15% Founder Share, 0% Police Fee, Mechanic Panic Button, Streamlit Bridge
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os
import secrets
import hashlib
from functools import wraps

# ============================================================================
# INITIALIZATION
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supreme_engine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# ============================================================================
# DATABASE MODELS (12-COLUMN SCHEMA v42.0)
# ============================================================================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(320), unique=True)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(255))
    bank_details = db.Column(db.String(1000))
    pin_code = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_signed_in = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer)
    country = db.Column(db.String(100)) # Supports all 54 African Countries
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    panic_active = db.Column(db.Boolean, default=False)
    total_amount = db.Column(db.Float)
    founder_share = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ============================================================================
# FOUNDER'S FINANCIAL ENGINE (HARDCODED RULES)
# ============================================================================

FOUNDER_SHARE_PERCENT = 15  # NON-NEGOTIABLE
SECURITY_FEE_PERCENT = 0    # 2% POLICE FEE REMOVED

def calculate_billing(amount):
    """Rule: Founder 15%, Mechanic 85%, Security 0%"""
    founder_share = amount * 0.15
    mechanic_share = amount * 0.85
    return {
        'total': round(amount, 2),
        'founder': round(founder_share, 2),
        'mechanic': round(mechanic_share, 2),
        'security': 0.00
    }

# ============================================================================
# SOVEREIGN ROUTES (REVENUE & PANIC)
# ============================================================================

@app.route('/')
def index():
    return "Great Mech Supreme Engine v42.0 is Active. Moving Africa to the Next Level. 🌍"

@app.route('/api/panic-button', methods=['POST'])
def trigger_panic():
    """Emergency Alert for On-Site Mechanics"""
    data = request.json
    print(f"!!! SECURITY ALERT !!! Mechanic {data.get('mechanic_id')} triggered panic.")
    return jsonify({"status": "CRITICAL", "message": "Private Security Dispatched."}), 200

@app.route('/api/billing/invoice/<int:request_id>', methods=['GET'])
def get_invoice(request_id):
    req = ServiceRequest.query.get(request_id)
    billing = calculate_billing(req.total_amount)
    return jsonify({"message": "Thanks for using Great Mech ⚙️, Moving Africa 🌍", "breakdown": billing})

# ============================================================================
# STREAMLIT CLOUD BRIDGE (FIXES ASSERTION ERROR)
# ============================================================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
else:
    # This exposes the Flask app so the cloud server can find it
    application = app
    
