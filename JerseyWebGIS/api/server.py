from flask import Flask, request, g
from flask_sock import Sock
from flask_cors import CORS,cross_origin
from orm.TypeSystem import DataBaseHanlder
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from json import loads

app = Flask(__name__)
sock = Sock(app)
cors = CORS(app)
global theHandler
theHandler = DataBaseHanlder()


@app.route('/category', methods=['POST', 'GET'])
@cross_origin()
def handler_category():
    """
    HTTP-POST:
        body:
        [
        {
            "name":"Position",
            "specification":[
                {"keyName":"Latitude","keyCategory":"Double"},{"keyName":"Longitude","keyCategory":"Double"}
            ],
            "isGeometry":false
        }
        ]
    :return:
    """
    global theHandler
    if request.method == 'GET':
        return theHandler.Get_Categories(), 200
    if request.method == 'POST':
        def removeIsGeometry(ele: dict):
            ele.pop('isGeometry')
            return ele

        postData = loads(request.data)
        print(postData)
        isgeometries = []
        for ele in postData:
            isgeometries.append(ele['isGeometry'])
        theCategories, theIsGeometries = (
            [category for category in map(removeIsGeometry, postData)],
            isgeometries,
        )

        theHandler.Add_Categories(categories=theCategories, isGeometry=theIsGeometries)
        return "Success", 200
    return "Are you use right HTTP method?", 404


@app.route('/data', methods=['POST'])
@cross_origin()
def handler_category_add_data():
    """
    POST-BODY:
    [
        {
        "name":"Position",
        "data":[
            {
                "Latitude":233,"Longitude":111
            }
        ]
        }
    ]
    """
    global theHandler
    if request.method == 'POST':
        postData = loads(request.data)
        for one_add_data in postData:
            theHandler.Add_Data(
                one_add_data['name'],
                one_add_data['data']
            )
        return "Success", 200
    return "Are you use right HTTP method?This port only support POST", 404

@app.route('/data/query',methods=['POST'])
@cross_origin()
def handler_category_data_query():
    """
    POST-BODY:
    {
        "category":"Position",
        "query":{
            "Latitude":233
        }
    }
    @metion:query is a json object
    :return:
    """
    global theHandler
    if request.method == 'POST':
        postData = loads(request.data)
        return theHandler.Get_Data_ByCondition(
            category_name=postData["category"],
            condition=postData["query"]
        )

@app.route('/data/batch', methods=['POST'])
@cross_origin()
def handler_category_data_batch_get():
    """
    POST-BODY:
    [
    {
        "category":"","num":-1
    }
    ]
    :return:
    {
        "category_name":[thedata],
        "DEFAULT":[

        ]
    }
    """
    global theHandler
    if request.method == 'POST':

        postData = loads(request.data)
        result = {}
        for one_request in postData:
            result[one_request["category"]] = theHandler.Get_Data_ByNums(
                category_name=one_request["category"],
                num=one_request["num"]
            )
        return result


@app.route('/default/<default_name>')


@sock.route("/config")
def handler_config(ws):
    while True:
        data = ws.receive()
        config = loads(data)
        with open('./config.json','w+') as f:
            f.write(str(config))
            ws.send("done")


@app.errorhandler(DBAPIError)
def catch_DBAPI_Error(e):
    return "Error occur in DataBaseHandler:{error}".format(error=e), 500


@app.errorhandler(SQLAlchemyError)
def catch_SQLAlchemy_Error(e):
    return "Error occur in DataBaseHandler:{error}".format(error=e), 500


@app.errorhandler(404)
def handler_404(e):
    return "Resources not exist", 404



# def get_api_flask_app(shared_db_path):
#
#     app = Flask(__name__)
#
#     @app.route('/topic/<tid>')
#     def getTopicWithComments(tid):
#         results = {key: value for key, value in
#                    DataBaseConnector(db=str(shared_db_path.value,encoding="utf-8")).queryTopicWithComments(tid).items()}
#         return results
#
#     @app.route('/topic/versions/<tid>')
#     def getTopics(tid):
#         results = DataBaseConnector(db=str(shared_db_path.value,encoding="utf-8")).queryTopic(tid=tid)
#         return {
#             'results': results
#         }
#     return app


if __name__ == "__main__":
    app.run(debug=True,port=1211)
