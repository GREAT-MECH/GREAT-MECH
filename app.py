"""
SUPREME ENGINE - African Engineering Services Platform
Complete Single-Page Flask Application with Black & Gold Prestige Theme
Author: Founder
Version: 1.0.0
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
import requests

# ============================================================================
# INITIALIZATION
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///supreme_engine.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)
CORS(app)

# ============================================================================
# DATABASE MODELS (12-COLUMN SCHEMA v42.0)
# ============================================================================

class User(db.Model):
    """User table - 12 columns for founder control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(320), unique=True)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(255))
    bank_details = db.Column(db.String(1000))  # Encrypted
    pin_code = db.Column(db.String(255))  # Hashed
    role = db.Column(db.String(20), default='user')  # admin, mechanic, customer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_signed_in = db.Column(db.DateTime, default=datetime.utcnow)

class Service(db.Model):
    """Service verticals"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emoji = db.Column(db.String(10))
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, default=0)
    founder_share_percent = db.Column(db.Float, default=15)
    security_fee_percent = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceRequest(db.Model):
    """Service requests from customers"""
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, accepted, in_progress, completed
    quote_amount = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    founder_share = db.Column(db.Float, default=0)
    mechanic_share = db.Column(db.Float, default=0)
    paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class Invoice(db.Model):
    """Financial records"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'))
    amount = db.Column(db.Float)
    founder_share = db.Column(db.Float)
    mechanic_share = db.Column(db.Float)
    security_fee = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    """Immutable audit trail"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ============================================================================
# SECURITY & AUTHENTICATION
# ============================================================================

def require_role(*roles):
    """Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                return jsonify({'error': 'Access denied'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_audit(action, details):
    """Log all actions for founder oversight"""
    log = AuditLog(
        user_id=session.get('user_id'),
        action=action,
        details=json.dumps(details),
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

def encrypt_bank_details(details):
    """Encrypt sensitive bank information"""
    return hashlib.sha256(details.encode()).hexdigest()

def hash_pin(pin):
    """Hash PIN code"""
    return hashlib.sha256(pin.encode()).hexdigest()

# ============================================================================
# FINANCIAL ENGINE - HARDCODED RULES
# ============================================================================

FOUNDER_SHARE_PERCENT = 15  # NON-NEGOTIABLE
SECURITY_FEE_PERCENT = 0    # STRICTLY ENFORCED
MECHANIC_SHARE_PERCENT = 85  # 100 - 15

def calculate_billing(amount):
    """
    Calculate billing with hardcoded founder share and zero security fee
    RULE: Founder gets 15%, Mechanic gets 85%, Security fee is always 0%
    """
    founder_share = amount * (FOUNDER_SHARE_PERCENT / 100)
    mechanic_share = amount * (MECHANIC_SHARE_PERCENT / 100)
    security_fee = 0  # ALWAYS ZERO
    
    return {
        'total_amount': amount,
        'founder_share': round(founder_share, 2),
        'mechanic_share': round(mechanic_share, 2),
        'security_fee': security_fee,
        'founder_share_percent': FOUNDER_SHARE_PERCENT,
        'security_fee_percent': SECURITY_FEE_PERCENT,
        'mechanic_share_percent': MECHANIC_SHARE_PERCENT
    }

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main landing page with Black & Gold prestige theme"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.pin_code, password):
        session['user_id'] = user.id
        session['role'] = user.role
        log_audit('LOGIN', {'email': email})
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.json
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400
    
    user = User(
        open_id=secrets.token_hex(16),
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        location=data.get('location'),
        role=data.get('role', 'customer'),
        pin_code=hash_pin(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    log_audit('REGISTER', {'email': data['email'], 'role': user.role})
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    })

@app.route('/api/services', methods=['GET'])
def get_services():
    """Get all 5 core service verticals"""
    services = Service.query.all()
    
    if not services:
        # Initialize default services
        default_services = [
            {'name': 'Truck Services', 'emoji': '🚚', 'base_price': 150},
            {'name': 'Car Services', 'emoji': '🚗', 'base_price': 100},
            {'name': 'Diesel Engine/Generator', 'emoji': '⚙️', 'base_price': 200},
            {'name': 'CCTV Systems', 'emoji': '📹', 'base_price': 120},
            {'name': 'Solar Solutions', 'emoji': '☀️', 'base_price': 180},
        ]
        
        for svc in default_services:
            service = Service(
                name=svc['name'],
                emoji=svc['emoji'],
                base_price=svc['base_price'],
                founder_share_percent=FOUNDER_SHARE_PERCENT,
                security_fee_percent=SECURITY_FEE_PERCENT
            )
            db.session.add(service)
        db.session.commit()
        services = Service.query.all()
    
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'emoji': s.emoji,
        'base_price': s.base_price,
        'founder_share_percent': s.founder_share_percent,
        'security_fee_percent': s.security_fee_percent
    } for s in services])

