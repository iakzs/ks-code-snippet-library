from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from app import db
from app.snippets import bp
from app.snippets.forms import SnippetForm
from app.models import Snippet
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = SnippetForm()
    if form.validate_on_submit():
        snippet = Snippet(
            title=form.title.data,
            code=form.code.data,
            description=form.description.data,
            language=form.language.data,
            public=form.public.data,
            author=current_user
        )
        db.session.add(snippet)
        db.session.commit()
        flash('Your snippet has been created!', 'success')
        return redirect(url_for('snippets.view', slug=snippet.slug))
    return render_template('snippets/editor.html', title='Create Snippet', form=form)

@bp.route('/<slug>')
def view(slug):
    snippet = Snippet.query.filter_by(slug=slug).first_or_404()
    if not snippet.public and not (current_user.is_authenticated and (snippet.can_modify(current_user))):
        abort(404)
    
    try:
        if snippet.language != 'other':
            lexer = get_lexer_by_name(snippet.language)
        else:
            lexer = guess_lexer(snippet.code)
    except:
        lexer = guess_lexer(snippet.code)
    
    formatter = HtmlFormatter(linenos=True, cssclass='syntax-highlight')
    highlighted_code = highlight(snippet.code, lexer, formatter)
    css = formatter.get_style_defs('.syntax-highlight')
    
    snippet.increment_views()
    
    return render_template('snippets/view.html',
                         title=snippet.title,
                         snippet=snippet,
                         highlighted_code=highlighted_code,
                         css=css)

@bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    snippet = Snippet.query.filter_by(slug=slug).first_or_404()
    if not snippet.can_modify(current_user):
        abort(403)
    
    form = SnippetForm()
    if form.validate_on_submit():
        snippet.title = form.title.data
        snippet.code = form.code.data
        snippet.description = form.description.data
        snippet.language = form.language.data
        snippet.public = form.public.data
        snippet.generate_slug()
        db.session.commit()
        flash('Your snippet has been updated!', 'success')
        return redirect(url_for('snippets.view', slug=snippet.slug))
    elif request.method == 'GET':
        form.title.data = snippet.title
        form.code.data = snippet.code
        form.description.data = snippet.description
        form.language.data = snippet.language
        form.public.data = snippet.public
    return render_template('snippets/editor.html', title='Edit Snippet', form=form)

@bp.route('/<slug>/delete')
@login_required
def delete(slug):
    snippet = Snippet.query.filter_by(slug=slug).first_or_404()
    if not snippet.can_modify(current_user):
        abort(403)
    db.session.delete(snippet)
    db.session.commit()
    flash('Your snippet has been deleted!', 'success')
    return redirect(url_for('main.index'))
