# Import important imports from flask
from flask import Flask, render_template,\
                  request, \
                  session, redirect
# Import Python imports
from decouple import config

# Get secret keys from a hidden .env file
secret_key = config('SECRET_KEY')

# Init our app flask object
app = Flask(__name__)
app.secret_key = secret_key

# Define routes below
@app.route('/')
def index_method():
    # Create the context to pass to the page
    context = {
        'page_title': 'Welcome!'
    }
    return render_template('index.html', context=context)

# Start the app
if __name__ == '__main__':
    app.run(debug=True, port=8888)