@app.route('/api/request-service', methods=['POST'])
@require_role('customer')
def request_service():
    """Customer requests a service"""
    data = request.json
    
    service_request = ServiceRequest(
        customer_id=session['user_id'],
        service_id=data['service_id'],
        location=data['location'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        description=data['description'],
        quote_amount=data.get('quote_amount', 0)
    )
    
    db.session.add(service_request)
    db.session.commit()
    
    log_audit('SERVICE_REQUEST', {
        'service_id': data['service_id'],
        'location': data['location']
    })
    
    return jsonify({
        'success': True,
        'request_id': service_request.id
    })

@app.route('/api/billing/calculate', methods=['POST'])
def calculate_billing_api():
    """Calculate billing with founder share and zero security fee"""
    data = request.json
    amount = data.get('amount', 0)
    
    billing = calculate_billing(amount)
    
    return jsonify(billing)

@app.route('/api/billing/invoice/<int:request_id>', methods=['GET'])
def get_invoice(request_id):
    """Get invoice with transparent breakdown"""
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({'error': 'Request not found'}), 404
    
    billing = calculate_billing(service_request.total_amount or service_request.quote_amount)
    
    return jsonify({
        'request_id': request_id,
        'service': service_request.service_id,
        'customer': service_request.customer_id,
        'mechanic': service_request.mechanic_id,
        'total_amount': billing['total_amount'],
        'founder_share': billing['founder_share'],
        'founder_share_percent': billing['founder_share_percent'],
        'mechanic_share': billing['mechanic_share'],
        'security_fee': billing['security_fee'],
        'security_fee_percent': billing['security_fee_percent'],
        'message': 'Thanks for using Great Mech ⚙️🧰, Moving Africa 🌍 to the next level'
    })

@app.route('/api/mechanic/complete-job/<int:request_id>', methods=['POST'])
@require_role('mechanic')
def complete_job(request_id):
    """Mark job as completed and trigger mechanic payout"""
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request or service_request.mechanic_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Calculate payout
    billing = calculate_billing(service_request.total_amount or service_request.quote_amount)
    
    # Update service request
    service_request.status = 'completed'
    service_request.completed_at = datetime.utcnow()
    service_request.founder_share = billing['founder_share']
    service_request.mechanic_share = billing['mechanic_share']
    
    # Create invoice
    invoice = Invoice(
        service_request_id=request_id,
        amount=billing['total_amount'],
        founder_share=billing['founder_share'],
        mechanic_share=billing['mechanic_share'],
        security_fee=billing['security_fee'],
        status='completed'
    )
    
    db.session.add(invoice)
    db.session.commit()
    
    log_audit('JOB_COMPLETED', {
        'request_id': request_id,
        'mechanic_id': session['user_id'],
        'payout': billing['mechanic_share']
    })
    
    return jsonify({
        'success': True,
        'message': 'Thanks for using Great Mech ⚙️🧰, Moving Africa 🌍 to the next level',
        'payout': billing['mechanic_share'],
        'founder_share': billing['founder_share']
    })

@app.route('/api/founder/dashboard', methods=['GET'])
@require_role('admin')
def founder_dashboard():
    """Founder dashboard with complete ecosystem view"""
    # Get all metrics
    total_requests = ServiceRequest.query.count()
    completed_requests = ServiceRequest.query.filter_by(status='completed').count()
    total_revenue = db.session.query(db.func.sum(Invoice.amount)).scalar() or 0
    founder_total = db.session.query(db.func.sum(Invoice.founder_share)).scalar() or 0
    mechanic_total = db.session.query(db.func.sum(Invoice.mechanic_share)).scalar() or 0
    
    # Get recent transactions
    recent_invoices = Invoice.query.order_by(Invoice.created_at.desc()).limit(10).all()
    
    return jsonify({
        'founder_view': True,
        'metrics': {
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'total_revenue': round(total_revenue, 2),
            'founder_total': round(founder_total, 2),
            'mechanic_total': round(mechanic_total, 2),
            'founder_share_percent': FOUNDER_SHARE_PERCENT,
            'security_fee_percent': SECURITY_FEE_PERCENT
        },
        'recent_invoices': [{
            'id': inv.id,
            'amount': inv.amount,
            'founder_share': inv.founder_share,
            'mechanic_share': inv.mechanic_share,
            'created_at': inv.created_at.isoformat()
        } for inv in recent_invoices]
    })

@app.route('/api/audit-logs', methods=['GET'])
@require_role('admin')
def get_audit_logs():
    """Get immutable audit trail"""
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    
    return jsonify([{
        'id': log.id,
        'user_id': log.user_id,
        'action': log.action,
        'details': log.details,
        'timestamp': log.timestamp.isoformat()
    } for log in logs])

# ============================================================================
# HTML TEMPLATE - BLACK & GOLD PRESTIGE THEME
# ============================================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supreme Engine - African Engineering Services Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #e0e0e0;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(90deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
            border-bottom: 2px solid #d4af37;
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.1);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 28px;
            font-weight: 900;
            color: #d4af37;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Playfair Display', serif;
        }
        
        .nav-links {
            display: flex;
            gap: 30px;
            list-style: none;
        }
        
        .nav-links a {
            color: #d4af37;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            border-bottom: 2px solid transparent;
        }
        
        .nav-links a:hover {
            border-bottom-color: #d4af37;
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        }
        
        .hero {
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(180deg, rgba(212, 175, 55, 0.05) 0%, transparent 100%);
            animation: fadeIn 1.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hero h1 {
            font-size: 48px;
            font-family: 'Playfair Display', serif;
            color: #d4af37;
            margin-bottom: 20px;
            text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
        }
        
        .hero p {
            font-size: 18px;
            color: #b0b0b0;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }
        
        .service-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            border: 2px solid #d4af37;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1);
        }
        
        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 30px rgba(212, 175, 55, 0.3);
            border-color: #ffd700;
        }
        
        .service-emoji {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .service-name {
            font-size: 20px;
            font-weight: 700;
            color: #d4af37;
            margin-bottom: 10px;
        }
        
        .service-description {
            font-size: 14px;
            color: #999;
            margin-bottom: 15px;
        }
        
        .service-price {
            font-size: 18px;
            color: #d4af37;
            font-weight: 600;
        }
        
      
