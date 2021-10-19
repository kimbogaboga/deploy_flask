from arbortrary_app import app

from arbortrary_app.controllers import users_controllers, trees_controllers

if __name__=="__main__":
    app.run(debug=True)