
from flask import Flask,request,render_template,redirect,url_for,session,flash
from forms import RegisterForm,LoginForm,ForgotPassword,VerifyCode,PasswordChange
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import random,string
from flask_mail import Mail, Message

app = Flask(__name__)
app.debug=True

# Mysql
app.config["MYSQL_HOST"] = '127.0.0.1'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'atria_db'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'
mysql = MySQL(app)

#mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'noreply.ait.ise@gmail.com'
app.config['MAIL_PASSWORD'] = 'webdevatriaise!@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Home
@app.route("/",methods=['POST','GET'])
def index():
    form = LoginForm()
    if(request.method=="POST" and form.validate()):
        usn = request.form['usn']
        password_user = request.form['password']
        cur = mysql.connection.cursor()
        result=cur.execute("select * from users where usn = '%s'"%(usn))
        if(result>0):
            data=cur.fetchone()
            password_actual=data['password']
            email_verified = data['email_verified']
            if(email_verified==0):
                flash('Your Email ID is not verified. Please check your email and verify first','danger')
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('EmailVerify',email=data['email']))
            elif(sha256_crypt.verify(password_user, password_actual)):
                mysql.connection.commit()
                cur.close()
                return redirect(url_for("study_materials"))
            else:
                flash("Wrong Password","danger")
                mysql.connection.commit()
                cur.close()
                return redirect(url_for("index"))
        else:
            flash("Invalid user creditials. User not found or invalid USN","danger")
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("index"))
        mysql.connection.commit()
        cur.close()

    return render_template("index.html",form=form)

# Register
@app.route("/register",methods=['POST','GET'])
def register():
    form = RegisterForm()
    if(request.method=='POST'and form.validate() ):
        name = form.name.data
        email= form.email.data
        usn = form.usn.data
        password = sha256_crypt.hash(form.password.data)
        cur = mysql.connection.cursor()
        cur.execute("insert into users(username,email,usn,password) values('%s','%s','%s','%s')"%(name,email,usn,password))
        mysql.connection.commit()
        verify_code = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(10))
        msg = Message('Verification Code', sender = 'noreply.ait.ise@gmail.com', recipients = [email])
        msg.body = "Hello your Email verification code for Atris ISE Dept. website is "+verify_code
        mail.send(msg)
        cur.execute("UPDATE users set verification_code = '%s' where email = '%s' "%(verify_code,email))
        cur.execute("UPDATE users set verification_time = current_timestamp where email = '%s' "%(email))
        mysql.connection.commit()
        cur.close()
        flash("Registered Successfully. Please verify your email before you login","success")

        return redirect(url_for("EmailVerify",email=email))
   
    return render_template("register.html",form=form)
    

# Clubs
@app.route("/clubs")
def clubs():
    return render_template("clubs.html")

# About 
@app.route("/#section-2",methods=['POST','GET'])
def about():
    form = LoginForm()
    if(request.method=="POST" and form.validate()):
        usn = request.form['usn']
        password_user = request.form['password']
        cur = mysql.connection.cursor()
        result=cur.execute("select * from users where usn = '%s'"%(usn))
        if(result>0):
            data=cur.fetchone()
            password_actual=data['password']
            if(sha256_crypt.verify(password_user, password_actual)):
                mysql.connection.commit()
                scur.close()
                return redirect(url_for("study_materials"))
            else:
                flash("Wrong Password","danger")
                mysql.connection.commit()
                cur.close()
                return redirect(url_for("index"))
        else:
            flash("Invalid user creditials. User not found or invalid USN","danger")
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("index"))
    mysql.connection.commit()
    cur.close()

    return render_template("index.html#section-2",form=form)

# Forgot password
@app.route("/forgot",methods=['POST','GET'])
def forgot():
    form=ForgotPassword()
    if(request.method=='POST' and form.validate()):
        email =request.form['email']
        
        cur = mysql.connection.cursor()
        result=cur.execute("select * from users where email = '%s'"%(email))
        if(result>0):
            verify_code = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(10))
            msg = Message('Verification Code', sender = 'noreply.ait.ise@gmail.com', recipients = [email])
            msg.body = "Hello your verification code for Atris ISE Dept. website is "+verify_code
            mail.send(msg)
            cur.execute("UPDATE users set verification_code = '%s' where email = '%s' "%(verify_code,email))
            cur.execute("UPDATE users set verification_time = current_timestamp where email = '%s' "%(email))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('verify',email = email))
        else:
            flash("Entered Email ID doesnot belong to any user.","danger")
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("forgot"))

        # Connection closing
        mysql.connection.commit()
        cur.close()

    
    return render_template("forgot-password.html",form=form)

# Verify code and validate time 
@app.route("/verify/<email>",methods=['POST','GET'])
def verify(email):
    form=VerifyCode()
    if(request.method=='POST' and form.validate()):
        code = request.form['code']
        cur = mysql.connection.cursor()
        result= cur.execute("select * from users where TIMESTAMPDIFF(minute,users.verification_time,CURRENT_TIMESTAMP)<=120 and email = '%s'"%(email))
        if(result>0):
            data=cur.fetchone()
            actual_code = data['verification_code'] 
            if(str(actual_code)==str(code)):
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('change_password',email=email))
            else:
                flash("Verification code doesnot match","danger")
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('verify',email = email,form=form))

        else:
            flash("Verification code has expired or not generated","danger")
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('forgot'))
        mysql.connection.commit()
        cur.close()
    return render_template('verify.html',email=email,form=VerifyCode())

# Change password
@app.route('/change_password/<email>',methods=['POST','GET'])
def change_password(email):
    form = PasswordChange()
    if(request.method=='POST' and form.validate()):
        
        password = sha256_crypt.hash(form.password.data)
        cur = mysql.connection.cursor()
        cur.execute("update users SET users.password = '%s' WHERE users.email='%s'"%(password,email))
        flash("Password changed successfully.","success")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('password_change.html',form=form,email=email)

# After register verify email
@app.route('/EmailVerify/<email>',methods=['POST','GET'])
def EmailVerify(email):
    form = VerifyCode()
    if(request.method=='POST' and form.validate()):
        code = request.form['code']
        cur = mysql.connection.cursor()
        result= cur.execute("select * from users where TIMESTAMPDIFF(minute,users.verification_time,CURRENT_TIMESTAMP)<=360 and email = '%s'"%(email))
        if(result>0):
            data=cur.fetchone()
            actual_code = data['verification_code'] 
            if(str(actual_code)==str(code)):
                flash("Email Verified successfully","success")
                cur.execute("update users set email_verified = 1 where email = '%s'"%(email))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for("index"))
            else:
                flash("Verification code doesnot match","danger")
                return redirect(url_for('EmailVerify',email = email,form=form))

        else:
            flash("Verification code has expired please register again","danger")
            return redirect(url_for('register'))
        mysql.connection.commit()
        cur.close()
    return render_template('verify.html',email=email,form=VerifyCode())

# Study materials
@app.route('/study_materials')
def study_materials():
    return render_template('study_materials.html')


if(__name__ == '__main__'):
    app.secret_key='?\x01\xa7\xe4\x9c$\xd2\xcc,\xfdq-\xe1\xbb\x11.\xfdy~\x1c\xc6w\xbc}\xba'
    app.run()