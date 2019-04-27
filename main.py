import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    
@app.route('/create/', methods=['GET', 'POST'])
def create():
        if request.method == 'POST':
            try:
                name = Donor.select().where(Donor.name == request.form['name']).get()
                donation = Donation(value=request.form['value'], donor=name)
                donation.save()
            
                return redirect(url_for('all'))
            except:
                return render_template('create.jinja2', error='Donor is not the database')
        
        else:
            return render_template('create.jinja2')

@app.route('/new/', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        newname = Donor.create(name=request.form['newname'])
        donation = Donation(value=request.form['value'], donor=newname)
        donation.save()
        return redirect(url_for('all'))
    
    else:
        return render_template('new.jinja2')
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

