from flask import Flask, render_template, url_for, flash, redirect, request
import func as custom
from forms import RegistrationForm, LoginForm
from werkzeug import secure_filename
from sqlalchemy import create_engine
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.secret_key = 'damageassessment'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
posts = [
    {
        'author': 'Vala',
        'title': 'Web App to retrieve information of the residential properties',
        'date_posted': 'August 7, 2019'
    },
]

@app.route("/", methods=['GET', 'POST'])

@app.route("/home")
def Home():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    #         flash('You have been logged in!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('home.html', title='Home Page')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('about'))
    return render_template('register.html', title='Register', form=form)





@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if f.filename =='':
          flash('No Selected file')
          return redirect('upload.html')
      else:
          f.save(f'static/user-photo/{secure_filename(f.filename)}')
          master_results = custom.master_query(f'static/user-photo/{secure_filename(f.filename)}')
          name = str(time.time())
          os.rename('static/google-pics/gsv_0.jpg',f'static/google-pics/{name}.jpg')




      #
      # engine = create_engine('postgres://elfmuvhdhailnu:47c793a2d65fff982391c49abae7608c68adc66897919402fb73155dd67a5964@ec2-107-22-228-141.compute-1.amazonaws.com:5432/da22vfv1epa332')
      #
      # connection = engine.connect()
      # sql = f"""
      # INSERT INTO Property_info
      # values({master_results['zillow_id']},
      # {master_results['address']}',
      # {master_results['home_type']}')
      # {master_results['year_built']},
      # {master_results['property_size']},
      # {master_results['home_size']},
      # {master_results['bathrooms']},
      # {master_results['bedrooms']},
      # {master_results['last_sold_date']}',
      # {master_results['last_sold_price']},
      # {master_results['zestimate_amount']}
      # )
      # """
      # connection.execute(sql)


   return render_template('uploader.html',
   zillow_id = master_results['zillow_id'],
   home_type = master_results['home_type'],
   year_built = master_results['year_built'],
   property_size = master_results['property_size'],
   home_size = master_results['home_size'],
   bathrooms = master_results['bathrooms'],
   bedrooms = master_results['bedrooms'],
   last_sold_date = master_results['last_sold_date'],
   last_sold_price = master_results['last_sold_price'],
   zestimate_amount = master_results['zestimate_amount'],
   address = master_results['address'],
   filename = f.filename,
   name =name
   )

@app.route('/submitted', methods= ['GET','POST'])
def submitted():
    return render_template('submitted.html', title='Submitted')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run(debug=True)
