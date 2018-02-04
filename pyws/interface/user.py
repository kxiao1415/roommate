from flask import g, request, render_template

from pyws import latest
from pyws.email import email_helper
from pyws.service import user_service, auth_service
from pyws.helper.jsonify_response import jsonify_response
from pyws.helper.decorator import limit, validate_json, auth_required
from pyws.helper import data_helper
from pyws.helper import string_helper
from pyws.cache import cache_helper
from pyws.data.model.user_model import UserModel
from pyws.data.model.preference_model import PreferenceModel
from config import Config


@latest.route('/users/authenticate/', methods=['POST'])
@validate_json(required_fields=['email', 'password'])
@limit(requests=100, window=60, by="ip")
def authenticate_user():
    """
    Authenticate user

    **sample request**

        curl -X POST 'http://localhost:5000/users/authenticate/'
        --header "Content-Type: application/json"
        --data '{
                    "email": "test_user_email",
                    "password": "password"
                }


    **sample response**

        {
            "token": "Y2QyYjJlYTMxMjA1NDMwMTg5ZDJhMDhlYjk1MTU1Yjg"
        }

    """

    user_email = request.json['email']
    password = request.json['password']

    token = auth_service.authenticate_user(user_email, password)
    return jsonify_response(token=token)


@latest.route('/users/<user_id>', methods=['GET'])
@limit(requests=100, window=60, by="ip")
def get_user(user_id):
    """
    Get a user by user id

    **sample request**

        curl -X GET 'http://localhost:5000/users/1'

    **sample response**

        {
            "user": {
                "education": null,
                "created_time": "2017-12-17T03:59:16.782856",
                "budget_min": null,
                "id": 1,
                "email": "test@gmail.com",
                "short_description": null,
                "gender": null,
                "long_description": null,
                "age_last_modified": "2017-12-17T03:59:16.782865",
                "budget_max": null,
                "user_name": "test_user_name",
                "age": null,
                "phone": null,
                "deleted": false,
                "last_deleted_time": "2017-12-17T03:59:16.782865",
                "profile_photo": "example/path/to/photo.png",
                "preference": {
                    "gender": "F",
                    "education": "H",
                    "age_group": "25-30"
                }
            }
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    if user is None:
        raise Exception('Invalid user id.')

    return jsonify_response(user=user.to_json(filter_hidden_columns=True))


@latest.route('/users/', methods=['GET'])
@limit(requests=100, window=60, by="ip")
def get_qualified_users():
    """
    Get all users that fit the filter criteria

    **sample request**

        curl -X GET 'http://localhost:5000/users/?age_group=35-40&gender=M'

    **sample response**

        {
            "users":
                [
                    {
                        "education": null,
                        "created_time": "2017-12-17T03:59:16.782856",
                        "budget_min": null,
                        "id": 1,
                        "email": "test@gmail.com",
                        "short_description": null,
                        "gender": null,
                        "long_description": null,
                        "age_last_modified": "2017-12-17T03:59:16.782865",
                        "budget_max": null,
                        "user_name": "test_user_name",
                        "age": null,
                        "phone": null,
                        "deleted": false,
                        "last_deleted_time": "2017-12-17T03:59:16.782865",
                        "profile_photo": "example/path/to/photo.png",
                        "preference": {
                                          "gender": "F",
                                          "education": "H",
                                          "age_group": "25-30"
                                      }
                    },
                    {
                        "education": null,
                        "created_time": "2017-12-17T03:59:16.782856",
                        "budget_min": null,
                        "id": 1,
                        "email": "test@gmail.com",
                        "short_description": null,
                        "gender": null,
                        "long_description": null,
                        "age_last_modified": "2017-12-17T03:59:16.782865",
                        "budget_max": null,
                        "user_name": "test_user_name",
                        "age": null,
                        "phone": null,
                        "deleted": false,
                        "last_deleted_time": "2017-12-17T03:59:16.782865",
                        "profile_photo": "example/path/to/photo.png",
                        "preference": {
                                          "gender": "F",
                                          "education": "H",
                                          "age_group": "25-30"
                                      }
                    }
                ]
            }
        }

    """
    individual_preference = {}
    shared_preference = {}

    for filter in PreferenceModel.individual_preference_columns():
        filter_value = request.args.get(filter, default=None)
        if filter_value:
            individual_preference[filter] = filter_value

    for filter in PreferenceModel.shared_preference_columns():
        filter_value = request.args.get(filter, default=None)
        if filter_value:
            shared_preference[filter] = filter_value

    page = request.args.get('page', default=1)

    users = user_service.get_qualified_users(individual_preference, shared_preference, page=page)
    return jsonify_response(users=[user.to_json(filter_hidden_columns=True) for user in users])


@latest.route('/users/', methods=['POST'])
@validate_json(required_fields=UserModel.required_columns(), allowed_model=UserModel)
@limit(requests=100, window=60, by="ip")
def create_user():
    """
    Create a new user

    **sample request**

        curl -X POST 'http://localhost:5000/users/'
        --header "Content-Type: application/json"
        --data '{
                    "email": "test@email.com",
                    "user_name": "test_user_name",
                    "preference": {
                                      "gender": "F",
                                      "education": "H",
                                      "age_group": "25-30"
                                  }
                }'

    **sample response**

        {
            "user": {
                "education": null,
                "created_time": "2017-12-17T03:59:16.782856",
                "budget_min": null,
                "id": 1,
                "email": "test@gmail.com",
                "short_description": null,
                "gender": null,
                "long_description": null,
                "age_last_modified": "2017-12-17T03:59:16.782865",
                "budget_max": null,
                "user_name": "test_user_name",
                "age": null,
                "phone": null,
                "deleted": false,
                "last_deleted_time": "2017-12-17T03:59:16.782865",
                "profile_photo": "example/path/to/photo.png",
                "preference": {
                    "gender": "F",
                    "education": "H",
                    "age_group": "25-30"
                }
            }
        }

    """

    user_info = request.json
    data_helper.clean_info(UserModel, user_info)
    new_user = user_service.create_user(user_info)

    if new_user and Config.SEND_EMAIL:
        email_helper.send_email(
            [new_user.email],
            render_template('welcome_email_subject.txt'),
            render_template('welcome_email_body.txt', user=new_user),
            render_template('welcome_email_body.html', user=new_user)
        )

    return jsonify_response(user=new_user.to_json(filter_hidden_columns=True))


@latest.route('/users/<user_id>', methods=['PUT'])
@validate_json(allowed_model=UserModel)
@limit(requests=100, window=60, by="ip")
@auth_required('user_id')
def update_user(user_id):
    """
    Update a user

    **sample request**

        curl -X PUT 'http://localhost:5000/users/1'
        --header "Content-Type: application/json"
        --header "X-TOKEN: MDhjOTliMzg1Y2Q2NDA5ZTgwNzg4NGY3NjM1NTQ0M2U"
        --data '{
                    "email": "test@email.com",
                    "user_name": "test_user_name",
                    "preference": {
                                      "gender": "F",
                                      "education": "H",
                                      "age_group": "25-30"
                                  }
                }'

    **sample response**

        {
            "success": true
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    if not user:
        raise Exception('Invalid user id.')

    user_info = request.json
    data_helper.clean_info(UserModel, user_info)

    # to update password, user '/reset_password/' end point
    if 'password' in user_info:
        raise Exception('Please refer to /reset_password/ end point for password update')

    user_service.update_user(user, user_info)

    return jsonify_response(success=True)


@latest.route('/password_reset_email/', methods=['GET'])
@limit(requests=100, window=60, by="ip")
def send_password_reset_email():
    """
    Send user password reset email if the email exists

    **sample request**

        curl -X GET 'http://localhost:5000/password_reset_email/?email=test@test.com'

    **sample response**

        {
            "success"=True
        }

    """

    user_email = request.args.get('email', default=None)

    user = user_service.get_user_by_user_email(user_email)

    if user:
        # create password reset token
        token = string_helper.generate_guid()

        # store password reset token in redis
        cache_helper.cache_password_reset_key(user, token)

        # generate the password reset url to be included in the email
        password_reset_url = 'http://localhost:5000/reset_password/?token={token}'.format(token=token)

        # send email
        email_helper.send_email(
                [user_email],
                render_template('password_reset_email_subject.txt'),
                render_template('password_reset_email_body.txt',
                                user_name=user.user_name,
                                link=password_reset_url),
                render_template('password_reset_email_body.html',
                                user_name=user.user_name,
                                link=password_reset_url)
            )

    return jsonify_response(success=True)


@latest.route('/reset_password/', methods=['GET'])
@limit(requests=100, window=60, by="ip")
def get_reset_password_page():
    # if valid_reset_token:
    #
    # else:
    #
    pass


@latest.route('/users/<user_id>/password', methods=['PUT'])
@validate_json(required_fields=['password'])
@limit(requests=100, window=60, by="ip")
def reset_password(user_id):
    """
    Reset password

    **sample request**

        curl -X PUT 'http://localhost:5000/users/121/password_reset/'
        --header "Content-Type: application/json"
        --header "X-TOKEN: MDhjOTliMzg1Y2Q2NDA5ZTgwNzg4NGY3NjM1NTQ0M2U"
        --data '{
                    "password": "test password"
                }'

    **sample response**

        {
            "success": true
        }

    """

    is_valid_token = cache_helper.validate_password_reset_token(user_id, g.token)

    if not is_valid_token:
        raise Exception('The password reset token is not valid for user {0}'.format(user_id))

    user = user_service.get_user_by_user_id(user_id)

    if not user:
        raise Exception('Invalid user id.')

    password = request.json['password']

    user_service.update_user(user, {'password': password})

    return jsonify_response(success=True)


@latest.route('/users/<user_id>', methods=['DELETE'])
@auth_required('user_id')
def hard_delete_user(user_id):
    """
    Hard delete a user by user id

    !!!Important!!!

    This end point should not be exposed to public

    **sample request**

        curl -X DELETE 'http://localhost:5000/users/1'
        --header "Content-Type: application/json"
        --header "X-TOKEN: MDhjOTliMzg1Y2Q2NDA5ZTgwNzg4NGY3NjM1NTQ0M2U"

    **sample response**

        {
            "success": true
        }

    """

    user = user_service.get_user_by_user_id(user_id, include_deleted=True)

    if not user:
        raise Exception('Invalid user id.')

    result = user_service.hard_delete_user(user)
    return jsonify_response(success=result)
