#!/usr/bin/env python
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField
import arya.arya

app = Flask(__name__)


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
def main():
    """
    :return: rendered web page
    """
    if request.method == 'GET':
        form = DataForm()
        return render_template('webarya.html', title='WebArya', form=form)
    elif request.method == 'POST':
        resp = post_action(str(request.form['data']))
        resp = resp.rstrip().split('\n')
        return render_template('completed.html',
                               title='Success',
                               data=resp)

if __name__ == '__main__':
    app.secret_key = '1234'
    app.run(host='0.0.0.0', debug=True)
