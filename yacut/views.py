from flask import flash, redirect, render_template, url_for

from . import app
from .consts import SHORT_FUNCTION_NAME
from .error_handlers import URLMapException
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['POST', 'GET'])
def add_link_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    short_link = form.custom_id.data
    try:
        link_record = URLMap().db_writer(
            original_link, short_link
        )
    except URLMapException:
        flash('Имя {0} уже занято!'.format(short_link))
        return render_template('index.html', form=form)
    full_short_link = url_for(
        SHORT_FUNCTION_NAME, short_url=link_record.short, _external=True
    )
    return render_template(
        'index.html',
        form=form,
        full_short_link=full_short_link
    )


@app.route('/<string:short_url>')
def link_redirect_view(short_url):
    link_record = URLMap.query.first_or_404(short_url)
    return redirect(link_record.original)
