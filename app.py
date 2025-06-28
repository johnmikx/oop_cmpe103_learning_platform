"""
Simplified Flask Application for OOP Learning Platform
Focus on study guides using Pareto Principle
"""

from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'oop_study_guides_2024')

@app.route('/')
def index():
    """Main dashboard showing study guides"""
    return render_template('index.html')

@app.route('/encapsulation-guide')
def encapsulation_guide():
    """Encapsulation study guide"""
    return render_template('encapsulation-guide.html')

@app.route('/inheritance-guide')
def inheritance_guide():
    """Inheritance study guide"""
    return render_template('inheritance-guide.html')

@app.route('/polymorphism-guide')
def polymorphism_guide():
    """Polymorphism study guide"""
    return render_template('polymorphism-guide.html')

@app.route('/abstraction-guide')
def abstraction_guide():
    """Abstraction study guide"""
    return render_template('abstraction-guide.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'OOP Learning Platform is running',
        'guides': ['encapsulation', 'inheritance', 'polymorphism', 'abstraction']
    }

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting OOP Learning Platform on port {port}")
    print("Focus: Study Guides with 80/20 Pareto Principle")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
