from cam_server.instance_management.management import InstanceManager, InstanceWrapper


class CamRecordInstanceManager(InstanceManager):

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
        return {"config": None,
                "running": False,
                "statistics": None}

    def start_camera(self, camera_name):

        if self.is_instance_present(camera_name):
            instance = self.get_instance(camera_name)

            if instance.is_running():
                return
            else:
                self.delete_instance(camera_name)

        camera = self.config_manager.get_camera(camera_name)
        instance = CamRecordInstance(camera)

        self.add_instance(camera_name, instance)
        self.start_instance(instance)

    def stop_camera(self, camera_name):
        if self.is_instance_present(camera_name):
            self.stop_instance(camera_name)
            self.delete_instance(camera_name)


class CamRecordInstance(InstanceWrapper):
    def __init__(self, camera):
        self.camera = camera