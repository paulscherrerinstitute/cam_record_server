import json
import logging

import bottle
from bottle import request, response

from cam_record_server import config

_logger = logging.getLogger(__name__)


def register_rest_interface(app, instance_manager, api_prefix=None):
    """
    Get the rest api server.
    :param app: Bottle app to register the interface to.
    :param instance_manager: Manager for the server.
    :param api_prefix: Prefix to put before commands in URL.
    """

    if api_prefix is None:
        api_prefix = config.API_PREFIX

    @app.get(api_prefix + "/camera")
    def get_camera_list():
        return {"state": "ok",
                "status": "List of recorded cameras.",
                "cameras": instance_manager.get_camera_list()}

    @app.get(api_prefix + "/camera/<camera_name>")
    def get_camera_config(camera_name):
        return {"state": "ok",
                "status": "Info for camera %s." % camera_name,
                "config": instance_manager.get_camera_config(camera_name)}

    @app.put(api_prefix + '/camera/<camera_name>')
    def save_camera_config(camera_name):
        return {"state": "ok",
                "status": "Camera %s configuration saved." % camera_name,
                "config": instance_manager.save_camera_config(camera_name, request.json)}

    @app.delete(api_prefix + '/camera/<camera_name>')
    def delete_camera_config(camera_name):
        return {"state": "ok",
                "status": "Camera %s configuration deleted." % camera_name,
                "config": instance_manager.delete_camera_config(camera_name)}

    @app.get(api_prefix + "/server")
    def get_server_info():
        return {"state": "ok",
                "status": "Server info.",
                "info": instance_manager.get_server_info()}

    @app.put(api_prefix + "/server")
    def start_all_cameras():
        return {"state": "ok",
                "status": "Cameras started.",
                "info": instance_manager.start_all_cameras()}

    @app.delete(api_prefix + "/server")
    def stop_all_cameras():
        return {"state": "ok",
                "status": "Cameras stopped.",
                "info": instance_manager.stop_all_cameras()}

    @app.get(api_prefix + "/server/<camera_name>")
    def get_camera_info(camera_name):
        return {"state": "ok",
                "status": "Camera %s info." % camera_name,
                "info": instance_manager.get_camera_info(camera_name)}

    @app.put(api_prefix + '/server/<camera_name>')
    def start_camera(camera_name):
        instance_manager.start_camera(camera_name)

        return {"state": "ok",
                "status": "Camera %s stream started." % camera_name,
                "info": instance_manager.start_camera(camera_name)}

    @app.delete(api_prefix + '/server/<camera_name>')
    def stop_camera(camera_name):
        instance_manager.stop_camera(camera_name)

        return {"state": "ok",
                "status": "Camera %s stream stopped." % camera_name,
                "info": instance_manager.stop_camera(camera_name)}

    @app.error(405)
    def method_not_allowed(res):
        if request.method == 'OPTIONS':
            new_res = bottle.HTTPResponse()
            new_res.set_header('Access-Control-Allow-Origin', '*')
            new_res.set_header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
            new_res.set_header('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type')
            return new_res
        res.headers['Allow'] += ', OPTIONS'
        return request.app.default_error_handler(res)

    @app.hook('after_request')
    def enable_cors():
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    @app.error(500)
    def error_handler_500(error):
        response.content_type = 'application/json'
        response.status = 200

        return json.dumps({"state": "error",
                           "status": str(error.exception)})
