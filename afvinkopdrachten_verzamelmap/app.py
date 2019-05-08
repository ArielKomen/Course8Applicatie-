from flask import Flask, render_template
from flask import request
import mysql.connector


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('test template.html')


@app.route('/<input_a>', methods=['POST'])
def hello_world(input_a):
    output = []
    conn = mysql.connector.connect(
        host = "ensembldb.ensembl.org",
        user = "anonymous",
        db = "homo_sapiens_core_95_38")
    cursor = conn.cursor()
    cursor.execute("""select gene_id, description
    from homo_sapiens_core_95_38.gene
    where lower(description) like %s""", ("%" + request.form['input_a'] + "%",))

    rows = cursor.fetchall()
    #print(rows)
    for row in rows:
        nieuwe_regel = str(row[1].replace(request.form['input_a'] ,"<b>" + request.form['input_a'] + "</b>"))
        output.append(nieuwe_regel+"\n")
    return render_template('test template.html', input=output)


if __name__ == '__main__':
    app.run()
