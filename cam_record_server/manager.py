class CamRecordInstanceManager(object):

    def __init__(self, cam_client, config_manager):
        self.cam_client = cam_client
        self.config_manager = config_manager

    def get_camera_list(self):
        return self.config_manager.get_camera_list()

    def get_camera_config(self, camera_name):
        return self.config_manager.get_camera_config(camera_name)

    def save_camera_config(self, camera_name, configuration):
        self.config_manager.save_camera_config(camera_name, configuration)

        camera = self.config_manager.get_camera(camera_name)

        if camera.is_auto_start():
            self.stop_camera(camera_name)
            self.start_camera(camera_name)

        return camera.get_config()

    def delete_camera_config(self, camera_name):
        deleted_config = self.config_manager.get_camera_config(camera_name)

        self.stop_camera(camera_name)
        self.config_manager.delete_camera_config(camera_name)

        return deleted_config

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

