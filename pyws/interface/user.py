from flask import request

from pyws import latest
from pyws.service import user_service, auth_service
from pyws.helper.jsonify_response import jsonify_response
from pyws.helper.decorator import limit, validate_json, auth_required
from pyws.helper import data_helper
from pyws.data.model.user_model import UserModel


@latest.route('/users/authenticate/', methods=['POST'])
@validate_json('user_name', 'password')
@limit(requests=30, window=60, by="ip")
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


@latest.route('/users/<user_id>', methods=['GET'])
@limit(requests=30, window=60, by="ip")
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
        raise Exception('Invalid user id.')

    return jsonify_response(user=user.to_json(filter_hidden_columns=True))


@latest.route('/users/', methods=['POST'])
@validate_json(*UserModel.required_columns())
@limit(requests=30, window=60, by="ip")
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

    clean_user_info = data_helper.filter_private_columns(UserModel, request.json)
    new_user = user_service.create_user(clean_user_info)

    return jsonify_response(new_user=new_user.to_json(filter_hidden_columns=True))


@latest.route('/users/<user_id>', methods=['PUT'])
@validate_json()
@limit(requests=30, window=60, by="ip")
@auth_required('user_id')
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
        raise Exception('Invalid user id.')

    clean_user_info = data_helper.filter_private_columns(UserModel, request.json)
    updated_user = user_service.update_user(user, clean_user_info)

    return jsonify_response(updated_user=updated_user.to_json(filter_hidden_columns=True))


@latest.route('/users/<user_id>', methods=['DELETE'])
@limit(requests=30, window=60, by="ip")
@auth_required('user_id')
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
        raise Exception('Invalid user id.')

    result = user_service.delete_user(user)
    return jsonify_response(deleted=result)
