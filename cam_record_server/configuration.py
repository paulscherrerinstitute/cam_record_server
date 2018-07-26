class CamRecordConfigManager(object):

    def __init__(self, config_provider):
        self.config_provider = config_provider

    def get_camera_list(self):
        pass

    def get_camera_config(self, camera_name):
        pass

    def save_camera_config(self, camera_name, configuration):
        pass

    def delete_camera_config(self, camera_name):
        pass

    def get_camera(self, camera_name):
        camera_config = self.get_camera_config(camera_name)

        return CamRecordConfig(camera_name, camera_config)


class CamRecordConfig(object):

    MANDATORY_ATTRIBUTES = {"camera_name": str,
                            "output_stream_port": int,
                            "auto_start": bool}

    def __init__(self, camera_name, configuration):

        self.camera_name = camera_name
        self.configuration = configuration

        self.validate_config(self.configuration)

    @staticmethod
    def validate_config(configuration):
        """
        Verify if the camera record config has the mandatory attributes.
        :param configuration: Configuration to verify.
        """
        if not configuration:
            raise ValueError("Config object cannot be empty. Config: %s" % configuration)

        error = ""
        for attr_name, attr_type in CamRecordConfig.MANDATORY_ATTRIBUTES.items():
            if attr_name not in configuration:

                error += "Mandatory attribute %s missing in config. " % attr_name

                if not isinstance(configuration[attr_name], attr_type):
                    error += "Attribute %s expected of type %s. " % (attr_name, attr_type)

        if error:
            error += "Config: %s" % configuration
            raise ValueError(error)

    def is_auto_start(self):
        return self.configuration["auto_start"]

    def get_config(self):
        return self.configuration

    def get_name(self):
        return self.camera_name
