import os, json
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from KeywordMatch import keywordMatch
from fileHandler import readPdf
from remainingkeywordPairs import getRemainingKeywordPairs
app = Flask(__name__)


class ReusableForm(Form):
    # Form which takes title, description and url['Grants.gov']
    title = StringField('Title*:  ', validators=[validators.required()])
    description = TextAreaField('Description*: ', validators=[validators.required()])
    backgroundInformation = TextAreaField('Background Information:')
    URL = StringField('URL: (Grants.gov URL) ')


UPLOAD_FOLDER = 'uploads/'  # upload folder
ALLOWED_EXTENSIONS = set(['pdf', 'txt', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/fileupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("keywords" + file.filename[-4:])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('read'))
    return render_template("fileUpload.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/readpdf')
def read():
    readPdf()
    return render_template("readPdf.html")


@app.route("/", methods=['GET', 'POST'])
def Form():
    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        backgroundInformation = request.form['backgroundInformation']
        url = request.form['URL']
        if form.validate():
            keywords = keywordMatch(title, description, backgroundInformation)
            keywordPairs = getRemainingKeywordPairs(keywords)
            return render_template('addFA.html', title=title, description=description, url=url, keywords=keywords,
                                   keywordPairs=keywordPairs)
        else:
            print('All the form fields are required. ')
    elif request.method == 'GET':
        return render_template('index.html', form=form)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        return render_template('keywordFinder.html', title=['vivek'], keywords=['hello'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)