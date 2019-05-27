from flask import Flask, redirect, url_for, request, render_template
from flask_table import Table, Col

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('radiobutton.html')


@app.route('/change', methods = ['POST', 'GET'])
def change():
    boolean = False
    if request.method=='POST':
        print('hello world')
        user_answer = request.form['options']
        if user_answer == "Compound":
            boolean = True
        else:
            boolean = False
        print(user_answer)
        return boolean
    

if __name__ == '__main__':
    app.run()
