# app/mods/bookmark/views.py

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from app import db
from . import mod
from .forms import BookmarkForm
from .models import Bookmark



@mod.route('/')
def index():
    bmList = Bookmark.query.order_by( Bookmark.title ).all()
    
    return render_template('bookmark/list.html', bookmarks=bmList)


@mod.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        qstr = request.args.get('q', default='')
    else:
        qstr = request.args['q']
    
    # Build/execute the query
    if qstr:
        qstr = '%' + qstr + '%'
        criterion = or_(
            Bookmark.url.ilike(qstr), 
            Bookmark.title.ilike(qstr), 
            Bookmark.note.ilike(qstr)
        )
        bmList = Bookmark.query.filter(criterion).all()
    else:
        bmList = Bookmark.query.all()
    
    return render_template('bookmark/list.html', bookmarks=bmList)


@mod.route('/popular/')
def popular():
    bmList = Bookmark.Select(popular=True, limit=20)
    
    return render_template('bookmark/list.html', bookmarks=bmList)


@mod.route('/tag/<name>/')
def tag(name):
    bmList = Bookmark.Select(tag=name)
    
    return render_template('bookmark/list.html', bookmarks=bmList)


@mod.route('/visit/<id>/')
def visit(id):
    bm = Bookmark.query.get_or_404(id)
    newCount = bm.bumpVisitCount()

    return redirect(bm.url)


@mod.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        form = BookmarkForm(request.args)
    else:  # POST
        form = BookmarkForm(request.form)
        if form.validate():
            bm = Bookmark('', '')
            form.populate_obj(bm)
            db.session.add(bm)
            db.session.commit()
            flash('Bookmark added', 'success')
            return redirect( url_for('bookmark.index') )
        else:
            flash('Form validation error', 'error')

    return render_template('bookmark/add.html', form=form)


@mod.route('/edit/<id>/', methods=['GET', 'POST'])
def edit(id):
    bm = Bookmark.query.get_or_404(id)
    if request.method == 'GET':
        form = BookmarkForm(None, bm)
    else:  # POST
        form = BookmarkForm(request.form, bm)
        if form.validate():
            form.populate_obj(bm)
            db.session.commit()
            flash('Bookmark saved', 'success')
            return redirect( url_for('bookmark.index') )
        else:
            flash('Form validation error', 'error')
    
    return render_template('bookmark/edit.html', form=form, bookmarkId=id)


@mod.route('/delete/<id>/')
def delete(id):
    bm = Bookmark.query.get_or_404(id)
    Bookmark.Delete(bm)
    flash('Bookmark deleted', 'success')
    
    return redirect( url_for('bookmark.index') )