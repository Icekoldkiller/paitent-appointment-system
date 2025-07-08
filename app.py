from flask import Flask,redirect,render_template,request,session,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'
db = SQLAlchemy(app)

class Appointment(db.Model):
              id = db.Column(db.Integer,primary_key=True)
              patient_name = db.Column(db.String(200),nullable=False)
              doctor = db.Column(db.String(200),nullable=False)
              date = db.Column(db.String(200),nullable=False)
              time = db.Column(db.String(200),nullable=False)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/doctors')
def doctors():
    doctor_list = ['Dr. Aisha Ali', 'Dr. John Doe', 'Dr. Wangari Kariuki']
    return render_template('doctors.html', doctors=doctor_list)

@app.route('/book', methods=['GET', 'POST'])
def book():
    doctor_list = ['Dr. Aisha Ali', 'Dr. John Doe', 'Dr. Wangari Kariuki']
    if request.method == 'POST':
        name = request.form['name']
        doctor = request.form['doctor']
        date = request.form['date']
        time = request.form['time']

        if not name or not date or not time:
            return "Please fill in all the fields."

        new_appointment = Appointment(
            patient_name=name,
            doctor=doctor,
            date=date,
            time=time
        )
        db.session.add(new_appointment)
        db.session.commit()
        return redirect('/')

    return render_template('book.html', doctors=doctor_list)

@app.route('/admin')
def admin():
    all_appointments = Appointment.query.order_by(Appointment.date).all()
    return render_template('admin.html', appointments=all_appointments)

@app.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        session['doctor_name'] = doctor_name
        return redirect('/doctor-dashboard')
    return render_template('doctor_login.html')

@app.route('/doctor-dashboard')
def doctor_dashboard():
    if 'doctor_name' not in session:
        return redirect('/doctor-login')
    
    doctor_name = session['doctor_name']
    appointments = Appointment.query.filter_by(doctor=doctor_name).order_by(Appointment.date).all()
    return render_template('doctor_dashboard.html', doctor=doctor_name, appointments=appointments)

@app.route('/logout')
def logout():
    session.pop('doctor_name', None)
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    



