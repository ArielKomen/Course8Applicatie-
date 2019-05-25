from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/<output>', methods = ['POST'])
def verwerk_output(output):
    print(request.form["submit"])
    return output
    #eerst achterhalen welke knop is ingedrukt.



@app.route('/', methods=['GET'])
def main():
    combinatie_lijst = maak_combinatie_lijst()
    html_lijst = zooi(combinatie_lijst)

    return render_template('webpage.html', input=html_lijst)

def maak_combinatie_lijst():
    compound_data = "/home/cole/Documents/course_8/weektaken/textmining applicatie/data/compound lijst"
    ziekte_data = "/home/cole/Documents/course_8/weektaken/textmining applicatie/data/ziekte lijst"
    boolean = False

    if boolean == False:
        combinatie_lijst = make_compound_ziekte_combinatie_lijst(compound_data, ziekte_data)
    else:
        combinatie_lijst = make_ziekte_compound_combinatie_lijst(compound_data, ziekte_data)

    return combinatie_lijst


def make_compound_ziekte_combinatie_lijst(compound_data, ziekte_data):
    # in deze functie er voor zorgen dat er een combinatielijst gemaakt wordt tussen ziekte en compound
    combinatie_lijst = []
    combinatie_dict = {}
    ziekte_lijst = make_ziekte_lijst(ziekte_data)
    compound_lijst = make_compound_lijst(compound_data)

    for ziekte in ziekte_lijst[0:]:
        combinatie_dict[ziekte] = compound_lijst[0:]
        combinatie_lijst.append(combinatie_dict)
        combinatie_dict = {}

    return combinatie_lijst


def make_ziekte_compound_combinatie_lijst(compound_data, ziekte_data):
    # in deze functie er voor zorgen dat er een combinatielijst gemaakt wordt tussen compound en ziekte
    combinatie_lijst = []
    combinatie_dict = {}
    ziekte_lijst = make_ziekte_lijst(ziekte_data)
    compound_lijst = make_compound_lijst(compound_data)
    for compound in compound_lijst[0:]:
        combinatie_dict[compound] = ziekte_lijst[0:]
        combinatie_lijst.append(combinatie_dict)
        combinatie_dict = {}

    return combinatie_lijst


def make_ziekte_lijst(ziekte_data):
    ziekte_lijst = []
    for regel in open(ziekte_data):
        regel = regel.strip()
        if regel != "":
            ziekte_lijst.append(regel)

    return ziekte_lijst


def make_compound_lijst(compound_data):
    compound_lijst = []
    for regel in open(compound_data):
        regel = regel.strip()
        if regel != "":
            compound_lijst.append(regel)

    return compound_lijst


def zooi(combinatie_lijst):
    html_lijst = []
    opteller = 0
    speciale_opteller = 0

    # html_lijst.append('<ul>')
    html_lijst.append('<div class="btn-group-vertical">')
    for item in combinatie_lijst:

        html_lijst.append('<button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#Flask_applicatie_'+str(opteller)+ '" aria-expanded="false" aria-controls="Flask_applicatie">' + list(item.items())[0][0] + "</button>")
        html_lijst.append('<div class ="collapse" id="Flask_applicatie_'+str(opteller)+'">')

        html_lijst.append('<div class="card card-body">')
        html_lijst.append('<div class="btn-group-vertical">')
        for lijst in item.values():
            for woord in lijst:
                #<form action="/input_a" method="POST">
                #html_lijst.append('<input type="submit" name="output" value="output_'+str(speciale_opteller)+'" >')
                #html_lijst.append('<input type="button" name="ouput_'+str(speciale_opteller)+'" >')
                html_lijst.append('<button type="button" class="btn btn-secondary">'+woord+'</button>')
                #html_lijst.append(woord)
                #html_lijst.append('</li>')
                speciale_opteller += 1
        speciale_opteller = 0
        html_lijst.append('</div>')
        html_lijst.append('</div>')
        html_lijst.append('</div>')
        opteller += 1
    html_lijst.append('</div>')
    #for item in html_lijst:
        #print(item)
    return html_lijst

if __name__ == '__main__':
    app.run()
