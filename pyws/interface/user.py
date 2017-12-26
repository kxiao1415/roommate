from flask import request

from pyws import app
from pyws.service import user_service, auth_service
from pyws.helper.jsonify_response import jsonify_response


@app.route('/users/authenticate/', methods=['POST'])
def authenticate_user():
    """
    Authenticate user

    **sample request**

        curl -X POST 'http://localhost:5000/users/authenticate/'
        --header "Content-Type: application/json"
        --data '{
                    "user_name": "test_user_name",
                    "password": "password"
                }


    **sample response**

        {
            "token": "Y2QyYjJlYTMxMjA1NDMwMTg5ZDJhMDhlYjk1MTU1Yjg"
        }

    """
    user_name = request.json['user_name']
    password = request.json['password']

    token = auth_service.authenticate_user(user_name, password)
    return jsonify_response(token=token)


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a user by user id

    **sample request**

        curl -X GET 'http://localhost:5000/users/1'

    **sample response**

        {
            "user": {
                "last_name": "test_last_name",
                "education": null,
                "created": "2017-12-17T03:59:16.782856",
                "budget_min": null,
                "id": 1,
                "email": "test@gmail.com",
                "short_description": null,
                "gender": null,
                "long_description": null,
                "age_last_modified": "2017-12-17T03:59:16.782865",
                "budget_max": null,
                "user_name": "test_user_name",
                "estimated_age": null,
                "phone": null,
                "first_name": "test_first_name"
            }
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    if user is None:
        raise Exception('Invalid user id')

    return jsonify_response(user=user.to_json())


@app.route('/users/', methods=['POST'])
def create_user():
    """
    Create a new user

    **sample request**

        curl -X POST 'http://localhost:5000/users/'
        --header "Content-Type: application/json"
        --data '{
                    "email": "test@email.com",
                    "first_name": "test_first_name",
                    "last_name": "test_last_name",
                    "user_name": "test_user_name"
                }'

    **sample response**

        {
            "user": {
                "last_name": "test_last_name",
                "education": null,
                "created": "2017-12-17T03:59:16.782856",
                "budget_min": null,
                "id": 1,
                "email": "test@gmail.com",
                "short_description": null,
                "gender": null,
                "long_description": null,
                "age_last_modified": "2017-12-17T03:59:16.782865",
                "budget_max": null,
                "user_name": "test_user_name",
                "estimated_age": null,
                "phone": null,
                "first_name": "test_first_name"
            }
        }

    """

    new_user_info = request.json
    new_user = user_service.create_user(new_user_info)
    return jsonify_response(new_user=new_user.to_json())


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user

    **sample request**

        curl -X PUT 'http://localhost:5000/users/1'
        --header "Content-Type: application/json"
        --data '{
                    "email": "test@email.com",
                    "first_name": "test_first_name",
                    "last_name": "test_last_name",
                    "user_name": "test_user_name"
                }'

    **sample response**

        {
            "user": {
                "last_name": "test_last_name",
                "education": null,
                "created": "2017-12-17T03:59:16.782856",
                "budget_min": null,
                "id": 1,
                "email": "test@gmail.com",
                "short_description": null,
                "gender": null,
                "long_description": null,
                "age_last_modified": "2017-12-17T03:59:16.782865",
                "budget_max": null,
                "user_name": "test_user_name",
                "estimated_age": null,
                "phone": null,
                "first_name": "test_first_name"
            }
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    if not user:
        raise Exception('Invalid user id')

    user_info = request.json
    updated_user = user_service.update_user(user, user_info)

    return jsonify_response(updated_user=updated_user.to_json())


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by user id

    **sample request**

        curl -X DELETE 'http://localhost:5000/users/1'

    **sample response**

        {
            "deleted": true
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    if not user:
        raise Exception('Invalid user id')

    result = user_service.delete_user(user)
    return jsonify_response(deleted=result)
