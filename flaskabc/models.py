#from datetime import datetime
from flaskabc import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

'''
class Cc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<Cc %r>' % (self.date)
'''


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Transaction %r>' % (self.service)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    bname = db.Column(db.String(100), nullable=False)
    bacc = db.Column(db.String(100), nullable=False)
    ifsc = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    dsgn = db.Column(db.String(100), nullable=False)
    inst = db.Column(db.String(100), nullable=False)
    basic_pay = db.Column(db.String(100), nullable=True)
    id_no = db.Column(db.String(100), nullable=False)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)


class Telephone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    emp_id = db.Column(db.String, nullable=False)
    bill = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    month = db.Column(db.String(100), nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    account = db.Column(db.Integer, nullable=False)
    ifsc = db.Column(db.String(100), nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Telephone %r>' % (self.name)


class Travel_allw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    basic_pay = db.Column(db.Integer, nullable=False)
    d_o_j1 = db.Column(db.String(100), nullable=False)
    d_o_j2 = db.Column(db.String(100), nullable=False)
    p_o_j = db.Column(db.String(100), nullable=False)
    s_no = db.Column(db.String(100), nullable=False)
    c_o_j = db.Column(db.String(100), nullable=False)
    e_o_f = db.Column(db.String(100), nullable=False)
    acc_chrg = db.Column(db.String(100), nullable=False)
    exp = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    add_req = db.Column(db.String(100), nullable=False)
    ta_no = db.Column(db.String(100), nullable=False)
    ta_ad = db.Column(db.String(100), nullable=False)
    rup = db.Column(db.String(100), nullable=False)
    b_name = db.Column(db.String(100), nullable=False)
    b_acc = db.Column(db.String(100), nullable=False)
    ifsc = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Travel_allw %r>' % (self.name)


class Contingent(db.Model):
    __tablename__ = 'contingent'
    id = db.Column(db.Integer, primary_key=True)
    curr_date = db.Column(db.String(100), nullable=False)
    station = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    bankbranch = db.Column(db.String(100), nullable=False)
    acc_num = db.Column(db.String(100), nullable=False)
    ifsc = db.Column(db.String(100), nullable=False)
    pets = db.relationship('Contingent_a')

    def __repr__(self):
        return '<Contigent %r>' % (self.name)


class Contingent_a(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt1 = db.Column(db.String(100), nullable=False)
    des1 = db.Column(db.String(100), nullable=False)
    amt1 = db.Column(db.Integer, nullable=False)
    contingent_id = db.Column(db.Integer, db.ForeignKey('contingent.id'))



class Tab(db.Model):
    __tablename__ = 'tab'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    srn = db.Column(db.String(100), nullable=False)
    dsgn = db.Column(db.String(100), nullable=False)
    dpt = db.Column(db.String(100), nullable=False)
    inst = db.Column(db.String(100), nullable=False)
    bp = db.Column(db.Integer, nullable=True)
    ipac = db.Column(db.String(100), nullable=False)
    poj = db.Column(db.String(100), nullable=False)
    enc = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    #amt44 = db.Column(db.Integer, nullable=False)
    #amt55 = db.Column(db.Integer, nullable=False)
    #AB = db.Column(db.Integer, nullable=False)
    advdrawn = db.Column(db.Integer, nullable=False)
    #netclaimed = db.Column(db.Integer, nullable=False)
    #excesspaid = db.Column(db.Integer, nullable=False)
    #excessrecovered = db.Column(db.Integer, nullable=False)
    bankname = db.Column(db.String(100), nullable=False)
    accno = db.Column(db.String(100), nullable=False)
    ifsc = db.Column(db.String(100), nullable=False)
    pets1 = db.relationship('Tab_a')
    pets2 = db.relationship('Tab_b')



class Tab_a(db.Model):
    __tablename__ = 'tab_a'
    id = db.Column(db.Integer, primary_key = True)
    ds = db.Column(db.String(100), nullable=False)
    dd = db.Column(db.String(100), nullable=False)
    dtym = db.Column(db.String(100), nullable=False)
    arst = db.Column(db.String(100), nullable=False)
    ad = db.Column(db.String(100), nullable=False)
    atym = db.Column(db.String(100), nullable=False)
    moj = db.Column(db.String(100), nullable=False)
    jc = db.Column(db.String(100), nullable=False)
    road = db.Column(db.Integer, nullable=False)
    tktno = db.Column(db.String(100), nullable=False)
    fare = db.Column(db.Integer, nullable=False)
    tab_id = db.Column(db.Integer, db.ForeignKey('tab.id'))



class Tab_b(db.Model):
    __tablename__ = 'tab_b'
    id = db.Column(db.Integer, primary_key = True)
    exp = db.Column(db.String(100), nullable=False)
    amt22 = db.Column(db.Integer, nullable=False)
    bill = db.Column(db.String(100), nullable=False)
    tab_id = db.Column(db.Integer, db.ForeignKey('tab.id'))



class Reim(db.Model):
    __tablename__ = 'reim'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    dpt = db.Column(db.String(100), nullable=False)
    #net_claimed = db.Column(db.String(100), nullable=False)
    #amt2 = db.Column(db.Integer, nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    acc_no = db.Column(db.String(100), nullable=False)
    ifsc = db.Column(db.String(100), nullable=False)
    pets = db.relationship('Reim_det')


class Reim_det(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(100), nullable=False)
    cash_no = db.Column(db.String(100), nullable=False)
    firm = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    amt = db.Column(db.Integer, nullable=False)
    reim_id = db.Column(db.Integer, db.ForeignKey('reim.id'))
