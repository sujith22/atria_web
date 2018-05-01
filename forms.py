from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField

from wtforms import validators

class RegisterForm(FlaskForm):
    name = StringField("Name",[validators.Required("Please enter your name"),validators.Length(min=2,max=50)],render_kw={"placeholder": "John Andreson"})
    email = StringField("Email",[validators.Required("Enter Your Email ID"),validators.Email("Enter a Proper Mail ID")],render_kw={"placeholder": "John@email.com"})
    usn = StringField("USN",[validators.Required("Enter Your USN (All in capitals)"),validators.Length(min=5,max=50)],render_kw={"placeholder": "1AT15IS092"})
    password = PasswordField("Password",[validators.InputRequired("Enter a password"),validators.EqualTo("Confirm",message="Password Not Matching")],render_kw={"placeholder": "Password"})
    Confirm = PasswordField("Confirm Password",[validators.DataRequired("Enter Password again to confirm")],render_kw={"placeholder": "Confirm Password"})
    
class LoginForm(FlaskForm):
    usn = StringField("USN",[validators.DataRequired()],render_kw={"placeholder": "1AT15IS092"})
    password = PasswordField("Password",[validators.DataRequired()],render_kw={"placeholder": "Password"})

class ForgotPassword(FlaskForm):
    email = StringField("Email",[validators.Required("Enter Your Email ID"),validators.Email("Enter a Proper Mail ID")],render_kw={"placeholder": "John@email.com"})

class VerifyCode(FlaskForm):
    code = StringField("Code",[validators.Required("Please enter the code"),validators.Length(min=10,max=10)])

class PasswordChange(FlaskForm):
    password = PasswordField("Password",[validators.InputRequired("Enter a password"),validators.EqualTo("Confirm",message="Password Not Matching")],render_kw={"placeholder": "Password"})
    Confirm = PasswordField("Confirm Password",[validators.DataRequired("Enter Password again to confirm")],render_kw={"placeholder": "Confirm Password"})

class EmailVerification(FlaskForm):
    code = StringField("Code",[validators.Required("Please enter the code"),validators.Length(min=10,max=10)])