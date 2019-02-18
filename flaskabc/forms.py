from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField,IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, Email, EqualTo
from wtforms import StringField, PasswordField, BooleanField
#from flask_bootstrap import Bootstrap
from wtforms.fields.html5 import DateField, TimeField
from flaskabc.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    bname = StringField('Bank Name & Branch', validators=[DataRequired()])
    bacc = StringField('Bank Account Number', validators=[DataRequired()])
    ifsc = StringField('IFSC Code', validators=[DataRequired()])
    dept = StringField('Department', validators=[DataRequired()])
    dsgn = StringField('Designation', validators=[DataRequired()])
    inst = StringField('Institute', validators=[DataRequired()])
    basic_pay = StringField('Basic Pay (Rs.)')
    id_no = StringField('Roll No./ID', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class CcForm(FlaskForm):
    date = DateField(format='%Y-%m-%d')

class TransactionForm(FlaskForm):
    service = StringField('Service', validators=[DataRequired()])
    provider = StringField('Provider', validators=[DataRequired()])
    date = DateField(format='%Y-%m-%d')
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class TelephoneForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    emp_id = StringField('Employee ID', validators=[DataRequired()])
    bill = IntegerField('Bill Amount', validators=[DataRequired()])
    date = DateField(id='datepick',format='%Y-%m-%d')
    month = SelectField('Select-Month',choices = [('January','January'),('February','February'),('March','March'),('April','April'),('May','May'),('June','June'),('July','July'),('August','August'),('September','September'),('October','October'),('November','November'),('December','December')] ,validators=[DataRequired()])
    bank = StringField('Bank Name and Branch', validators=[DataRequired()])
    account = IntegerField('Account Number', validators=[DataRequired()])
    ifsc = StringField('IFSC Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Travel_allwForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    basic_pay = IntegerField('Basic Pay', validators=[DataRequired()])
    d_o_j1 = DateField('Date of Journey 1(from)', format='%Y-%m-%d')
    d_o_j2 = DateField('Date of Journey 2(to)', format='%Y-%m-%d')
    p_o_j = StringField('Purpose of journey', validators=[DataRequired()])
    s_no = StringField('Staff/Roll number', validators=[DataRequired()])
    c_o_j = StringField('Proposed class of journey', validators=[DataRequired()])
    e_o_f = StringField('Estimate of fare(one-way or two-way)', validators=[DataRequired()])
    acc_chrg = StringField('Accomodation Charges', validators=[DataRequired()])
    exp = StringField('Other Expenditures', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    add_req = StringField('Total Advance Requested', validators=[DataRequired()])
    ta_no = StringField('T A No.', validators=[DataRequired()])
    ta_ad = StringField('Approved TA advance of Rs.', validators=[DataRequired()])
    rup = StringField('Ruppes(in words)', validators=[DataRequired()])
    b_name = StringField('Bank Name & Branch', validators=[DataRequired()])
    b_acc = StringField('Bank Account Number', validators=[DataRequired()])
    ifsc = StringField('IFSC Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ContingentForm(FlaskForm):
    curr_date = DateField('Date',format='%Y-%m-%d')
    station = StringField('Station', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    bankbranch = StringField('Bank Name & Branch', validators=[DataRequired()])
    acc_num = StringField('Bank Account Number', validators=[DataRequired()])
    ifsc = StringField('IFSC Code', validators=[DataRequired()])
    submit = SubmitField('Submit')



class Contingent_aForm(FlaskForm):
    dt1 = DateField('Date 1',format='%Y-%m-%d', validators=[DataRequired()])
    des1 = StringField('Destination 1', validators=[DataRequired()])
    amt1 = IntegerField('Amount 1', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReimburseForm(FlaskForm):
    date = DateField(format='%d/%m/%Y')
    cash = IntegerField('Cash', validators=[DataRequired()])
    firm = StringField('Firm', validators=[DataRequired()])
    purpose = StringField('Purpose', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TabForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    srn = StringField('Staff No./ Roll No:', validators=[DataRequired()])
    dsgn = StringField('Designation', validators=[DataRequired()])
    dpt = StringField('Department', validators=[DataRequired()])
    inst = StringField('Institute', validators=[DataRequired()])
    bp = IntegerField('Basic Pay Rs')
    ipac = StringField('Institute Account/Project Account No.', validators=[DataRequired()])
    poj = StringField('Purpose of Journey', validators=[DataRequired()])
    enc = IntegerField('No. of Enclosures', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d')
    #amt44 = IntegerField('Total Amount Admissible (A)', validators=[DataRequired()])
    #amt55 = IntegerField('Total Amount Admissible (B)', validators=[DataRequired()])
    #AB = IntegerField('A + B', validators=[DataRequired()])
    advdrawn = IntegerField('Advance Draw (C)', validators=[DataRequired()])
    #netclaimed = IntegerField('Net Claim Admissible (A+B-C)', validators=[DataRequired()])
    #excesspaid = IntegerField('Excess to be paid by IITH', validators=[DataRequired()])
    #excessrecovered = IntegerField('Excess to be recovered by IITH', validators=[DataRequired()])
    bankname = StringField('Bank Name & Branch', validators=[DataRequired()])
    accno = StringField('Account No.', validators=[DataRequired()])
    ifsc = StringField('IFSC Code', validators=[DataRequired()])
    submit = SubmitField('Submit')



class Tab_aForm(FlaskForm):
    ds = StringField('Station (departure)', validators=[DataRequired()])
    dd = DateField('Date (departure)', format='%Y-%m-%d')
    dtym = TimeField('Hour (departure)', format='%H:%M',validators=[DataRequired()])
    arst = StringField('Station (Arrival)', validators=[DataRequired()])
    ad = DateField('Date (Arrival)', format='%Y-%m-%d')
    atym = TimeField('Hour (Arrival)',format='%H:%M', validators=[DataRequired()])
    moj = SelectField('Mode of Journey(rail/air/road)',choices = [('rail','Rail'),('air','Air'),('road','Road')] ,validators=[DataRequired()])
    jc = StringField('Class', validators=[DataRequired()])
    road = IntegerField('Road (kms)', validators=[DataRequired()])
    tktno = StringField('Flight/Train Ticket no.', validators=[DataRequired()])
    fare = IntegerField('Fare(Rs.)', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Tab_bForm(FlaskForm):
    exp = StringField('Item of Expenditure', validators=[DataRequired()])
    amt22 = IntegerField('Amount (Rs.)', validators=[DataRequired()])
    bill = StringField('Cash Bill Details', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReimForm(FlaskForm):
    name = StringField('Name of the faculty/staff', validators=[DataRequired()])
    dpt = StringField('Department', validators=[DataRequired()])
    #net_claimed = IntegerField('Net Claimed', validators=[DataRequired()])
    #amt2 = IntegerField('Aprroved Expenditure for Reimbursement (Rs)', validators=[DataRequired()])
    bank = StringField('Bank Name & Branch', validators=[DataRequired()])
    acc_no = StringField('Account Number', validators=[DataRequired()])
    ifsc = StringField('IFSC Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Reim_detForm(FlaskForm):
    date = DateField('Date',format='%Y-%m-%d')
    cash_no = StringField('Cash Memo No.', validators=[DataRequired()])
    firm = StringField('Name of the Firm', validators=[DataRequired()])
    purpose = StringField('Purpose', validators=[DataRequired()])
    amt = IntegerField('Amount (Rs.)', validators=[DataRequired()])
    submit = SubmitField('Submit')