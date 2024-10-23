import os
from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import *
from .rando import CodeGenerator
class CodeGenerationForm(FlaskForm):
    seed = IntegerField()
    gct = BooleanField("Generate GCT")
    submit = SubmitField()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap = Bootstrap4(app)
    csrf = CSRFProtect(app)
    codegen = CodeGenerator()

    current_gct_bytes = b''

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = CodeGenerationForm()
        current_codestring = ""
        if form.validate_on_submit():
            flash('Generating Code!')
            codegen = CodeGenerator()
            seed = form.seed.data
            codegen.gen_code(seed)
            current_codestring = codegen.get_code_text()
            current_gct_bytes = codegen.get_gct_bytes()
            redirect(url_for('index'))
        return render_template('rando_gen.html', form=form,current_codestring=current_codestring)





    return app