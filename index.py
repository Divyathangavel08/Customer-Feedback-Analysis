from flask import Flask, render_template, flash, request 
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from textblob import TextBlob #ML package
import mysql.connector #mysql connector

# App config.
DEBUG = True
app = Flask(__name__) #intilizing flask
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form): #class definiton
    name = TextField('Name:', validators=[validators.required()]) #for validation purpose
    email = TextField('Email:', validators=[validators.required()])
    phone = TextField('Phone:',validators=[validators.required()])
    feedback = TextField('Feedback:',validators=[validators.required()])
    
    @app.route('/shopping/login')
    def index():
        return render_template('login.html')
    @app.route('/shopping/about')
    def about():
        return render_template('about.html')
    @app.route('/shopping/product')
    def product():
        return render_template('product.html')
    @app.route('/shopping/blog')
    def blog():
        return render_template('blog.html')
    @app.route('/shopping/contact')
    def contact():
        return render_template('contact.html')   
    @app.route("/shopping", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
    
        print(form.errors)
        if request.method == 'POST':#getting values from form
            name=request.form['name']
            email=request.form['email']
            phone=request.form['phone']
            feedback=request.form['feedback']
            print(name," ",email," ",phone," ",feedback)
    
        if form.validate():
            # Save the comment here.
            edu=TextBlob(feedback)
            x=edu.sentiment.polarity
            ans=None
            # Negative = x<e and Neutral = 0 and Positive x>0 && x=edu.sentiment.polarity
            if x<0:
                ans = "Negative"
            elif x==0:
                ans = "Neutral"
            elif x>0 and x<=1:
                ans = "Positive"
                
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password="",
              database="shopping"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO details VALUES (%s, %s, %s, %s, %s)" #inserting values in detail table
            val = (name,email,int(phone),feedback,ans)

            mycursor.execute(sql, val)

            mydb.commit()
            
            flash('feedback submitted successfully')
        else:
            flash('All the form fields are required. ')
    
        return render_template('index.html', form=form)# viewing html index page

class Form2(Form):
    email = TextField('Email:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required()])
    
    @app.route("/shopping/details", methods=['GET', 'POST'])
    def login1():
        form = Form2(request.form)
    
        print(form.errors)
        if request.method == 'POST':
            email=request.form['email']
            password=request.form['password']
            print(email," ",password)
        result='login.html'
        data=None
        ans=[]
        count1=0
        count2=0
        count3=0
        if form.validate():
            if email=='divyaadmin@gmail.com' and password=='divya123':
                mydb1 = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="shopping"
                )

                mycursor1 = mydb1.cursor()

                mycursor1.execute("Select * from details")

                data = mycursor1.fetchall()
                for i in data:
                    if i[4]=="Positive":
                        count1=count1+1
                    elif i[4]=="Negative":
                        count2=count2+1
                    elif i[4]=="Neutral":
                        count3=count3+1
                ans.append(count1)
                ans.append(count2)
                ans.append(count3)
                result = 'details.html'
            else:
                flash('Invalid login credentials')
        else:
            flash('All the form fields are required. ')
            
        return render_template(result,data=data,ans=ans)
        
if __name__ == "__main__":
    app.run()