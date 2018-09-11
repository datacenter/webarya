#!/usr/bin/env python
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField
from flask_bootstrap import Bootstrap
import arya.arya
from argparse import ArgumentParser
import socket

app = Flask(__name__)

bootstrap = Bootstrap(app)

class DataForm(Form):
    """
    Form for inputing json/xml data
    """
    data = TextAreaField('data',)


def post_action(string):
    """
    function ran with input from POST
    :param string: string of xml or json data
    :return: string of cobra python code
    """
    fmt = arya.arya.isxmlorjson(string)
    wa = arya.arya.arya()

    if fmt == 'xml':
        return wa.getpython(xmlstr=string)
    elif fmt == 'json':
        return wa.getpython(jsonstr=string)
    else:
        raise IOError('Unsupported format passed as input. Please check ' +
                      'that input is formatted correctly in JSON or XML syntax')


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    :return: rendered web page
    """
    if request.method == 'GET':
        form = DataForm()
        sysname = socket.gethostname()
        return render_template('webarya.html', title='WebArya', form=form, hostname=sysname)
    elif request.method == 'POST':
        resp = post_action(str(request.form['data']))
        resp = resp.rstrip().split('\n')
        return render_template('completed.html',
                               title='Success',
                               data=resp)

def main():
    parser = ArgumentParser('Code generator for APIC cobra SDK')
    parser.add_argument(
        '-p', '--port', help='Port to listen on ', required=False, default=8888)
    args = parser.parse_args()
    app.secret_key = '1234'
    port = int(args.port)
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main()
