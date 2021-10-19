from flask import render_template,redirect,session,request, flash
from arbortrary_app import app
from arbortrary_app.models.tree import Tree
from arbortrary_app.models.user import User


@app.route('/new/tree')
def new_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_tree.html',user=User.get_by_id(data))


@app.route('/create/tree',methods=['POST'])
def create_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/dashboard')
    data = {
        "species": request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date": request.form["date"],
        "user_id": session["user_id"],
    }
    Tree.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_tree(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",tree=Tree.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/tree',methods=['POST'])
def update_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/edit/<int:id>')
    data = {
        "species": request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date": request.form["date"],
        "user_id": session["user_id"],
        "id": request.form['id']
    }
    Tree.update(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show(id):
    from datetime import datetime 
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }  
    return render_template('show.html', user=User.get_by_id(user_data), tree = Tree.get_one_complete(data))

@app.route('/user/account')
def mytrees():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }  
    return render_template('mytrees.html', user=User.get_by_id(user_data), alltrees = Tree.get_all_complete(user_data))


@app.route('/destroy/tree/<int:id>')
def destroy_tree(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Tree.destroy(data)
    return redirect('/user/account')