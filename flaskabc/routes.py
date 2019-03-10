import os
#import secrets
import xlsxwriter
from flask import Flask, render_template, url_for, flash, redirect, request, abort, send_file, send_from_directory, Blueprint
from flaskabc import app, db
from flaskabc.forms import TransactionForm, LoginForm, TelephoneForm, Travel_allwForm, ContingentForm, TabForm, Tab_aForm, Tab_bForm, Contingent_aForm, Reim_detForm, ReimForm, RegistrationForm,Opt_cert_AForm,Opt_cert_BForm,Opt_cert_CForm,Opt_certForm
from flaskabc.models import Transaction, User, Telephone, Contingent, Travel_allw, Tab, Tab_a, Tab_b, Contingent_a, Reim, Reim_det, Opt_cert,Opt_cert_A,Opt_cert_B,Opt_cert_C
from werkzeug import secure_filename
from io import BytesIO
import os
import xlsxwriter
import inflect
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, Email
from datetime import datetime
#from flask_bootstrap import Bootstrap
####################################################################
#from pyPdf2 import PdfFileWriter, PdfFileReader
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4,inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
############################# telephone functions ##################

def getmonth(mo):	
	# print mo, type(mo)
	if mo == "01":
		return "January"
	elif mo == "02":
		return "February"
	elif mo == "03":
		return "March"
	elif mo == "04":
		return "April"
	elif mo == "05":
		return "May"
	elif mo == "06":
		return "June"
	elif mo == "07":
		return "July"
	elif mo == "08":
		return "August"
	elif mo == "09":
		return "Septemeber"
	elif mo == "10":
		return "October"
	elif mo == "11":
		return "November"
	elif mo == "12":
		return "December"
	elif mo == "00":
		return "."


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
global user1

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' :
       return render_template('login.html', form = form)
    username = form.username.data
    password = form.password.data
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid!' , 'danger')
        return render_template(('login.html'),form = form)
    login_user(registered_user)
    flash('Logged in successfully', 'success')
    #user1 = registered_user
    return redirect(request.args.get('next') or url_for('menu'))

    #return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=form.password.data, name = form.name.data,address=form.address.data,bname=form.bname.data,bacc=form.bacc.data,ifsc=form.ifsc.data,dept=form.dept.data,dsgn=form.dsgn.data,inst=form.inst.data,basic_pay=form.basic_pay.data,id_no=form.id_no.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/home")
