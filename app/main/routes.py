from flask import render_template, request
from app.main import bp
from app.models import Snippet, User

@bp.route('/')

@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    snippets = Snippet.query.filter_by(public=True).order_by(
        Snippet.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False)
    return render_template('main/index.html', title='Home', snippets=snippets)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    language = request.args.get('language', '')
    page = request.args.get('page', 1, type=int)
    
    snippet_query = Snippet.query.filter_by(public=True)
    
    if query:
        snippet_query = snippet_query.filter(
            (Snippet.title.contains(query)) |
            (Snippet.description.contains(query)) |
            (Snippet.code.contains(query))
        )
    
    if language:
        snippet_query = snippet_query.filter_by(language=language)
    
    snippets = snippet_query.order_by(Snippet.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('main/search.html', 
                         title='Search Results',
                         snippets=snippets,
                         query=query,
                         language=language)

@bp.route('/user/<username>')
def public_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    snippets = Snippet.query.filter_by(user_id=user.id, public=True).order_by(Snippet.created_at.desc()).all()
    return render_template('user/profile.html', user=user, snippets=snippets)