from flask import Flask, Response, request, render_template, redirect, session
from elasticsearch import Elasticsearch
from time import sleep, time
import json
import os
import requests

from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean,analyzer, InnerDoc, Completion, Keyword, Text, connections,Search
from elasticsearch import Elasticsearch

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])
client = Elasticsearch()

# elastic search metadata id
id=0

#model file
class Saved(Document):
    name = Text()
    criteria = Text()
    user_id = Text()
    created_at = Date()
    class Index:
        name = 'search'

    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super().save(** kwargs)

# create the mappings in elasticsearch
Saved.init()


#es = Elasticsearch(hosts='localhost:9200')
app = Flask(__name__)


@app.route('/saved', methods=['POST'])
def create():
    global id
    id=id+1

    search_data_dict = request.json
    name=search_data_dict["name"]
    criteria=search_data_dict["criteria"]
    user_id=search_data_dict["user_id"]

    status=None
    result={}
    try:
        saved_obj = Saved(meta={'id': id}, name=name, criteria=criteria,user_id=user_id)
        saved_obj.save()
        result["message"]="saved search created successfully"
        status=200
    except Exception as e:
        status=500
        result["message"]="saved search creation process failed with exception:"+str(e)
    finally:
       resp = Response(json.dumps(result),status=status, mimetype="application/json")
    return resp

@app.route('/saved', methods=['GET'])
def read():
    search_id = request.args.get("id")
    status=None
    result={}
            
    try:
        #s = Search(using=client, index="search").query("match", id=search_id)    
        saved_obj = Saved.get(id=search_id)
        result = {"name":saved_obj.name,"criteria":saved_obj.criteria,"user_id":saved_obj.user_id}
        status=200
    except Exception as e:
        status=500
        result["message"]="saved search retrive process failed with exception:"+str(e)
    finally:
       resp = Response(json.dumps(result),status=status, mimetype="application/json")
    return result

@app.route('/saved', methods=['PUT'])
def update():
    search_id = request.args.get("id")
    data_dict=request.json
    status=None
    result={}
    try:
        # retrieve the document
        saved_obj = Saved.get(id=search_id)
        # we execute a script in elasticsearch with additional kwargs being passed
        # as params into the script
        saved_obj.update(**data_dict)
        result["message"]="search updated successfully"
        status=200
    except Exception as e:
        status=500
        result["message"]="saved search update process failed with exception:"+str(e)
    finally:
       resp = Response(json.dumps(result),status=status, mimetype="application/json")
    return resp

@app.route('/saved', methods=['DELETE'])
def delete():
    search_id = request.args.get("id")
    status=None
    result={}
    try:
        # retrieve the document
        saved_obj = Saved.get(id=search_id)
        saved_obj.delete()
        result["message"]="search id deleted successfully"
        status=200
    except Exception as e:
        status=500
        result["message"]="saved search delete process failed with exception:"+str(e)
    finally:
       resp = Response(json.dumps(result),status=status, mimetype="application/json")
    return resp


if __name__ == '_main_':
    app.run(debug=True, port=5000)

