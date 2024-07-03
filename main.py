from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '18e4101a9db0ec1bdb23c4c9ec11cfeb'
app.debug = True
toolbar = DebugToolbarExtension(app)

@app.route("/")                          # this tells you the URL the method below is related to
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')        # this prints HTML to the webpage

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page', text='This is the about page')
  
if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")