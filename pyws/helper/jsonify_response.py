import json
from pyws import app

def jsonify_response(status_code=200, *args, **kwargs):

    json_response = json.dumps(dict(*args, **kwargs))
    response = app.response_class(json_response,
                                  mimetype='application/json')
    response.status_code = status_code

    return response