@login_required
def menu():
    return render_template('mainmenu.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/menu_htmlforms")
@login_required
def menu_htmlforms():
    return render_template('menu_htmlforms.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/<int:tele_id>/all_transactions")
@login_required
def all_transactions(tele_id):
    telephone = Telephone.query.get_or_404(tele_id)
    transactions = telephone.pets
    return render_template('transactions.html', transactions=transactions, telephone = telephone)

'''
@app.route("/delete_transactions")
@login_required
def delete_transactions():
   transactions = Transaction.query.all()
   for transaction in transactions:
      db.session.delete(transaction)
      db.session.commit()
   flash('All transactions have been deleted!', 'success')
   return render_template('menu_htmlforms.html')

@app.route("/transaction/<int:transaction_id>/update", methods=['GET', 'POST'])
@login_required
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    
    form = TransactionForm()
    if form.validate_on_submit():
        transaction.service = form.service.data
        transaction.provider = form.provider.data
        transaction.date = form.date.data
        transaction.amount = form.amount.data
        db.session.commit()
        flash('Your transaction has been updated!', 'success')
        return redirect(url_for('all_transactions'))
    elif request.method == 'GET':
        form.service.data = transaction.service
        form.provider.data = transaction.provider
        form.date.data = datetime.strptime(transaction.date, '%Y-%m-%d')
        form.amount.data = transaction.amount
    return render_template('create_transaction.html',title='Update Transaction',form=form, legend='Update Transaction')


@app.route("/transaction/<int:transaction_id>/delete")
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('all_transactions'))
'''

@app.route("/about")
def about():
    #db.session.add(User(username = 'tlc', password = '1234'))
    #db.session.commit()
    return render_template('about.html', title='About')


@app.route("/transaction/<int:tele_id>/new", methods=['GET', 'POST'])
@login_required
def new_transaction(tele_id):
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(service=form.service.data, provider=form.provider.data, date=form.date.data.strftime('%d/%m/%y'), amount=form.amount.data, tele_id = tele_id)
        db.session.add(transaction)
        db.session.commit()
        flash('Your transaction has been created!', 'success')
        return redirect(url_for('all_telephones'))
    return render_template('create_transaction.html', title='New Transaction',
                           form=form, legend='New Transaction')


@app.route("/transaction/<int:trans_id>/delete_transaction", methods=['GET', 'POST'])
@login_required
def del_transaction(trans_id):
    transaction = Transaction.query.get_or_404(trans_id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('all_telephones'))


@app.route("/<int:tele_id>/download")
@login_required
def download(tele_id):
    telephone = Telephone.query.get_or_404(tele_id)
    transaction_all = telephone.pets
    f_name = str(telephone.id) + '.xlsx'
    #f_name1 = str(telephone.id) + '.pdf'
    workbook = xlsxwriter.Workbook(f_name)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    #bold = workbook.add_format({'bold': True})
    merge_format2 = workbook.add_format({
        'bold': 1,
        'border': 1})
    merge_format3 = workbook.add_format({
        'border': 1})
    merge_format4 = workbook.add_format({
        'border': 1,
        'align': 'left'})
    worksheet.write('A1', 'S.No.', merge_format2)
    worksheet.write('B1', 'Service', merge_format2)
    worksheet.write('C1', 'Provider', merge_format2)
    worksheet.write('D1', 'Date', merge_format2)
    worksheet.write('E1', 'Amount', merge_format2)
    row = 1
    #transaction_all = Transaction.query.all()
    
    total = 0
    for trans in (transaction_all):
        worksheet.write(row, col, row,merge_format4)
        worksheet.write(row, col+1, trans.service,merge_format3)
        worksheet.write(row, col + 2, trans.provider,merge_format3)
        date1 = str(trans.date)
        worksheet.write(row, col + 3,date1,merge_format3)
        w = int(trans.amount)
        total = total + w
        worksheet.write(row, col + 4, w,merge_format3)
        row += 1

    # Write a total using a formula.
    
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'})
    stra = 'B' + str(row+1) + ":D" + str(row+1)
    worksheet.merge_range(stra,'Total',merge_format)
    #worksheet.write('B4:D4', 'Total', bold)
    worksheet.write(row, 4, total,merge_format2)
    workbook.close()
    path2 = os.getcwd() + '/' + f_name
    #path29 = os.getcwd() + '/' + f_name1
    return send_file(path2, attachment_filename=f_name, as_attachment=True)
    


# app = Flask(__name__)
x = ""
def isnum2(num2):
   if num2 == "1" :
      return 1
   if num2 == "2" :
      return 1
   if num2 == "3" :
      return 1
   if num2 == "4" :
      return 1
   if num2 == "5" :
      return 1
   if num2 == "6" :
      return 1
   if num2 == "7" :
      return 1
   if num2 == "8" :
      return 1
   if num2 == "9" :
      return 1   
   if num2 == "0" :
      return 1
   else :
      return 0

@app.route('/upload')
@login_required
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
@login_required
def upload_file1():
   if request.method == 'POST':
      f = request.files['file']
      global x
      x=(f.filename)
      f.save(secure_filename(f.filename))
      return render_template('download_excel.html')
		
@app.route('/download_sheet')
@login_required
def download_excel():
   file = x
   #print (x + "hi")
   file2 = x[:-4] + ".txt"
   file3 = x[:-4] + ".xlsx"
   #path = os.getcwd() + '/' +file
   workbook = xlsxwriter.Workbook(file3)
   worksheet = workbook.add_worksheet()
   row = 0
   #col = 0
   worksheet.write('A1', 'Date')
   worksheet.write('B1', 'Transactional Details')
   worksheet.write('C1', 'Amount')
   worksheet.write('D1','Debit/Credit')
   os.system("pdftotext -layout -l 1 " + file)
   readfrom = open(file2, "r+")
   #strr = ""
   index = 0
   for text in readfrom:
      #print (text)
      date = ""
      transaction = ""
      amount = ""
      dc = ""
      amt1 = ""
      #strr = strr + text
      text=" ".join(text.split())
      index = index + 1
      if (index >= 48) and len(text) > 13:
         if isnum2(text[0]) == 1 and text[2] == ' ':
            date = text[0:10]
            #print (date)	
            length = len(text) -1
            cc = 0
            for i in range(length):
               if isnum2(text[length-2-i]) == 0 and (text[length-2-i]) != ',' and (text[length-2-i]) != '.' :
                  cc = length-2-i
                  break
            amount = text[cc+1:length-1]
            #print (amount)
            transaction = text[10:cc]
            dc = text[length:length+1]
            #print (transaction)
            row += 1
            worksheet.write(row,0, date)
            worksheet.write(row,1, transaction)
            amt1 = amount.replace(",", "")
            #print(dc)
            worksheet.write(row,2, float(amt1))
            worksheet.write(row,3,dc)
            
   workbook.close()
   readfrom.close()  
   print ('check the results.xlsx file')
   path22 = os.getcwd() + '/' + file3
   return send_file(path22, attachment_filename = file3, as_attachment = True)


temp11 = ""
@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    
    if request.method == 'GET':
        return render_template('calc_bkup.html')

    elif request.method == 'POST': 
        global temp11
        if "one" in request.form:
            temp11 = request.form['name']
            result = temp11 + "1" 
        elif "two" in request.form:
            temp11 = request.form['name'] 
            result = temp11 + "2" 
        elif "three" in request.form:
            temp11 = request.form['name']
            result = temp11 + "3"
        elif "four" in request.form:
            temp11 = request.form['name']
            result = temp11 + "4"
        elif "five" in request.form:
            temp11 = request.form['name']
            result = temp11 + "5"
        elif "six" in request.form:
            temp11 = request.form['name']
            result = temp11 + "6"
        elif "seven" in request.form:
            temp11 = request.form['name']
            result = temp11 + "7"
        elif "eight" in request.form:
            temp11 = request.form['name']
            result = temp11 + "8"
        elif "nine" in request.form:
            temp11 = request.form['name']
            result = temp11 + "9"
        elif "zero" in request.form:
            temp11 = request.form['name']
            result = temp11 + "0"
        elif "dot" in request.form:
            temp11 = request.form['name']
            result = temp11 + "."
        elif "cancel" in request.form:
            temp11 = request.form['name']
            result = ""
        elif "plus" in request.form:
            temp11 = request.form['name']
            result = temp11 + "+"
        elif "minus" in request.form:
            temp11 = request.form['name']
            result = temp11 + "-"
        elif "mul" in request.form:
            temp11 = request.form['name']
            result = temp11 + "*"
        elif "slash" in request.form:
            temp11 = request.form['name']
            result = temp11 + "/"
        elif "open" in request.form:
            temp11 = request.form['name']
            result = temp11 + "("
        elif "close" in request.form:
            temp11 = request.form['name']
            result = temp11 + ")" 
        elif "back" in request.form:
            temp11 = request.form['name']
            result = temp11[:-1]
        elif "percentile" in request.form:
            temp11 = request.form['name']
            result = temp11 + "%"
        elif "equals" in request.form:
            temp11 = request.form['name']
            if temp11[-1] == "+" or temp11[-1] == "-" or temp11[-1] == "*" or temp11[-1] == "/" or temp11[0] == "+" or temp11[0] == "-" or temp11[0] == "*" or temp11[0] == "/" or temp11[0] == "%" or temp11[-1] == "%":
                return render_template('calc_bkup2.html', result=temp)
            else :
                result2 = eval(temp11)
                temp11 = str(result2)
                return render_template('calc_bkup.html',  result=result2)

        temp11 = result
        return render_template('calc_bkup.html',  result=result)



@app.route("/all_telephones")
@login_required
def all_telephones():
    telephones = Telephone.query.all()
    return render_template('telephone.html', telephones=telephones)


@app.route("/delete_telephones")
@login_required
def delete_telephones():
   telephones = Telephone.query.all()
   for telephone in telephones:
      db.session.delete(telephone)
      db.session.commit()
   flash('All telephone data has been deleted!', 'success')
   return redirect(url_for('all_telephones'))

@app.route("/telephone/<int:telephone_id>/update", methods=['GET', 'POST'])
@login_required
def update_telephone(telephone_id):
    telephone = Telephone.query.get_or_404(telephone_id)
    
    form = TelephoneForm()
    if form.validate_on_submit():
        telephone.name = form.name.data
        telephone.designation = form.designation.data
        telephone.department = form.department.data
        telephone.emp_id = form.emp_id.data
        #telephone.bill = form.bill.data
        telephone.month = form.month.data
        telephone.date = form.date.data.strftime('%d/%m/%y')
        telephone.bank = form.bank.data
        telephone.account = form.account.data
        telephone.ifsc = form.ifsc.data
        db.session.commit()
        flash('Your telephone entry has been updated!', 'success')
        return redirect(url_for('all_telephones'))
    elif request.method == 'GET':
        form.name.data = telephone.name
        form.designation.data = telephone.designation
        form.department.data = telephone.department
        form.emp_id.data = telephone.emp_id
        #form.bill.data = telephone.bill
        form.month.data = telephone.month
        form.date.data = datetime.strptime(telephone.date, '%d/%m/%y')
        form.bank.data = telephone.bank
        form.account.data = telephone.account
        form.ifsc.data = telephone.ifsc
    return render_template('telephoneform.html',title='Update Telephone Form',form=form, legend='Update Telephone Form')


@app.route("/telephone/<int:telephone_id>/delete")
@login_required
def delete_telephone(telephone_id):
    telephone = Telephone.query.get_or_404(telephone_id)
    db.session.delete(telephone)
    db.session.commit()
    flash('Your telephone entry has been deleted!', 'success')
    return redirect(url_for('all_telephones'))


@app.route("/telephone/new/manual", methods=['GET', 'POST'])
@login_required
def new_telephone():
    form = TelephoneForm()
    if form.validate_on_submit():
        telephone = Telephone(name=form.name.data, designation=form.designation.data, department = form.department.data, emp_id = form.emp_id.data,month=form.month.data, date=form.date.data.strftime('%d/%m/%y'), bank = form.bank.data, account=form.account.data, ifsc = form.ifsc.data)
        db.session.add(telephone)
        db.session.commit()
        flash('Your telephone entry has been created!', 'success')
        return redirect(url_for('all_telephones'))
    return render_template('telephoneform.html', title='New Telephone Form',
                           form=form, legend='New Telephone Form')

@app.route("/telephone/new/default", methods=['GET', 'POST'])
@login_required
def new_telephone_default():
    form = TelephoneForm()
    user_id = current_user.get_id()
    user = User.query.get_or_404(int(user_id))
    form.name.data = user.name
    form.designation.data = user.dsgn
    form.department.data = user.dept
    form.emp_id.data = user.id_no
    form.bank.data = user.bname
    form.account.data = user.bacc
    form.ifsc.data = user.ifsc
    if form.validate_on_submit():
        telephone = Telephone(name=form.name.data, designation=form.designation.data, department = form.department.data, emp_id = form.emp_id.data,month=form.month.data, date=form.date.data.strftime('%d/%m/%y'), bank = form.bank.data, account=form.account.data, ifsc = form.ifsc.data)
        db.session.add(telephone)
        db.session.commit()
        flash('Your telephone entry has been created!', 'success')
        return redirect(url_for('all_telephones'))
    return render_template('telephoneform.html', title='New Telephone Form',
                           form=form, legend='New Telephone Form')



@app.route("/telephone/<int:telephone_id>/download", methods=['GET', 'POST'])
@login_required
def download_telephone(telephone_id):
    telephone = Telephone.query.get_or_404(telephone_id)
    name = telephone.name
    designation = telephone.designation
    department = telephone.department
    id = telephone.emp_id
    month = telephone.month
    date = telephone.date
    bank = telephone.bank
    account = telephone.account
    ifsc = telephone.ifsc
    tele_id = str(telephone.id)
    #createpdf_tele(str(telephone.name),str(telephone.designation),str(telephone.department),str(telephone.emp_id),str(telephone.month),str(telephone.date),str(telephone.bank),str(telephone.account),str(telephone.ifsc),str(telephone.id))
    telephone = Telephone.query.get_or_404(tele_id)
    transactions = telephone.pets
    bill = 0
    for transaction in transactions:
        bill = bill + transaction.amount
    packet = io.BytesIO()
# create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    #can.drawString(10, 100, "Hello world")
    can.setFont("Helvetica", 10) 
    can.drawString(505, 593, str(date))
    can.drawString(397, 480, str(bill))
    
    p = inflect.engine()
    ss = p.number_to_words(bill)
    ss = ss.upper()
    #can.drawString(170, 213, ss)
    if (len(ss)>10):       
        can.drawString(485,480, ss[:10]+'-')
        if(len(ss)>34):
            can.setFont("Helvetica", 7) 
            can.drawString(50,462, ss[10:len(ss)])
            
        else:
            can.drawString(80,462, ss[10:len(ss)])
    
    #month = getmonth(str(date[5])+str(date[6]))
    can.setFont("Helvetica", 10) 
    if(len(month)>10):
        can.drawString(296, 470, month[:10]+'-')
        can.drawString(296,463,month[10:])
    else:
        can.drawString(296, 463, str(month))
    if(len(month)>10):
        can.drawString(236, 453, month[:10]+'-')
        can.drawString(236,445,month[10:])
    else:
        can.drawString(236, 445, str(month))
    can.drawString(482, 372, str(name))
    can.drawString(482, 358, str(designation))
    can.drawString(482, 345, str(department))
    can.drawString(482, 333, str(id))
    can.drawString(230, 296.5, str(bank))
    can.drawString(230, 275, str(account))
    can.drawString(230, 252, str(ifsc))
    can.save()

#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF
    cw = os.getcwd()
    filepath = cw + "/static"
    existing_pdf = PdfFileReader(open((filepath+"/Telephone_Re.pdf"), "rb"))
    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    #output.addPage(page)
    doc = SimpleDocTemplate("simple_table_grid.pdf", pagesize = A4, rightMargin=30,leftMargin=30, topMargin=600,bottomMargin=18)
# container for the 'Flowable' objects
    elements = []
    tele_id = int(tele_id)
    

    data= [['Service', 'Provider', 'Date', 'Amount']]
    for transaction in transactions:
        li = [transaction.service,transaction.provider,str(transaction.date),str(transaction.amount)]
        data.append(li)

    t=Table(data,70, 30)
    t.setStyle(TableStyle([
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
    elements.append(t)
    doc.build(elements)
    existing_pdf2 = PdfFileReader(open((cw+"/simple_table_grid.pdf"), "rb"))
    page2 = existing_pdf2.getPage(0)
    page
    page.mergePage(page2)
    output.addPage(page)
    copy = 0
    outputStream = open(str(tele_id)+'_copy(' +str(copy)+")_tele.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    path21 = os.getcwd() + '/' +str(tele_id)+'_copy(' +str(copy)+")_tele.pdf"
    copy = copy + 1
    return send_file(path21, attachment_filename=str(telephone.id) + "_tele.pdf", as_attachment=True)


###############################################################################################

@app.route("/all_travel_allw")
@login_required
def all_travel_allw():
    travel_allws = Travel_allw.query.all()
    return render_template('travel_allw.html', travel_allws=travel_allws)


@app.route("/delete_travel_allws")
@login_required
def delete_travel_allws():
   travel_allws = Travel_allw.query.all()
   for travel_allw in travel_allws:
      db.session.delete(travel_allw)
      db.session.commit()
   flash('All travel allowance data has been deleted!', 'success')
   return redirect(url_for('all_travel_allw'))

@app.route("/travel_allw/<int:travel_allw_id>/update", methods=['GET', 'POST'])
@login_required
def update_travel_allw(travel_allw_id):
    travel_allw = Travel_allw.query.get_or_404(travel_allw_id)
    
    form = Travel_allwForm()
    if form.validate_on_submit():
        travel_allw.name = form.name.data
        travel_allw.designation = form.designation.data
        travel_allw.department = form.department.data
        travel_allw.basic_pay = form.basic_pay.data
        travel_allw.d_o_j1 = form.d_o_j1.data.strftime('%d/%m/%y')
        travel_allw.d_o_j2 = form.d_o_j2.data.strftime('%d/%m/%y')
        travel_allw.p_o_j = form.p_o_j.data
        travel_allw.s_no = form.s_no.data
        travel_allw.c_o_j = form.c_o_j.data
        travel_allw.e_o_f = form.e_o_f.data
        travel_allw.acc_chrg = form.acc_chrg.data
        travel_allw.exp = form.exp.data
        travel_allw.details = form.details.data
        travel_allw.add_req = form.add_req.data
        travel_allw.ta_no = form.ta_no.data
        travel_allw.ta_ad = form.ta_ad.data
        travel_allw.rup = form.rup.data
        travel_allw.b_name = form.b_name.data
        travel_allw.b_acc = form.b_acc.data
        travel_allw.ifsc = form.ifsc.data
        db.session.commit()
        flash('Your travel allowance form entry has been updated!', 'success')
        return redirect(url_for('all_travel_allw'))
    elif request.method == 'GET':
        form.name.data = travel_allw.name
        form.designation.data = travel_allw.designation
        form.department.data = travel_allw.department
        form.basic_pay.data = travel_allw.basic_pay  
        form.d_o_j1.data = datetime.strptime(travel_allw.d_o_j1, '%d/%m/%y')  
        form.d_o_j2.data = datetime.strptime(travel_allw.d_o_j2, '%d/%m/%y')  
        form.p_o_j.data = travel_allw.p_o_j  
        form.s_no.data = travel_allw.s_no 
        form.c_o_j.data = travel_allw.c_o_j  
        form.e_o_f.data = travel_allw.e_o_f 
        form.acc_chrg.data = travel_allw.acc_chrg 
        form.exp.data = travel_allw.exp 
        form.details.data = travel_allw.details  
        form.add_req.data = travel_allw.add_req  
        form.ta_no.data = travel_allw.ta_no  
        form.ta_ad.data = travel_allw.ta_ad  
        form.rup.data = travel_allw.rup 
        form.b_name.data = travel_allw.b_name  
        form.b_acc.data = travel_allw.b_acc  
        form.ifsc.data = travel_allw.ifsc
    return render_template('travel_allwform.html',title='Update Travel ALlowance Form',form=form, legend='Update Travel Allowance Form')


@app.route("/travel_allw/<int:travel_allw_id>/delete")
@login_required
def delete_travel_allw(travel_allw_id):
    travel_allw = Travel_allw.query.get_or_404(travel_allw_id)
    db.session.delete(travel_allw)
    db.session.commit()
    flash('Your travel allowance entry has been deleted!', 'success')
    return redirect(url_for('all_travel_allw'))


@app.route("/travel_allw/new/manual", methods=['GET', 'POST'])
@login_required
def new_travel_allw():
    form = Travel_allwForm()
    if form.validate_on_submit():
        travel_allw = Travel_allw(name=form.name.data, designation=form.designation.data, department = form.department.data, basic_pay = form.basic_pay.data, d_o_j1 = form.d_o_j1.data.strftime('%d/%m/%y'), d_o_j2 = form.d_o_j2.data.strftime('%d/%m/%y'), p_o_j = form.p_o_j.data, s_no = form.p_o_j.data, c_o_j = form.c_o_j.data, e_o_f = form.e_o_f.data, acc_chrg = form.acc_chrg.data, exp = form.exp.data, details = form.details.data, add_req = form.add_req.data, ta_no = form.ta_no.data, ta_ad = form.ta_ad.data, rup = form.rup.data, b_name = form.b_name.data, b_acc = form.b_acc.data, ifsc = form.ifsc.data)
        db.session.add(travel_allw)
        db.session.commit()
        flash('Your travel allowance entry has been created!', 'success')
        return redirect(url_for('all_travel_allw'))
    return render_template('travel_allwform.html', title='New Travel Allowance Form',
                           form=form, legend='New Travel Allowance Form')

@app.route("/travel_allw/new/default", methods=['GET', 'POST'])
@login_required
def new_travel_allw_default():
    form = Travel_allwForm()
    user_id = current_user.get_id()
    user = User.query.get_or_404(int(user_id))
    form.name.data = user.name
    form.s_no.data = user.id_no
    form.designation.data = user.dsgn
    form.department.data = user.dept
    #form.inst.data = user.inst
    form.basic_pay.data = user.basic_pay
    form.b_name.data = user.bname
    form.b_acc.data = user.bacc
    form.ifsc.data = user.ifsc
    if form.validate_on_submit():
        travel_allw = Travel_allw(name=form.name.data, designation=form.designation.data, department = form.department.data, basic_pay = form.basic_pay.data, d_o_j1 = form.d_o_j1.data.strftime('%d/%m/%y'), d_o_j2 = form.d_o_j2.data.strftime('%d/%m/%y'), p_o_j = form.p_o_j.data, s_no = form.s_no.data, c_o_j = form.c_o_j.data, e_o_f = form.e_o_f.data, acc_chrg = form.acc_chrg.data, exp = form.exp.data, details = form.details.data, add_req = form.add_req.data, ta_no = form.ta_no.data, ta_ad = form.ta_ad.data, rup = form.rup.data, b_name = form.b_name.data, b_acc = form.b_acc.data, ifsc = form.ifsc.data)
        db.session.add(travel_allw)
        db.session.commit()
        flash('Your travel allowance entry has been created!', 'success')
        return redirect(url_for('all_travel_allw'))
    return render_template('travel_allwform.html', title='New Travel Allowance Form',
                           form=form, legend='New Travel Allowance Form')



def createpdf_tra(name,desigtn,dept,basic_p,d_o_j1,d_o_j2,p_o_j,s_no,c_o_j,e_o_f,acc_chrg,\
		   			exp,details,ad_req,ta_no,ta_ad,rup,b_name, b_acc,ifs):
	
    packet = io.BytesIO()
# create a new PDF with Reportlab
    can = canvas.Canvas(packet,pagesize=A4)
    can.setFont("Helvetica", 10) 
    can.drawString(250, 602, name)
    can.drawString(505, 598, s_no)
    can.drawString(250, 584, desigtn)
    can.drawString(250, 568, dept)
    can.drawString(250,551, basic_p)
    can.drawString(220,532, d_o_j1)
    can.drawString(292,532, d_o_j2)
    can.drawString(230,514, p_o_j)
    can.drawString(342,473, c_o_j)
    can.drawString(350,442, e_o_f)
	# can.drawString(442,442, "3326")
    can.drawString(350,420, acc_chrg)
	# can.drawString(442,420, "3326")
    can.drawString(350,398, exp)
	# can.drawString(442,398, "3326")
    nn = int(e_o_f) + int(acc_chrg) + int(exp)
    mm = str(nn)
    can.drawString(150,382, details)
    can.drawString(335,353, mm)
    can.drawString(130,203, ta_no)
    can.drawString(225,160, mm)
    p = inflect.engine()
    ss = p.number_to_words(nn)
    ss = ss.upper()
    #can.drawString(170, 213, ss)
    can.drawString(130,143, ss)
    can.drawString(225,58, b_name)
    can.drawString(225,47, b_acc)
    can.drawString(225,37, ifs)
    can.save()

#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF
    cw = os.getcwd()
    filepath = cw + "/static"
    existing_pdf = PdfFileReader(open((filepath+"/Travel_adv.pdf"), "rb"))
    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file
    outputStream = open(name+"_trav.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return


@app.route("/travel_allw/<int:travel_allw_id>/download", methods=['GET', 'POST'])
@login_required
def download_travel_allw(travel_allw_id):
    travel_allw = Travel_allw.query.get_or_404(travel_allw_id)
    createpdf_tra(travel_allw.name,travel_allw.designation,travel_allw.department,str(travel_allw.basic_pay),travel_allw.d_o_j1,travel_allw.d_o_j2,travel_allw.p_o_j,travel_allw.s_no,travel_allw.c_o_j,travel_allw.e_o_f,travel_allw.acc_chrg,\
		   			travel_allw.exp,travel_allw.details,travel_allw.add_req,travel_allw.ta_no,travel_allw.ta_ad,travel_allw.rup,travel_allw.b_name, travel_allw.b_acc,travel_allw.ifsc)
    path31 = os.getcwd() + '/' +travel_allw.name + "_trav.pdf"
    return send_file(path31, attachment_filename=travel_allw.name + "_trav.pdf", as_attachment=True)


#####################################################################################################################################################


@app.route("/all_contingent")
@login_required
def all_contingent():
    contingents = Contingent.query.all()
    return render_template('contingent.html', contingents=contingents)


@app.route("/delete_contingents")
@login_required
def delete_contingents():
   contingents = Contingent.query.all()
   for contingent in contingents:
      db.session.delete(contingent)
      db.session.commit()
   flash('All Contingent data has been deleted!', 'success')
   return redirect(url_for('all_contingent'))

@app.route("/contingent/<int:contingent_id>/update", methods=['GET', 'POST'])
@login_required
def update_contingent(contingent_id):
    contingent = Contingent.query.get_or_404(contingent_id)
    
    form = ContingentForm()
    if form.validate_on_submit():
        '''
        contingent.dt1 = form.dt1.data
        contingent.des1 = form.des1.data
        contingent.amt1 = form.amt1.data
        contingent.dt2 = form.dt2.data
        contingent.des2 = form.des2.data
        contingent.amt2 = form.amt2.data
        contingent.dt3 = form.dt3.data
        contingent.amt3 = form.amt3.data
        contingent.dt4 = form.dt4.data
        contingent.des4 = form.des4.data
        contingent.amt4 = form.amt4.data
        '''
        contingent.curr_date = form.curr_date.data.strftime('%d/%m/%y')
        contingent.station = form.station.data
        contingent.name = form.name.data
        contingent.address = form.address.data
        contingent.bankbranch = form.bankbranch.data
        contingent.acc_num = form.acc_num.data
        contingent.ifsc = form.ifsc.data
        db.session.commit()
        flash('Your Contingent form entry has been updated!', 'success')
        return redirect(url_for('all_contingent'))
    elif request.method == 'GET':
        '''
        form.dt1.data = datetime.strptime(contingent.dt1, '%Y-%m-%d')
        form.des1.data = contingent.des1
        form.amt1.data = contingent.amt1
        form.dt2.data = datetime.strptime(contingent.dt2, '%Y-%m-%d')
        form.des2.data = contingent.des2
        form.amt2.data = contingent.amt2
        form.dt3.data = datetime.strptime(contingent.dt3, '%Y-%m-%d')
        form.des3.data = contingent.des3
        form.amt3.data = contingent.amt3  
        form.dt4.data = datetime.strptime(contingent.dt4, '%Y-%m-%d')
        form.des4.data = contingent.des4
        form.amt4.data = contingent.amt4 
        '''
        form.curr_date.data = datetime.strptime(contingent.curr_date, '%d/%m/%y')
        form.station.data = contingent.station  
        form.name.data = contingent.name  
        form.address.data = contingent.address  
        form.bankbranch.data = contingent.bankbranch 
        form.acc_num.data = contingent.acc_num  
        form.ifsc.data = contingent.ifsc 
    return render_template('contingentform.html',title='Update Contingent Form',form=form, legend='Update Contingent Form')


@app.route("/contingent/<int:contingent_id>/delete")
@login_required
def delete_contingent(contingent_id):
    contingent = Contingent.query.get_or_404(contingent_id)
    db.session.delete(contingent)
    db.session.commit()
    flash('Your Contingent entry has been deleted!', 'success')
    return redirect(url_for('all_contingent'))


@app.route("/contingent/new/manual", methods=['GET', 'POST'])
@login_required
def new_contingent():
    form = ContingentForm()
    if form.validate_on_submit():
        contingent = Contingent(curr_date = form.curr_date.data.strftime('%d/%m/%y'), station = form.station.data, name = form.name.data, address = form.address.data, bankbranch = form.bankbranch.data, acc_num = form.acc_num.data, ifsc = form.ifsc.data)
        db.session.add(contingent)
        db.session.commit()
        flash('Your Contingent entry has been created!', 'success')
        return redirect(url_for('all_contingent'))
    return render_template('contingentform.html', title='New Contingent Form',
                           form=form, legend='New Contingent Form')

@app.route("/contingent/new/default", methods=['GET', 'POST'])
@login_required
def new_contingent_default():
    form = ContingentForm()
    user_id = current_user.get_id()
    user = User.query.get_or_404(int(user_id))
    form.name.data = user.name
    form.address.data = user.address
    form.bankbranch.data = user.bname
    form.acc_num.data = user.bacc
    form.ifsc.data = user.ifsc
    if form.validate_on_submit():
        contingent = Contingent(curr_date = form.curr_date.data.strftime('%d/%m/%y'), station = form.station.data, name = form.name.data, address = form.address.data, bankbranch = form.bankbranch.data, acc_num = form.acc_num.data, ifsc = form.ifsc.data)
        db.session.add(contingent)
        db.session.commit()
        flash('Your Contingent entry has been created!', 'success')
        return redirect(url_for('all_contingent'))
    return render_template('contingentform.html', title='New Contingent Form',
                           form=form, legend='New Contingent Form')


@app.route("/contingent/<int:contingent_id>/new_a",methods=['GET', 'POST'])
@login_required
def new_contingent_a(contingent_id):
    form = Contingent_aForm()
    if form.validate_on_submit():
        contingent_a = Contingent_a(dt1 = form.dt1.data.strftime('%d/%m/%y'),des1 = form.des1.data,amt1 = form.amt1.data,contingent_id = contingent_id)
        db.session.add(contingent_a)
        db.session.commit()
        flash('Your Contingent Expenditure Bill (Part 2) entry has been created!', 'success')
        return redirect(url_for('all_contingent', contingent_id = contingent_id))
    return render_template('contingent_aform.html', title='New Contingent Expenditure Bill (Part 2) Form',
                           form=form, legend='New Contingent Expenditure Bill (Part 2) Form')


@app.route("/contingent/<int:contingent_a_id>/delete_a")
@login_required
def delete_contingent_a(contingent_a_id):
    contingent_a = Contingent_a.query.get_or_404(contingent_a_id)
    db.session.delete(contingent_a)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_contingent'))


@app.route("/contingent/<int:contingent_id>/all_contingent_a")
@login_required
def all_contingent_a(contingent_id):
    contingent = Contingent.query.get_or_404(contingent_id)
    contingents_a = contingent.pets
    return render_template('contingent_a.html', contingents_a=contingents_a, contingent = contingent)


@app.route("/contingent/<int:contingent_id>/download", methods=['GET', 'POST'])
@login_required
def download_contingent(contingent_id):
    contingent = Contingent.query.get_or_404(contingent_id)
    packet = io.BytesIO()
# create a new PDF with Reportlab
    can = canvas.Canvas(packet,pagesize=A4)
    can.setFont("Helvetica", 10)
    ''' 
    can.drawString(73, 520, params[0])
    can.drawString(150, 520, params[1])
    can.drawString(460, 520, params[2])
    can.drawString(73, 495, params[3])
    can.drawString(150, 495, params[4])
    can.drawString(460, 495, params[5])
    can.drawString(73, 470, params[6])
    can.drawString(150, 470, params[7])
    can.drawString(460, 470, params[8])
    can.drawString(73, 445, params[9])
    can.drawString(150, 445, params[10])
    can.drawString(460, 445, params[11])

    total = int(params[11]) + int(params[8]) + int(params[5]) + int(params[2])
    can.drawString(460, 398, str(total))#total
    '''
    ccd = -1
    total = 0
    conts = contingent.pets
    for cont in conts:
        ccd += 1
        can.drawString(73, 520-(15*ccd), cont.dt1)
        can.drawString(150, 520-(15*ccd), cont.des1)
        can.drawString(460, 520-(15*ccd), str(cont.amt1))
        total += cont.amt1
    total = "%.2f" % total
    can.drawString(460, 398, str(total))
    p = inflect.engine()
    ss = p.number_to_words(int(float(total)))
    ss = ss.upper()
    can.drawString(100, 365, ss)
    can.drawString(90, 260, contingent.curr_date)
    can.drawString(130, 245, contingent.station)
    can.drawString(425, 215, contingent.name)
    can.drawString(425, 197, contingent.address)
    can.drawString(230, 85, contingent.bankbranch)
    can.drawString(230, 63, contingent.acc_num)
    can.drawString(230, 40, contingent.ifsc)
    can.save()
#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF
    cw = os.getcwd()
    filepath = cw + "/static"
    existing_pdf = PdfFileReader(open((filepath+"/contingent_exp.pdf"), "rb"))
    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file
    outputStream = open(contingent.name+"_cont.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    path41 = os.getcwd() + '/' +contingent.name + "_cont.pdf"
    return send_file(path41, attachment_filename=contingent.name + "_cont.pdf", as_attachment=True)


#####################################################################################################################################################

@app.route("/all_tab")
@login_required
def all_tab():
    tabs = Tab.query.all()
    return render_template('tab.html', tabs=tabs)


@app.route("/delete_tabs")
@login_required
def delete_tabs():
   tabs = Tab.query.all()
   for tab in tabs:
      db.session.delete(tab)
      db.session.commit()
   flash('All Travel Allowance Bills are deleted!', 'success')
   return redirect(url_for('all_tab'))

@app.route("/tab/<int:tab_id>/update", methods=['GET', 'POST'])
@login_required
def update_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    
    form = TabForm()
    if form.validate_on_submit():
        tab.name = form.name.data
        tab.srn = form.srn.data
        tab.dsgn = form.dsgn.data
        tab.dpt = form.dpt.data
        tab.inst = form.inst.data
        tab.bp = form.bp.data
        tab.ipac = form.ipac.data
        tab.poj = form.poj.data
        '''
        tab.ds = form.ds.data
        tab.dd = form.dd.data
        tab.dtym = form.dtym.data
        tab.arst = form.arst.data
        tab.ad = form.ad.data
        tab.atym = form.atym.data
        tab.moj = form.moj.data
        tab.jc = form.jc.data
        tab.road = form.road.data
        tab.tktno = form.tktno.data
        tab.fare = form.fare.data
        tab.exp = form.exp.data
        tab.amt22 = form.amt22.data
        tab.bill = form.bill.data
        '''
        tab.enc = form.enc.data
        tab.date = form.date.data.strftime('%d/%m/%y')
        #tab.amt44 = form.amt44.data
        #tab.amt55 = form.amt55.data
        #tab.AB = form.AB.data
        tab.advdrawn = form.advdrawn.data
        #tab.netclaimed = form.netclaimed.data
        #tab.excesspaid = form.excesspaid.data
        #tab.excessrecovered = form.excessrecovered.data
        tab.bankname = form.bankname.data
        tab.accno = form.accno.data
        tab.ifsc = form.ifsc.data
        db.session.commit()
        flash('Your Travel Allowance Bill form entry has been updated!', 'success')
        return redirect(url_for('all_tab'))
    elif request.method == 'GET':
        # form.dt1.data = datetime.strptime(tab.dt1, '%Y-%m-%d')

        form.name.data = tab.name
        form.srn.data = tab.srn 
        form.dsgn.data = tab.dsgn
        form.dpt.data = tab.dpt 
        form.inst.data = tab.inst 
        form.bp.data = tab.bp 
        form.ipac.data = tab.ipac 
        form.poj.data = tab.poj
        '''
        form.ds.data = tab.ds 
        form.dd.data = datetime.strptime(tab.dd, '%Y-%m-%d')
        form.dtym.data = tab.dtym 
        form.arst.data = tab.arst 
        form.ad.data = datetime.strptime(tab.ad, '%Y-%m-%d') 
        form.atym.data = tab.atym 
        form.moj.data = tab.moj 
        form.jc.data = tab.jc 
        form.road.data = tab.road
        form.tktno.data = tab.tktno 
        form.fare.data = tab.fare 
        form.exp.data = tab.exp 
        form.amt22.data = tab.amt22 
        form.bill.data = tab.bill 
        '''
        form.enc.data = tab.enc 
        form.date.data = datetime.strptime(tab.date, '%d/%m/%y')
        #form.amt44.data = tab.amt44 
        #form.amt55.data = tab.amt55 
        #form.AB.data = tab.AB 
        form.advdrawn.data = tab.advdrawn 
        #form.netclaimed.data = tab.netclaimed 
        #form.excesspaid.data = tab.excesspaid 
        #form.excessrecovered.data = tab.excessrecovered 
        form.bankname.data = tab.bankname 
        form.accno.data = tab.accno 
        form.ifsc.data = tab.ifsc
    return render_template('tabform.html',title='Update Travel Allowance Bill Form',form=form, legend='Update Travel Allowance Bill Form')


@app.route("/tab/<int:tab_id>/delete")
@login_required
def delete_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    db.session.delete(tab)
    db.session.commit()
    flash('Your Travel Allowance Bill entry has been deleted!', 'success')
    return redirect(url_for('all_tab'))


@app.route("/tab/new", methods=['GET', 'POST'])
@login_required
def new_tab():
    form = TabForm()
    if form.validate_on_submit():
        tab = Tab(name = form.name.data,srn = form.srn.data,dsgn = form.dsgn.data,dpt = form.dpt.data,inst = form.inst.data,bp = form.bp.data,ipac = form.ipac.data,poj = form.poj.data,enc = form.enc.data,date = form.date.data.strftime('%d/%m/%y'),advdrawn = form.advdrawn.data,bankname = form.bankname.data,accno = form.accno.data,ifsc = form.ifsc.data)
        db.session.add(tab)
        db.session.commit()
        flash('Your Travel Allowance Bill entry has been created!', 'success')
        return redirect(url_for('all_tab'))
    return render_template('tabform.html', title='New Travel Allowance Bill Form',
                           form=form, legend='New Travel Allowance Bill Form')

@app.route("/tab/new/default", methods=['GET', 'POST'])
@login_required
def new_tab_default():
    form = TabForm()
    user_id = current_user.get_id()
    user = User.query.get_or_404(int(user_id))
    form.name.data = user.name
    form.srn.data = user.id_no
    form.dsgn.data = user.dsgn
    form.dpt.data = user.dept
    form.inst.data = user.inst
    form.bp.data = user.basic_pay
    form.bankname.data = user.bname
    form.accno.data = user.bacc
    form.ifsc.data = user.ifsc
    if form.validate_on_submit():
        tab = Tab(name = form.name.data,srn = form.srn.data,dsgn = form.dsgn.data,dpt = form.dpt.data,inst = form.inst.data,bp = form.bp.data,ipac = form.ipac.data,poj = form.poj.data,enc = form.enc.data,date = form.date.data.strftime('%d/%m/%y'),advdrawn = form.advdrawn.data,bankname = form.bankname.data,accno = form.accno.data,ifsc = form.ifsc.data)
        db.session.add(tab)
        db.session.commit()
        flash('Your Travel Allowance Bill entry has been created!', 'success')
        return redirect(url_for('all_tab'))
    return render_template('tabform.html', title='New Travel Allowance Bill Form',
                           form=form, legend='New Travel Allowance Bill Form')



@app.route("/tab/<int:tab_id>/download", methods=['GET', 'POST'])
@login_required
def download_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    packet = io.BytesIO()
# create a new PDF with Reportlab
    can = canvas.Canvas(packet,pagesize=A4)
    can.setFont("Helvetica", 10) 
    can.drawString(95, 692, tab.name)
    can.drawString(355,692, tab.srn)
    can.setFont("Helvetica", 7)
    can.drawString(111,673, tab.dsgn)
    can.drawString(228,673, tab.dpt)
    can.setFont("Helvetica", 10)
    can.drawString(345,673, tab.inst)
    can.drawString(113,653, str(tab.bp))
    can.drawString(494,651, str(tab.ipac))
    can.drawString(140,632, tab.poj)
    tabs_a = tab.pets1
    tabs_b = tab.pets2
    total_a = 0
    total_b = 0
    total = 0
    net = 0
    cca = -1
    ccb = -1
    #ccb = tabs_b.id - 1
    for tab_a in tabs_a:
        cca = cca + 1
        can.drawString(70,(550-(20*cca)), tab_a.ds)
        can.drawString(122,(550-(20*cca)),tab_a.dd)
        can.drawString(175,(550-(20*cca)), tab_a.dtym)
        can.drawString(215,(550-(20*cca)), tab_a.arst)
        can.drawString(275,(550-(20*cca)), tab_a.ad)
        can.drawString(326,(550-(20*cca)), tab_a.atym)
        can.drawString(360, (550-(20*cca)), tab_a.moj)
        can.drawString(402,(550-(20*cca)), tab_a.jc)
        can.drawString(442,(550-(20*cca)), str(tab_a.road))
        can.drawString(478,(550-(20*cca)), tab_a.tktno)
        can.drawString(560,(550-(20*cca)), str(tab_a.fare))
        total_a = total_a + float(tab_a.fare)
    
    for tab_b in tabs_b:
        ccb = ccb + 1
        can.drawString(52,(330-(12*ccb)), str(ccb + 1))
        can.drawString(90,(330-(12*ccb)), tab_b.exp)
        can.drawString(460,(330-(12*ccb)), str(tab_b.amt22))
        can.drawString(525,(330-(12*ccb)), tab_b.bill)
        total_b = total_b + float(tab_b.amt22)
    '''
    can.drawString(70,550, tab.ds)
    can.drawString(122,550,tab.dd)
    can.drawString(175,550, tab.dtym)
    can.drawString(215,550, tab.arst)
    can.drawString(275,550, tab.ad)
    can.drawString(326,550, tab.atym)
    can.drawString(360, 550, tab.moj)
    can.drawString(402,550, tab.jc)
    can.drawString(442,550, str(tab.road))
    can.drawString(478,550, tab.tktno)
    can.drawString(560,550, str(tab.fare))
    can.drawString(550,390, str(tab.fare))
    can.drawString(52,330, '1')
    
    can.drawString(525,252.5, str(tab.amt22))
    '''
    total_a = "%.2f" % total_a
    total_b = "%.2f" % total_b
    can.drawString(525,252.5, str(total_b))
    can.drawString(550,390, str(total_a))
    can.drawString(130,241, str(tab.enc))
    can.drawString(80,231.5, tab.date)
    can.drawString(280,223, str(total_a))
    can.drawString(362,223, str(total_b))
    total = float(total_a) + float(total_b)
    total = "%.2f" % total
    can.drawString(215,204, str(total))
    can.drawString(215,194, str(tab.advdrawn))
    net = float(total) - float(tab.advdrawn)
    can.drawString(215,184, str(net))
    #can.drawString(215,174, str(tab.excesspaid))
    #can.drawString(215,165, str(tab.excessrecovered))
    if (net>0) :
        can.drawString(215,174, str(net))
        can.drawString(215,165,'-')
    else:
        can.drawString(215,165, str(net*(-1)))
        can.drawString(215,174,'-')
    can.save()
#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF
    cw = os.getcwd()
    filepath = cw + "/static"
    existing_pdf = PdfFileReader(open((filepath+"/TAB.pdf"), "rb"))
    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file
    outputStream = open(tab.name+"_tab.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    path51 = os.getcwd() + '/' +tab.name + "_tab.pdf"
    return send_file(path51, attachment_filename=tab.name + "_tab.pdf", as_attachment=True)


##########################################################################################################

@app.route("/tab/<int:tab_id>/new_a",methods=['GET', 'POST'])
@login_required
def new_tab_a(tab_id):
    form = Tab_aForm()
    if form.validate_on_submit():
        tab_a = Tab_a(ds = form.ds.data,dd = form.dd.data.strftime('%d/%m/%y'),dtym = form.dtym.data.strftime('%H:%M'),arst = form.arst.data,ad = form.ad.data.strftime('%d/%m/%y'),atym = form.atym.data.strftime('%H:%M'),moj = form.moj.data,jc = form.jc.data,road = form.road.data,tktno = form.tktno.data,fare = form.fare.data, tab_id = tab_id)
        db.session.add(tab_a)
        db.session.commit()
        flash('Your Travel Allowance Bill (Part A) entry has been created!', 'success')
        return redirect(url_for('all_tab', tab_id = tab_id))
    return render_template('tab_aform.html', title='New Travel Allowance Bill (Part A) Form',
                           form=form, legend='New Travel Allowance Bill Form (Part A)')



@app.route("/tab/<int:tab_id>/all_tab_a")
@login_required
def all_tab_a(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    tabs_a = tab.pets1
    return render_template('tab_a.html', tabs_a=tabs_a, tab = tab)


@app.route("/tab/<int:tab_a_id>/delete_tab_a")
@login_required
def delete_tab_a(tab_a_id):
    tab_a = Tab_a.query.get_or_404(tab_a_id)
    db.session.delete(tab_a)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_tab'))

############################################################################################################################################################################

@app.route("/tab/<int:tab_id>/new_b",methods=['GET', 'POST'])
@login_required
def new_tab_b(tab_id):
    form = Tab_bForm()
    if form.validate_on_submit():
        tab_b = Tab_b(exp = form.exp.data,amt22 = form.amt22.data,bill = form.bill.data,tab_id = tab_id)
        db.session.add(tab_b)
        db.session.commit()
        flash('Your Travel Allowance Bill (Part B) entry has been created!', 'success')
        return redirect(url_for('all_tab', tab_id = tab_id))
    return render_template('tab_bform.html', title='New Travel Allowance Bill (Part B) Form',
                           form=form, legend='New Travel Allowance Bill Form (Part B)')



@app.route("/tab/<int:tab_id>/all_tab_b")
@login_required
def all_tab_b(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    tabs_b = tab.pets2
    return render_template('tab_b.html', tabs_b=tabs_b, tab = tab)


@app.route("/tab/<int:tab_b_id>/delete_tab_b")
@login_required
def delete_tab_b(tab_b_id):
    tab_b = Tab_b.query.get_or_404(tab_b_id)
    db.session.delete(tab_b)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_tab'))
######################################################################################################################################



@app.route("/all_reim")
@login_required
def all_reim():
    reims = Reim.query.all()
    return render_template('reim.html', reims=reims)


@app.route("/reim/new/manual", methods=['GET', 'POST'])
@login_required
def new_reim():
    form = ReimForm()
    if form.validate_on_submit():
        reim = Reim(name = form.name.data, dpt = form.dpt.data, bank = form.bank.data, acc_no = form.acc_no.data, ifsc = form.ifsc.data)
        db.session.add(reim)
        db.session.commit()
        flash('Your Reimbursement Form has been created!', 'success')
        return redirect(url_for('all_reim'))
    return render_template('reimform.html', title='New Reimbursement Form',
                           form=form, legend='New Reimbursement Form')

@app.route("/reim/new/default", methods=['GET', 'POST'])
@login_required
def new_reim_default():
    form = ReimForm()
    user_id = current_user.get_id()
    user = User.query.get_or_404(int(user_id))
    form.name.data = user.name
    form.dpt.data = user.dept
    form.bank.data = user.bname
    form.acc_no.data = user.bacc
    form.ifsc.data = user.ifsc
    if form.validate_on_submit():
        reim = Reim(name = form.name.data, dpt = form.dpt.data, bank = form.bank.data, acc_no = form.acc_no.data, ifsc = form.ifsc.data)
        db.session.add(reim)
        db.session.commit()
        flash('Your Reimbursement Form has been created!', 'success')
        return redirect(url_for('all_reim'))
    return render_template('reimform.html', title='New Reimbursement Form',
                           form=form, legend='New Reimbursement Form')

@app.route("/delete_reims")
@login_required
def delete_reims():
   reims = Reim.query.all()
   for reim in reims:
      db.session.delete(reim)
      db.session.commit()
   flash('All Reimbursement data has been deleted!', 'success')
   return redirect(url_for('all_reim'))


@app.route("/reim/<int:reim_id>/delete")
@login_required
def delete_reim(reim_id):
    reim = Reim.query.get_or_404(reim_id)
    db.session.delete(reim)
    db.session.commit()
    flash('Your Reimbursement form entry has been deleted!', 'success')
    return redirect(url_for('all_reim'))


@app.route("/reim/<int:reim_id>/update", methods=['GET', 'POST'])
@login_required
def update_reim(reim_id):
    reim = Reim.query.get_or_404(reim_id)
    
    form = ReimForm()
    if form.validate_on_submit():
        reim.name = form.name.data
        reim.dpt = form.dpt.data
        #reim.net_claimed = form.net_claimed.data
        reim.bank = form.bank.data
        reim.acc_no = form.acc_no.data
        reim.ifsc = form.ifsc.data
        db.session.commit()
        flash('Your Reimbursement form entry has been updated!', 'success')
        return redirect(url_for('all_reim'))
    elif request.method == 'GET':  
        form.name.data = reim.name  
        form.dpt.data = reim.dpt  
        #form.net_claimed.data = reim.net_claimed
        form.bank.data = reim.bank
        form.acc_no.data = reim.acc_no  
        form.ifsc.data = reim.ifsc 
    return render_template('reimform.html',title='Update Reimbursement Form',form=form, legend='Update Reimbursement Form')

@app.route("/reim/<int:reim_id>/all_reim_det")
@login_required
def all_reim_det(reim_id):
    reim = Reim.query.get_or_404(reim_id)
    reim_dets = reim.pets
    return render_template('reim_det.html', reim_dets=reim_dets, reim = reim)


@app.route("/reim/<int:reim_id>/new_reim_det",methods=['GET', 'POST'])
@login_required
def new_reim_det(reim_id):
    form = Reim_detForm()
    if form.validate_on_submit():
        reim_det = Reim_det(date = str(form.date.data.strftime('%d/%m/%y')),cash_no = form.cash_no.data,firm = form.firm.data,purpose = form.purpose.data,amt = form.amt.data,reim_id = reim_id)
        db.session.add(reim_det)
        db.session.commit()
        flash('Your Reimbursement Form Detail entry has been created!', 'success')
        return redirect(url_for('all_reim', reim_id = reim_id))
    return render_template('reim_detform.html', title='New Reimbursement Detail Form',
                           form=form, legend='New Reimbursement Detail Form')


@app.route("/reim/<int:reim_det_id>/delete_reim_det")
@login_required
def delete_reim_det(reim_det_id):
    reim_det = Reim_det.query.get_or_404(reim_det_id)
    db.session.delete(reim_det)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_reim'))


@app.route("/reim/<int:reim_id>/download", methods=['GET', 'POST'])
@login_required
def download_reim(reim_id):
    reim = Reim.query.get_or_404(reim_id)
    packet = io.BytesIO()
# create a new PDF with Reportlab
    can = canvas.Canvas(packet,pagesize=A4)
    can.setFont("Helvetica", 10)
    ccd = -1
    total = 0
    flag1 = 0
    flag2 = 0
    flag3 = 0
    reim_dets = reim.pets
    can.drawString(210, 588, reim.name)
    #can.showPage()
    can.drawString(210, 570, reim.dpt)
    #can.drawString(210, 550, reim.net_claimed)
    count = 1
    for reim_det in reim_dets:
        ccd += 1
        flag = flag1 + flag2 + flag3
        if(flag > 0):
            ccd = ccd + 1
        wwe = reim_det.cash_no
        can.drawString(84, 488-(19*ccd), str(count))
        can.drawString(107, 488-(19*ccd), reim_det.date)
        #can.drawString(213, 488-(19*ccd), reim_det.firm)
        #can.drawString(364, 488-(19*ccd), reim_det.purpose)
        #can.drawString(525, 488-(19*ccd), str(reim_det.amt))
        if (len(reim_det.cash_no) > 10):
            flag1 = 1
            can.drawString(153, 488-(19*ccd), wwe[0:9])
            ccd = ccd + 1
            xx = len(reim_det.cash_no)
            can.drawString(153, 488-(19*ccd), wwe[9:xx])
            ccd = ccd -1
        else :
            flag1 = 0
            can.drawString(153, 488-(19*ccd), reim_det.cash_no)
        
        if (len(reim_det.firm) > 30):
            flag2 = 1
            wwe1 = reim_det.firm
            can.drawString(213, 488-(19*ccd), wwe1[0:29])
            ccd = ccd + 1
            xx = len(reim_det.firm)
            can.drawString(213, 488-(19*ccd), wwe1[29:xx])
            ccd = ccd -1
        else :
            flag2 = 0
            can.drawString(213, 488-(19*ccd), reim_det.firm)
        
        if (len(reim_det.purpose) > 30):
            flag3 = 1
            wwe2 = reim_det.purpose
            can.drawString(364, 488-(19*ccd), wwe2[0:29])
            ccd = ccd + 1
            xx = len(reim_det.purpose)
            can.drawString(364, 488-(19*ccd), wwe2[29:xx])
            ccd = ccd - 1
        else :
            flag3 = 0
            can.drawString(364, 488-(19*ccd), reim_det.purpose)
        can.drawString(525, 488-(19*ccd), str(reim_det.amt))
        total += reim_det.amt
        count += 1
    total = "%.2f" % total
    p = inflect.engine()
    ss = p.number_to_words(int(float(total)))
    ss = ss.upper()
    can.drawString(170, 213, ss)
    can.drawString(530, 225, str(total))
    can.drawString(470, 155, str(total))
    can.drawString(210, 550, str(total))         #net claimed
    can.drawString(230, 88, reim.bank)
    can.drawString(230, 78, reim.acc_no)
    can.drawString(230, 68, reim.ifsc)
    can.save()
#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF
    cw = os.getcwd()
    filepath = cw + "/static"
    existing_pdf = PdfFileReader(open((filepath+"/Reimbursement.pdf"), "rb"))
    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file
    outputStream = open(reim.name+"_reim.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    path51 = os.getcwd() + '/' +reim.name + "_reim.pdf"
    return send_file(path51, attachment_filename=reim.name + "_reim.pdf", as_attachment=True)


########################################################################################################################################################


@app.route("/all_opt_cert")
@login_required
def all_opt_cert():
    opt_certs = Opt_cert.query.all()
    return render_template('opt_cert.html', opt_certs=opt_certs)


@app.route("/opt_cert/new/manual", methods=['GET', 'POST'])
@login_required
def new_opt_cert():
    form = Opt_certForm()
    if form.validate_on_submit():
        opt_cert = Opt_cert(name_emp = form.name_emp.data, dsg_emp = form.dsg_emp.data, emp_id = form.emp_id.data, pt_nm = form.pt_nm.data, age = form.age.data, relationship=form.relationship.data, nm_address_doc = form.nm_address_doc.data, disease = form.disease.data, from_date=str(form.from_date.data.strftime('%d/%m/%y')),to_date = str(form.to_date.data.strftime('%d/%m/%y')),referred_doc = form.referred_doc.data, place = form.place.data, date = str(form.date.data.strftime('%d/%m/%y')))
        db.session.add(opt_cert)
        db.session.commit()
        flash('Your Opt Certificate A Form has been created!', 'success')
        return redirect(url_for('all_opt_cert'))
    return render_template('opt_certform.html', title='New Opt Certificate A Form',
                           form=form, legend='New Opt Certificate A Form')



@app.route("/opt_cert/new/default", methods=['GET', 'POST'])
@login_required
def new_opt_cert_default():
    form = Opt_certForm()
    user_id = current_user.get_id()
    user = User.query.get_or_404(int(user_id))
    form.name_emp.data = user.name
    form.dsg_emp.data = user.dsgn
    form.emp_id.data = user.id_no
    if form.validate_on_submit():
        opt_cert = Opt_cert(name_emp = form.name_emp.data, dsg_emp = form.dsg_emp.data, emp_id = form.emp_id.data, pt_nm = form.pt_nm.data, age = form.age.data, relationship=form.relationship.data, nm_address_doc = form.nm_address_doc.data, disease = form.disease.data, from_date=str(form.from_date.data.strftime('%d/%m/%y')),to_date = str(form.to_date.data.strftime('%d/%m/%y')),referred_doc = form.referred_doc.data, place = form.place.data, date = str(form.date.data.strftime('%d/%m/%y')))
        db.session.add(opt_cert)
        db.session.commit()
        flash('Your Opt Certificate A Form has been created!', 'success')
        return redirect(url_for('all_opt_cert'))
    return render_template('opt_certform.html', title='New Opt Certificate A Form',
                           form=form, legend='New Opt Certificate A Form')


@app.route("/delete_opt_certs")
@login_required
def delete_opt_certs():
   opt_certs = Opt_cert.query.all()
   for opt_cert in opt_certs:
      db.session.delete(opt_cert)
      db.session.commit()
   flash('All Opt Certificate A data has been deleted!', 'success')
   return redirect(url_for('all_opt_cert'))


@app.route("/opt_cert/<int:opt_cert_id>/delete")
@login_required
def delete_opt_cert(opt_cert_id):
    opt_cert = Opt_cert.query.get_or_404(opt_cert_id)
    db.session.delete(opt_cert)
    db.session.commit()
    flash('Your Opt Certificate A form entry has been deleted!', 'success')
    return redirect(url_for('all_opt_cert'))


@app.route("/opt_cert/<int:opt_cert_id>/update", methods=['GET', 'POST'])
@login_required
def update_opt_cert(opt_cert_id):
    opt_cert = Opt_cert.query.get_or_404(opt_cert_id)
    
    form = Opt_certForm()
    if form.validate_on_submit():
        opt_cert.name_emp = form.name_emp.data
        opt_cert.dsg_emp = form.dsg_emp.data
        opt_cert.emp_id = form.emp_id.data
        opt_cert.pt_nm = form.pt_nm.data
        opt_cert.age = form.age.data
        opt_cert.relationship = form.relationship.data
        opt_cert.nm_address_doc = form.nm_address_doc.data
        opt_cert.disease = form.disease.data
        opt_cert.from_date = str(form.from_date.data.strftime('%d/%m/%y'))
        opt_cert.to_date = str(form.to_date.data.strftime('%d/%m/%y'))
        opt_cert.referred_doc = form.referred_doc.data
        opt_cert.place = form.place.data
        opt_cert.date = str(form.date.data.strftime('%d/%m/%y'))
        db.session.commit()
        flash('Your Opt Certificate A form entry has been updated!', 'success')
        return redirect(url_for('all_opt_cert'))
    elif request.method == 'GET':  
        form.name_emp.data = opt_cert.name_emp
        form.dsg_emp.data = opt_cert.dsg_emp
        form.emp_id.data = opt_cert.emp_id
        form.pt_nm.data = opt_cert.pt_nm
        form.age.data = opt_cert.age
        form.relationship.data = opt_cert.relationship
        form.nm_address_doc.data = opt_cert.nm_address_doc
        form.disease.data = opt_cert.disease
        form.from_date.data = datetime.strptime(opt_cert.from_date, '%d/%m/%y')
        form.to_date.data = datetime.strptime(opt_cert.to_date, '%d/%m/%y')
        form.referred_doc.data = opt_cert.referred_doc
        form.place.data = opt_cert.place
        form.date.data = datetime.strptime(opt_cert.date, '%d/%m/%y')
    return render_template('opt_certform.html',title='Update Opt Certificate A Form',form=form, legend='Update Reimbursement Form')



@app.route("/opt_cert/<int:opt_cert_id>/all_opt_cert_a")
@login_required
def all_opt_cert_a(opt_cert_id):
    opt_cert = Opt_cert.query.get_or_404(opt_cert_id)
    opt_certs_a = opt_cert.pets1
    return render_template('opt_cert_a.html', opt_certs_a=opt_certs_a, opt_cert = opt_cert)


@app.route("/opt_cert/<int:opt_cert_id>/new_opt_cert_a",methods=['GET', 'POST'])
@login_required
def new_opt_cert_a(opt_cert_id):
    form = Opt_cert_AForm()
    if form.validate_on_submit():
        opt_cert_a = Opt_cert_A(date = str(form.date.data.strftime('%d/%m/%y')),fee_consult = form.fee_consult.data,fee_inj = form.fee_inj.data,owner_id = opt_cert_id)
        db.session.add(opt_cert_a)
        db.session.commit()
        flash('Your Opt Certificate(Part A) Form Detail entry has been created!', 'success')
        return redirect(url_for('all_opt_cert'))
    return render_template('opt_cert_aform.html', title='New Opt Certificate(Part A) Detail Form',
                           form=form, legend='New Opt Certificate(Part A) Detail Form')


@app.route("/opt_cert/<int:opt_cert_a_id>/delete_opt_cert_a")
@login_required
def delete_opt_cert_a(opt_cert_a_id):
    opt_cert_a = Opt_cert_A.query.get_or_404(opt_cert_a_id)
    db.session.delete(opt_cert_a)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_opt_cert'))



@app.route("/opt_cert/<int:opt_cert_id>/all_opt_cert_b")
@login_required
def all_opt_cert_b(opt_cert_id):
    opt_cert = Opt_cert.query.get_or_404(opt_cert_id)
    opt_certs_b = opt_cert.pets2
    return render_template('opt_cert_b.html', opt_certs_b=opt_certs_b, opt_cert = opt_cert)


@app.route("/opt_cert/<int:opt_cert_id>/new_opt_cert_b",methods=['GET', 'POST'])
@login_required
def new_opt_cert_b(opt_cert_id):
    form = Opt_cert_BForm()
    if form.validate_on_submit():
        opt_cert_b = Opt_cert_B(date = str(form.date.data.strftime('%d/%m/%y')),quantity = form.quantity.data,price = form.price.data,cashmemo = form.cashmemo.data,name = form.name.data,owner_id = opt_cert_id)
        db.session.add(opt_cert_b)
        db.session.commit()
        flash('Your Opt Certificate(Part B) Form Detail entry has been created!', 'success')
        return redirect(url_for('all_opt_cert'))
    return render_template('opt_cert_bform.html', title='New Opt Certificate(Part B) Detail Form',
                           form=form, legend='New Opt Certificate(Part B) Detail Form')


@app.route("/opt_cert/<int:opt_cert_b_id>/delete_opt_cert_b")
@login_required
def delete_opt_cert_b(opt_cert_b_id):
    opt_cert_b = Opt_cert_B.query.get_or_404(opt_cert_b_id)
    db.session.delete(opt_cert_b)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_opt_cert'))



@app.route("/opt_cert/<int:opt_cert_id>/all_opt_cert_c")
@login_required
def all_opt_cert_c(opt_cert_id):
    opt_cert = Opt_cert.query.get_or_404(opt_cert_id)
    opt_certs_c = opt_cert.pets3
    return render_template('opt_cert_c.html', opt_certs_c=opt_certs_c, opt_cert = opt_cert)


@app.route("/opt_cert/<int:opt_cert_id>/new_opt_cert_c",methods=['GET', 'POST'])
@login_required
def new_opt_cert_c(opt_cert_id):
    form = Opt_cert_CForm()
    if form.validate_on_submit():
        opt_cert_c = Opt_cert_C(date = str(form.date.data.strftime('%d/%m/%y')),name_test = form.name_test.data,name_hos = form.name_hos.data,amount = form.amount.data,owner_id = opt_cert_id)
        db.session.add(opt_cert_c)
        db.session.commit()
        flash('Your Opt Certificate(Part C) Form Detail entry has been created!', 'success')
        return redirect(url_for('all_opt_cert'))
    return render_template('opt_cert_cform.html', title='New Opt Certificate(Part C) Detail Form',
                           form=form, legend='New Opt Certificate(Part C) Detail Form')


@app.route("/opt_cert/<int:opt_cert_c_id>/delete_opt_cert_c")
@login_required
def delete_opt_cert_c(opt_cert_c_id):
    opt_cert_c = Opt_cert_C.query.get_or_404(opt_cert_c_id)
    db.session.delete(opt_cert_c)
    db.session.commit()
    flash('Entry Deleted', 'success')
    return redirect(url_for('all_opt_cert'))



@app.route("/opt_cert/<int:opt_cert_id>/download", methods=['GET', 'POST'])
@login_required
def download_opt_cert(opt_cert_id):
    opt_cert = Opt_cert.query.get_or_404(opt_cert_id)
    opt_certs_a = opt_cert.pets1
    opt_certs_b = opt_cert.pets2
    opt_certs_c = opt_cert.pets3
    packet = io.BytesIO()
# create a new PDF with Reportlab
    can = canvas.Canvas(packet,pagesize=A4)
    can.setFont("Helvetica", 13)
    ccd = 0
    total = 0
    total_a = 0
    total_b = 0
    total_c = 0
    '''
    
        can.drawString(84, 488-(19*ccd), str(count))
        
    '''
    can.drawString(170, 680, opt_cert.name_emp)
    can.drawString(373, 680, opt_cert.dsg_emp)
    can.drawString(492, 680, opt_cert.emp_id)
    can.drawString(315, 617, opt_cert.pt_nm)
    can.drawString(315, 600, opt_cert.age)
    can.drawString(315, 587, opt_cert.relationship)
    nmadd = opt_cert.nm_address_doc
    if len(nmadd)>37:
        can.drawString(315, 573, nmadd[:37])
        can.drawString(315, 560, nmadd[37:])
    else:
        can.drawString(315, 573, nmadd)
    can.drawString(315, 535, opt_cert.disease)
    can.drawString(373, 516, opt_cert.from_date)
    can.drawString(373, 503, opt_cert.to_date)
    for opt_cert_a in opt_certs_a:
        can.drawString(145, (374-21*ccd), opt_cert_a.date)
        can.drawString(230, (374-21*ccd), str(opt_cert_a.fee_consult))
        can.drawString(362, (374-21*ccd), str(opt_cert_a.fee_inj))
        ccd = ccd + 1
        total_a = total_a + opt_cert_a.fee_consult + opt_cert_a.fee_inj
    ccd = 0
    for opt_cert_b in opt_certs_b:
        can.drawString(145, (212-21*ccd), opt_cert_b.name)
        can.drawString(280, (212-21*ccd), str(opt_cert_b.quantity))
        can.drawString(337, (212-21*ccd), str(opt_cert_b.price))
        can.drawString(390, (212-21*ccd), str(opt_cert_b.cashmemo))
        can.drawString(490, (212-21*ccd), str(opt_cert_b.date))
        ccd = ccd + 1
        total_b = total_b + opt_cert_b.price
    can.showPage()
    ccd = 0
    for opt_cert_c in opt_certs_c:
        can.drawString(130, (696-21*ccd), opt_cert_c.name_test)
        can.drawString(257, (696-21*ccd), str(opt_cert_c.name_hos))
        can.drawString(400, (696-21*ccd), str(opt_cert_c.date))
        can.drawString(490, (696-21*ccd), str(opt_cert_c.amount))
        ccd = ccd + 1
        total_c = total_c + opt_cert_c.amount
    total = total_a + total_b + total_c
    can.drawString(285, 579, str(total))
    can.drawString(328, 260, str(opt_cert.referred_doc))
    can.drawString(145, 190, str(opt_cert.place))
    can.drawString(135, 162, str(opt_cert.date))
    can.save()
#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF
    cw = os.getcwd()
    filepath = cw + "/static"
    existing_pdf = PdfFileReader(open((filepath+"/cert_A_OPT.pdf"), "rb"))
    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    page2 = existing_pdf.getPage(1)
    page2.mergePage(new_pdf.getPage(1))
    output.addPage(page)
    output.addPage(page2)
# finally, write "output" to a real file
    outputStream = open(str(opt_cert.id)+"_optcert.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    path51 = os.getcwd() + '/' +str(opt_cert.id) + "_optcert.pdf"
    return send_file(path51, attachment_filename=str(opt_cert.id) + "_optcert.pdf", as_attachment=True)

