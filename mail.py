from flask import Flask,render_template,request,session,jsonify,redirect,url_for
import datetime,time
import sqlite3 as sql
from dbConnection.datamanipulation import *
app=Flask(__name__)
app.secret_key='super secret key'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    countries=sql_query("select * from country_tb")
    return render_template('register.html',data=countries)




@app.route('/getstate')
def getstate():
    country_id=request.args.get('country_id')
    states=sql_query2("select id,state from state_tb where country_id=?",[country_id])
    return render_template('getstate.html',data=states)


@app.route('/registerAction',methods=['post'])
def registerAction():
    name=request.form['name']
    gender=request.form['gender']
    dob=request.form['dob']
    address=request.form['address']
    country=request.form['country']
    state=request.form['state']
    phone=request.form['phone']
    username=request.form['username']
    password=request.form['password']
    user=sql_edit_insert("insert into register_tb values(NULL,?,?,?,?,?,?,?,?,?)",(name,gender,dob,address,country,state,phone,username+'@mail.com',password))
    return render_template('register.html',msg="REGISTER SUCCSESFULL")

@app.route('/checkUsername')
def checkUsername():
    username=request.args.get('username')
    r=sql_query2("select username from register_tb where username=?",[username+'@mail.com'])
    if len(r)>0:
        check='exist'
    else:
        check='not exist'
    return jsonify({'check':check})
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginAction',methods=['post'])
def loginAction():
    username=request.form['username']
    password=request.form['password']
    user=sql_query2("select id,username,password from register_tb where username=? and password=?",(username,password))
    if len(user)>0:

        session['user_id']=user[0][0]
        return redirect(url_for('home'))
    else:
        return render_template('login.html',msg="incorrect username or password")
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/sendMessage')
def sendMessage():
    return render_template('sendmessage.html')
def username():
    user=session['user_id']
    p=sql_query2("select username from register_tb where id=?",[user])
    return p[0][0]
    
@app.route('/messageAction',methods=['post'])
def messageAction():
    r_username=request.form['r_username']
    r=sql_query2("select username from register_tb where username=?",[r_username])
    q=username()
    if len(r)>0:
       
        subject=request.form['subject']
        message=request.form['message']
        date=datetime.date.today()
        time=datetime.datetime.now().strftime("%H:%M")
        mess=sql_edit_insert("insert into message_tb values(NULL,?,?,?,?,?,?,?)",(q,r_username,subject,message,time,date,'pending'))
        return render_template('home.html',msg="message send")
    else:
        return render_template("home.html",msg="username not found")

@app.route('/recievedMessage')
def recievedMessage():
    q=username()
    
    message=sql_query2("select * from message_tb where reciever=? and status!=?",[q,'deletereciever'])
    
    return render_template('recievedmessage.html',data=message)
@app.route('/outbox')
def outbox():
    q=username()
    
    message=sql_query2("select * from message_tb where source=? and status!=?",[q,'deletesender'])
    return render_template('outbox.html',data=message)
@app.route('/reply')
def reply():
    r=request.args.get('id')
    
    message=sql_query2("select  * from message_tb where id=?",[r])
    return render_template("reply.html",data=message)

@app.route('/replyAction',methods=['post'])
def replyAction():
    q=username()
    reciever=request.form['reciever']
    message=request.form['message']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime("%H:%M")
    mess=sql_edit_insert("insert into message_tb values(NULL,?,?,?,?,?,?)",(q,reciever,'reply',message,time,date))
    
    
    return render_template('home.html',msg="replied")
@app.route('/forward')
def forward():
    r=request.args.get('id')
    message=sql_query2("select  * from message_tb where id=?",[r])
    return render_template("forward.html",data=message)
@app.route('/forwardAction',methods=['post'])
def forwardAction():
    reciever=request.form['reciever']
    r=sql_query2("select username from register_tb where username=?",[reciever])
    if len(r)>0:
        q=username()
    
        subject=request.form['subject']
        message=request.form['message']
        date=datetime.date.today()
        time=datetime.datetime.now().strftime("%H:%M")
        mess=sql_edit_insert("insert into message_tb values(NULL,?,?,?,?,?,?)",(q,reciever,subject,message,time,date))
        return render_template("home.html",msg="message forwarded")
    else:
        return render_template("forward.html",msg="username not found")

@app.route('/deletemessage')
def deletemessage():
    
    r=request.args.get('id')
    s=request.args.get('rec')
    if(s=='0'):
       
        msg=sql_query2("select status from message_tb where status=? and id=?",['deletesender',r])
        print(msg)
        if len(msg)>0:
            
            msg=sql_edit_insert("delete from message_tb where id=?",[r])
        else:
            messages=sql_edit_insert("update message_tb set status=? where id=?",['deletereciever',r])
        return redirect(url_for('recievedMessage'))
    else:
        msg=sql_query2("select status from message_tb where status=? and id=?",['deletereceiver',r])
        if len(msg)>0:
            
            msg=sql_edit_insert("delete from message_tb where id=?",[r])
        else:
            messages=sql_edit_insert("update message_tb set status=? where id=?",['deletesender',r])
        
            return redirect(url_for('outbox'))
        
        
        



if __name__=='__main__':
    app.run(debug=True)
