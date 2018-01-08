import os
from flask import request
from werkzeug.utils  import secure_filename

from config import Config
from pyws import latest
from pyws.service import user_service
from pyws.helper.jsonify_response import jsonify_response
from pyws.helper.decorator import limit, validate_file, auth_required


@latest.route('/users/<user_id>/photos/', methods=['POST', 'PUT'])
@validate_file(allowed_extensions=['.png', '.jpg', '.jpeg', '.gif'])
@limit(requests=30, window=60, by="ip")
@auth_required('user_id')
def upload_user_photo(user_id):
    """
    Upload user photo

    **sample request**

        CURL -X POST 'http://localhost:5000/users/12/photos'
        -F file=@image.png
        --header "X-TOKEN: MDhjOTliMzg1Y2Q2NDA5ZTgwNzg4NGY3NjM1NTQ0M2U"

    **sample response**

        {
            "success": true
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    # save file on the server
    file_dest_rel_dir = u'user_{0}/photos/'.format(user_id)
    file_dest_full_dir = os.path.join(Config.UPLOAD_FOLDER, 'users', file_dest_rel_dir)
    os.makedirs(file_dest_full_dir, exist_ok=True)

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_rel_path = os.path.join(file_dest_rel_dir, filename)
    file_full_path = os.path.join(file_dest_full_dir, filename)
    file.save(file_full_path)

    # update user
    user_service.update_user(user, {'profile_photo': file_rel_path})

    return jsonify_response(success=True)


@latest.route('/users/<user_id>/photos/', methods=['DELETE'])
@limit(requests=30, window=60, by="ip")
@auth_required('user_id')
def delete_user_photo(user_id):
    """
    Delete user photo

    **sample request**

        CURL -X DELETE 'http://localhost:5000/users/12/photos'
        --header "X-TOKEN: MDhjOTliMzg1Y2Q2NDA5ZTgwNzg4NGY3NjM1NTQ0M2U"

    **sample response**

        {
            "success": true
        }

    """

    user = user_service.get_user_by_user_id(user_id)

    if user.profile_photo:
        os.remove(os.path.join(Config.UPLOAD_FOLDER, 'users', user.profile_photo))

    # update user
    user_service.update_user(user, {'profile_photo': None})

    return jsonify_response(success=True)
