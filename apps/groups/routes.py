from flask import Blueprint


groups = Blueprint('groups', __name__, url_prefix='/groups')


@groups.route('/', methods=['GET'])
def list_groups():
    return "test"