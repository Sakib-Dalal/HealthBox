from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# Import your forms from the forms.py
from forms import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Create Database
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Create Table in database
class User(UserMixin, db.Model):
    __tablename__ =  "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    device: Mapped[str] = mapped_column(String(250), nullable=True)
    device_API: Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()


# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Check stored password hash against entered password hashed.
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('userpage'))

    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            # User already exists
            flash("You've already signed up with that email, login instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            email = request.form.get('email'),
            password = hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        # Can redirect() and get name from the current_user
        return redirect(url_for('userpage'))
    return render_template('register.html')

# About Us Page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# Features Page
@app.route('/features')
def features():
    return render_template('features.html')

# Users Main Page
@app.route('/userpage')
@login_required
def userpage():
    print(current_user.email)
    print(current_user.device)
    print(current_user.device_API)
    # Passing the name from the current_user
    return render_template('userpage.html', name=current_user.email, device=current_user.device, device_API=current_user.device_API)

# add new device page
@app.route(f'/new_device/<email>')
@login_required
def new_device(email):
    return render_template('new_device.html', email=email)



# Logout Page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
