from curses import flash
import dbm
import io
from xml.dom.minidom import Document
from flask import Flask, abort, render_template, request, redirect, send_file, url_for, session
from flask_login import current_user, login_required
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import render_template, redirect, url_for, flash, request, send_file, abort
from flask_login import login_user, logout_user, login_required, current_user
from website.models import User, Document
from website.forms import LoginForm, RegistrationForm, UploadForm, VerifyForm
from website.encryption import encrypt_document
from website.qr_code import generate_qr_code, decode_qr_code
from website.utils import save_uploaded_document, add_qr_code_to_document
import io
from website.encryption import encrypt_document
from website.qr_code import decode_qr_code, generate_qr_code
from website.utils import add_qr_code_to_document, save_uploaded_document
from website import app, db
from . import app  
  

  
mysql = MySQL(app)
app.route('/')
def index():
    return  render_template('index.html',)
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'familyname' in request.form and 'password1' in request.form and 'email' in request.form and 'firstname' in request.form and 'adress' in request.form and 'phone' in request.form  :
        familyname = request.form['familyname']
        password1 = request.form['password1']
        email = request.form['email']
        firstname = request.form['firstname']
        adress = request.form['adress']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not phone or not adress or not email or not firstname or not password1 or not familyname:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s, % s, % s)', (familyname, email, password1, firstname, adress, phone, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('signin.html', mesage = mesage)


@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password1' in request.form:
        email = request.form['email']
        password1 = request.form['password1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password1 = % s', (email, password1, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['familyname'] = user['name']
            session['email'] = user['email']
            session['firstname'] = user['firstname']
            session['adress'] = user['adress']
            session['phone'] = user['phone']

            mesage = 'Logged in successfully !'
            return render_template('signer.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('signin.html', mesage = mesage)
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        document = form.document.data
        document_filename = save_uploaded_document(document)
        encrypted_data = encrypt_document(document_filename)

        doc = Document(name=document_filename, encrypted_data=encrypted_data, email_id=current_user.id)
        db.session.add(doc)
        db.session.commit()

        qr_code_img = generate_qr_code(encrypted_data)
        qr_code_filename = f"qr_code_{doc.id}.png"
        qr_code_img.save(f"website/static/img/{qr_code_filename}")

        flash('QR code generated successfully!')
        return render_template('upload.html', form=form, qr_code=qr_code_filename)
    return render_template('upload.html', form=form)

@app.route('/download/<document_id>')
@login_required
def download(document_id):
    doc = Document.query.get_or_404(document_id)
    if doc.email_id != current_user.id:
        abort(403)

    qr_code_filename = f"qr_code_{doc.id}.png"
    qr_code_path = f"app/static/img/{qr_code_filename}"
    document_with_qr = add_qr_code_to_document(doc.name, qr_code_path)

    return send_file(
        io.BytesIO(document_with_qr),
        attachment_filename=f"{doc.name}_with_qr.pdf",
        mimetype='application/pdf',
        as_attachment=True
    )

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form = VerifyForm()
    if form.validate_on_submit():
        document = form.document.data
        document_filename = save_uploaded_document(document, temporary=True)
        qr_code_data = decode_qr_code(document_filename)

        if qr_code_data:
            encrypted_doc = Document.query.filter_by(encrypted_data=qr_code_data).first()
            if encrypted_doc:
                flash('The document is valid and the QR code matches the uploaded document.', 'success')
            else:
                flash('The QR code is not associated with any document in our database.', 'error')
        else:
            flash('No valid QR code found on the uploaded document.', 'error')

        # Clean up the temporary uploaded document
        # os.remove(document_filename)

        return render_template('verify.html', form=form)

 
