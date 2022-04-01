from datetime import datetime
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

def get_time_now():
    date_str = datetime.now()
    date_str = date_str.strftime("%d-%m-%Y %H:%M:%S")
    return date_str

app = Flask(__name__)
api = Api(app)

todo_post_args = reqparse.RequestParser()
todo_post_args.add_argument("id", type=int)
todo_post_args.add_argument("title", type=str, help="Title of the todo is required", required=True)
todo_post_args.add_argument("description", type=str, help="Description of the todo is required", required=True)
todo_post_args.add_argument("finished_at", type=str)
todo_post_args.add_argument("created_at", type=str)
todo_post_args.add_argument("updated_at", type=str)
todo_post_args.add_argument("deleted_at", type=str)

todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument("title", type=str, help="Title of the todo is required")
todo_put_args.add_argument("description", type=str, help="Description of the todo is required")

todo_finish_args = reqparse.RequestParser()
todo_finish_args.add_argument("finished_at", type=str)

todo_delete_args = reqparse.RequestParser()
todo_delete_args.add_argument("deleted_at", type=str)

todos = []
        #[{'id': 5, 'title': 'Laudnry', 'description': 'Do the laundry', 'finished_at': None, 'created_at': None, 'updated_at': None, 'deleted_at': None}, 
        #{'id': 6, 'title': 'Gaming', 'description': 'Go gaming', 'finished_at': None, 'created_at': None, 'updated_at': None, 'deleted_at': None}]

def abort_if_todo_id_doesnt_exist(todo_id):
    set_of_todos_id = []
    for i in range(len(todos)):
        set_of_todos_id.append(todos[i].get('id'))
    if todo_id not in set_of_todos_id:
        abort(404, message="Could not find Todo...")

class Todos(Resource):
    def get(self):
        # allActiveTodos = todos
        # for i in range(len(allActiveTodos)-1):
        #     if allActiveTodos[i].get('deleted_at') is not None:
        #         allActiveTodos.pop(i)
        # return allActiveTodos, 200 
        return todos, 200

    def post(self):
        args = todo_post_args.parse_args()
        if todos == []:
            args.id = 0
        else: 
            args.id = (todos[(len(todos)-1)].get('id')) + 1
        args.created_at = args.updated_at = get_time_now()
        todos.append(args)
        return todos[(len(todos)-1)], 201

class SingleTodo(Resource):
    def get(self, todo_id):
        abort_if_todo_id_doesnt_exist(todo_id)
        for i in range(len(todos)):
            if todos[i].get('id') == todo_id:
                matchedTodo = todos[i]
        return matchedTodo, 200

    def put(self, todo_id):
        abort_if_todo_id_doesnt_exist(todo_id)
        args = todo_put_args.parse_args()
        args.updated_at = get_time_now()
        for i in range(len(todos)):
            if todos[i].get('id') == todo_id:
                todos[i].update(args)
                updatedTodo = todos[i]
        # todos[todo_id].update(args)
        return updatedTodo, 200

    def delete(self, todo_id):
        # abort_if_todo_exist(todo_id)
        abort_if_todo_id_doesnt_exist(todo_id)
        args = todo_delete_args.parse_args()
        args.deleted_at = get_time_now()
        for i in range(len(todos)):
            if todos[i].get('id') == todo_id:
                todos[i].update(args)
                deletedTodo = todos[i]
        # todos[todo_id].update(args)
        return deletedTodo, 200

class FinishTodo(Resource):
    def put(self, todo_id):
        abort_if_todo_id_doesnt_exist(todo_id)
        args = todo_finish_args.parse_args()
        args.finished_at = get_time_now()
        for i in range(len(todos)):
            if todos[i].get('id') == todo_id:
                todos[i].update(args)
                finishedTodo = todos[i]
        # todos[todo_id].update(args)
        return finishedTodo, 200

api.add_resource(Todos, "/todo")
api.add_resource(SingleTodo, "/todo/<int:todo_id>")
api.add_resource(FinishTodo, "/todo/<int:todo_id>/finish")

if __name__ == "__main__":
    app.run(debug=True)