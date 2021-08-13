from flask import Flask,render_template,request,redirect,make_response
import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import random
r=requests.get("https://www.indiatoday.in/health")
soup=BeautifulSoup(r.text,'html.parser')
results=soup.find_all('div',attrs={'class':'detail'})
results1=soup.find_all('h2')
headings=[]
content=[]
for i in range(6):
  headings.append(results1[i].text)
  results2=results[i].find_all('p')
  content.append(results2[0].text)

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///patients.db'
db=SQLAlchemy(app)
class Patients(db.Model):
    id=db.Column(db.String(100),primary_key=True)
    pan=db.Column(db.Integer,nullable=False)
    pname=db.Column(db.String(200),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow())
    pmno=db.Column(db.Integer,nullable=False)
    dname=db.Column(db.String(200),nullable=False)
    page=db.Column(db.Integer,nullable=False)
    hin=db.Column(db.Integer,nullable=False)
    ddes=db.Column(db.Text)
    #pimg=db.Column(db.Text,nullable=False)

@app.route('/')
def index():
    return render_template("practice.html",head=headings,content=content)

@app.route('/home')
def home():
    return render_template("practice.html", head=headings, content=content)

@app.route('/personalize')
def personalize():
    return render_template("personalize.html")

@app.route('/fitness')
def fit():
    return render_template("fitness.html")

@app.route('/nutrition')
def health():
    return render_template("nutrition.html")
@app.route('/activities')
def activity():
    return render_template("activities.html")

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        hin=request.form['hin']
        pan=request.form['pan']
        pname=request.form['pname']
        pmno=request.form['pmno']
        page=request.form['page']
        dname=request.form['dname']
        ddes=request.form['ddes']
        #pimg=request.files['pic']
        #pimg=secure_filename(pimg.filename)
        patient=Patients(id=str(random.randint(1220,70000000))+str(random.randint(0,1220)),hin=hin,pan=pan,pname=pname,page=page,pmno=pmno,dname=dname,ddes=ddes)
        try:
            db.session.add(patient)
            db.session.commit()
            return redirect('/personalize')
        except:
            return "<center><h2 style='font-size:18px;font-family:cursive;color:grey;'>There was an error while registering please try again!</h2></center>"
@app.route('/check',methods=['POST','GET'])
def check():
    if request.method=='POST':
        pan = request.form['pan']
        print(pan)
        pmno = request.form['pmno']
        try:
            patient = Patients.query.filter_by(pan=pan).order_by(Patients.page).all()
            if len(patient)>0:
                return render_template('display.html', patient=patient)
            else:
                return "<center><h2 style='font-size:18px;font-family:cursive;color:grey;'>No Records Found!</h2></center>"
        except:
            return "<center><h2 style='font-size:18px;font-family:cursive;color:grey;'>No Records Found!</h2></center>"

if __name__=="__main__":
    app.run(debug=True)
