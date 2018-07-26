class CamRecordInstanceManager(object):

    def __init__(self, cam_client, config_manager):
        self.cam_client = cam_client
        self.config_manager = config_manager

    def get_camera_list(self):
        pass

    def get_camera_config(self, camera_name):
        pass

    def save_camera_config(self, camera_name, configuration):
        pass

    def delete_camera_config(self, camera_name):
        pass

    def get_server_info(self):
        pass

    def start_all_cameras(self):
        pass

    def stop_all_cameras(self):
        pass

    def get_camera_info(self, camera_name):
        pass

    def start_camera(self, camera_name):
        pass

    def stop_camera(self, camera_name):
        pass

