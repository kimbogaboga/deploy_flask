from arbortrary_app.config.mysqlconnection import connectToMySQL
from flask import flash
from arbortrary_app.models import user

class Tree:
    db_name = 'arbortrary'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.species = db_data['species']
        self.location = db_data['location']
        self.reason = db_data['reason']
        self.date = db_data['date']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO trees (species, location, reason, date, created_at, updated_at, user_id) VALUES (%(species)s,%(location)s,%(reason)s, %(date)s, NOW(), NOW(),%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trees;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_trees = []
        for row in results:
            all_trees.append( cls(row) )
        return all_trees

    @classmethod
    def get_all_complete(cls, data):
        query = "SELECT * FROM trees JOIN users ON trees.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        new_trees = []
        if len(results) ==0:
            return new_trees
        else:
            for tree in results:
                user_data ={
                    "id": tree['users.id'],
                    "first_name": tree['first_name'],
                    "last_name": tree['last_name'],
                    "email": tree['email'],
                    "password": tree['password'],
                    "created_at": tree['users.created_at'],
                    "updated_at": tree['users.updated_at']
                }
                userhere = user.User(user_data)
                new_tree = cls(tree)
                new_tree.user_id = userhere
                new_trees.append(new_tree)
            return new_trees

    @classmethod
    def get_all_trees(cls):
        query = "SELECT * FROM trees JOIN users ON trees.user_id = users.id"
        results = connectToMySQL(cls.db_name).query_db(query)
        new_trees = []
        if len(results) ==0:
            return new_trees
        else:
            for tree in results:
                user_data ={
                    "id": tree['users.id'],
                    "first_name": tree['first_name'],
                    "last_name": tree['last_name'],
                    "email": tree['email'],
                    "password": tree['password'],
                    "created_at": tree['users.created_at'],
                    "updated_at": tree['users.updated_at']
                }
                userhere = user.User(user_data)
                new_tree = cls(tree)
                new_tree.user_id = userhere
                new_trees.append(new_tree)
            return new_trees

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM trees WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_one_complete(cls,data):
        query = "SELECT * FROM trees JOIN users ON trees.user_id = users.id WHERE trees.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        tree = cls(results[0])
        user_data ={
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        userhere = user.User(user_data)
        tree.user_id = userhere
        return tree

    @classmethod
    def update(cls, data):
        query = "UPDATE trees SET species=%(species)s, location=%(location)s, reason=%(reason)s, date =%(date)s,created_at = NOW(),updated_at=NOW(), user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM trees WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_tree(data):
        is_valid = True
        if len(data['species']) < 5:
            is_valid = False
            flash("Species must be at least 5 characters", "tree")
        if len(data['location']) < 2:
            is_valid = False
            flash("Location must be at least 2 characters", "tree")
        if len(data['reason'])> 50:
            is_valid = False
            flash("Reason must be fewer than 50 characters", "tree")
        return is_valid