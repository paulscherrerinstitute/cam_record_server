import requests

from cam_record_server import config


def validate_response(server_response):
    if server_response["state"] != "ok":
        raise ValueError(server_response.get("status", "Unknown error occurred."))

    return server_response


class CamRecordClient(object):
    def __init__(self, address="http://sf-daqsync-02:%d/" % config.DEFAULT_API_PORT):
        """
        :param address: Address of the cam API, e.g. http://localhost:10000
        """

        self.api_address_format = address.rstrip("/") + config.API_PREFIX + "%s"
        self.address = address

    def get_rest_address(self):
        """
        Return the REST api endpoint address.
        """
        return self.address

    def get_camera_list(self):
        """
        List existing camera configurations.
        """
        rest_endpoint = "/camera"

        server_response = requests.get(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["cameras"]

    def get_camera_config(self, camera_name):
        """
        Get the config associated with a camera.
        :param camera_name: Name of the camera.
        :return: Config.
        """
        rest_endpoint = "/camera/%s" % camera_name

        server_response = requests.get(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["config"]

    def save_camera_config(self, camera_name, configuration):
        """
        Save or overwrite camera config.
        :param camera_name: Camera to save the config to.
        :param configuration: Config to save, in dictionary format.
        :return: Saved config.
        """
        rest_endpoint = "/camera/%s" % camera_name

        server_response = requests.put(self.api_address_format % rest_endpoint, json=configuration).json()
        return validate_response(server_response)["config"]

    def delete_camera_config(self, camera_name):
        """
        Delete config of camera.
        :param camera_name: Camera to delete.
        :return: Deleted config.
        """
        rest_endpoint = "/camera/%s" % camera_name

        server_response = requests.delete(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["config"]

    def get_server_info(self):
        """
        Return the info of the cam record server instance. For administrative purposes only.
        :return: Status of the server
        """
        rest_endpoint = "/server"
        server_response = requests.get(self.api_address_format % rest_endpoint).json()

        return validate_response(server_response)["info"]

    def start_all_cameras(self):
        """
        Start all cameras.
        :return: Server info.
        """
        rest_endpoint = "/server"

        server_response = requests.put(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["info"]

    def stop_all_cameras(self):
        """
        Stop all cameras.
        :return: Server info.
        """
        rest_endpoint = "/server"

        server_response = requests.delete(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["info"]

    def get_camera_info(self, camera_name):
        """
        Return the info of the camera instance. For administrative purposes only.
        :return: Status of the camera.
        """
        rest_endpoint = "/server/%s" % camera_name
        server_response = requests.get(self.api_address_format % rest_endpoint).json()

        return validate_response(server_response)["info"]

    def start_camera(self, camera_name):
        """
        Start the camera.
        :param camera_name: Name of the camera to start.
        :return: Camera instance info.
        """
        rest_endpoint = "/server/%s" % camera_name

        server_response = requests.put(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["info"]

    def stop_camera(self, camera_name):
        """
        Stop the camera.
        :param camera_name: Name of the camera to stop.
        :return: Camera instance info.
        """
        rest_endpoint = "/server/%s" % camera_name

        server_response = requests.delete(self.api_address_format % rest_endpoint).json()
        return validate_response(server_response)["info"]
