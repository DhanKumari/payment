from . import db
from flask import Blueprint, abort
from flask_restful import Resource,reqparse,fields, marshal_with
from .models import TodoModel
from youtube import api
from youtube import db

todoapiB= Blueprint('todoapi',__name__)

class HelloWorld(Resource):
    def get(self):
        return {'data':'hello,World'}



# todolist={
#     1:{"task":"hii first item","summary":"hii first item"}
# }



task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task",type=str, help="task is required", required=True)
task_post_args.add_argument("summary",type=str, help="summary is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task",type=str)
task_put_args.add_argument("summary",type=str)

#return the todo model db 
resource_fields ={
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String,

}

class Todo1(Resource):
    @marshal_with(resource_fields)
    def get(self):
        t_data = TodoModel.query.all()
        return t_data
        # todo={}
        # for task in tasks:
        #     todo[task.id]={"task":t_data.task,"summary":t_data.summary}


class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        t_data = TodoModel.query.filter_by(id=todo_id).first()
        if not t_data:
            abort(404," id not present ")
        return t_data

        # if todo_id not in todolist:
        #     abort(404," id not present ")
        # return todolist[todo_id]

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        t_data = TodoModel.query.filter_by(id=todo_id).first()
        if t_data:
            abort(409, "task id  is already present")
        todo= TodoModel(id=todo_id, task=args['task'],summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
        # if todo_id in todolist:
        #     abort(409, "task is already present")
        # todolist[todo_id] = {"task":args["task"],"summary":args["summary"]}
        # return todolist[todo_id]
    
    @marshal_with(resource_fields)
    def put(self,todo_id):
        args = task_put_args.parse_args()
        t_data = TodoModel.query.filter_by(id=todo_id).first()
        if  not t_data:
            abort(409, "task id  is not  present")
        if args['task']:
            t_data.task = args['task']
        if args['summary']:
            t_data.summary = args['summary']
        db.session.commit()
        return t_data
            
        # if todo_id not in todolist:
        #     abort(404,"id not present ")
        # if args['task']:
        #     todolist[todo_id]['task'] = args['task']
        # if args['summary']:
        #     todolist[todo_id]['summary'] =args['summary']
        # return todolist[todo_id]

    def delete(self,todo_id):
        t_data = TodoModel.query.filter_by(id=todo_id).first()
        db.session.delete(t_data)
        db.session.commit()
        return {"message":"todo deleted"},206
        d
        # del todolist[todo_id]
        # return {"data":"obj deletedS"}


#apiiii link 
api.add_resource(HelloWorld,'/helloworld')
api.add_resource(Todo,'/todo/<int:todo_id>/')
api.add_resource(Todo1,'/todoall')
# api.add_resource(Todo,'/todo')
