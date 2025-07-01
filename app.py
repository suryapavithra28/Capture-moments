from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------- Updated Photographers with All Specializations ----------
photographers = [
    {"id": "p1", "name": "Amit Lensman", "skills": ["Wedding", "Little Ones", "Nature", "Architecture", "Pre-Wedding"], "image": "amit.jpg"},
    {"id": "p2", "name": "Sana Clickz", "skills": ["Fashion", "Event", "Maternity", "Portrait", "Food"], "image": "sana.jpg"},
    {"id": "p3", "name": "Markus", "skills": ["Fashion", "Little Ones", "Event", "Street", "Aerial"], "image": "Markus.jpg"},
    {"id": "p4", "name": "Smitha", "skills": ["Fashion", "Little Ones", "Maternity", "Wildlife", "Pre-Wedding"], "image": "smitha.jpg"},
    {"id": "p5", "name": "Vikas", "skills": ["Wedding", "Fashion", "Portrait", "Architecture", "Documentary"], "image": "vikas.jpg"},
    {"id": "p6", "name": "Sravs", "skills": ["Event", "Little Ones", "Landscape", "Nature"], "image": "sravs.jpg"},
    {"id": "p7", "name": "Pavi", "skills": ["Wedding", "Little Ones", "Pre-Wedding", "Wildlife"], "image": "pavi.jpg"},
    {"id": "p8", "name": "Ayan", "skills": ["Wedding", "Event", "Street", "Aerial", "Documentary"], "image": "Ayan.jpg"},
]

availability_data = {
    "p1": ["2025-06-20", "2025-06-23"],
    "p2": ["2025-06-19", "2025-06-22"],
    "p3": ["2025-06-18", "2025-06-21"],
    "p4": ["2025-06-17", "2025-06-20"],
    "p5": ["2025-06-16", "2025-06-19"],
    "p6": ["2025-06-15", "2025-06-18"],
    "p7": ["2025-06-14", "2025-06-17"],
    "p8": ["2025-06-13", "2025-06-16"],
}

# ---------- Helper Functions ----------
USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def find_user(username_or_email):
    users = load_users()
    return next((u for u in users if u['username'] == username_or_email or u['email'] == username_or_email), None)

# ---------- Auth Routes ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']

        user = find_user(username_or_email)
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if find_user(username) or find_user(email):
            flash('User already exists.', 'error')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        users = load_users()
        users.append({'username': username, 'email': email, 'password': hashed_pw})
        save_users(users)

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

# ---------- Core Routes ----------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        user_id = request.form.get('user_id')
        date = request.form.get('date')
        return f"<h2 style='color:green'>Booking Confirmed! For {photographer_id} on {date}.</h2>"
    return render_template('book.html')

@app.route('/show-photographers')
def show_photographers():
    return render_template('photographers.html', photographers=photographers, availability_data=availability_data)

# ---------- Photography Specialization Routes ----------
@app.route('/wedding')
def wedding():
    return render_template('wedding.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/fashion')
def fashion():
    return render_template('fashion.html')

@app.route('/little ones')
def littleones():
    return render_template('little ones.html')

@app.route('/maternity')
def maternity():
    return render_template('maternity.html')

@app.route('/nature')
def nature():
    return render_template('nature.html')

@app.route('/wildlife')
def wildlife():
    return render_template('wildlife.html') 

@app.route('/street')
def street_photography():
    return render_template('street.html')

@app.route('/portrait')
def portrait_photography():
    return render_template('portrait.html')

@app.route('/documentary')
def documentary():
    return render_template('documentary.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/architecture')
def architecture_photography():
    return render_template('architecture.html')

@app.route('/landscape')
def landscape_photography():
    return render_template('landscape.html')

@app.route('/aerial')
def aerial_photography():
    return render_template('aerial.html')

@app.route('/prewedding')
def prewedding():
    return render_template('prewedding.html')
@app.route('/book', methods=['GET'])
def book_photographer():
    design = request.args.get('design')  # optional: pass design type
    return render_template('book.html', design=design)




if __name__ == '__main__':
    app.run(debug=True)
