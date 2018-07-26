import os
import signal
import unittest
from multiprocessing import Process
from time import sleep

from cam_record_server import config, start_cam_record_server
from cam_record_server.rest_api.rest_client import CamRecordClient


# TODO: Mock the instance manager.
class TestRestInterface(unittest.TestCase):
    def setUp(self):
        self.host = "0.0.0.0"
        self.port = config.DEFAULT_API_PORT

        self.process = Process(target=start_cam_record_server,
                               args=(self.host, self.port, "config_dir", "localhost"))
        self.process.start()

        # Give it some time to start.
        sleep(0.5)

        server_address = "http://%s:%s" % (self.host, self.port)
        self.client = CamRecordClient(server_address)

    def tearDown(self):
        self.client.stop_all_cameras()
        os.kill(self.process.pid, signal.SIGINT)

        # Wait for the server to die.
        sleep(1)

    def test_interface(self):
        # TODO: Actually test something.

        camera_name = "simulation"

        cameras = self.client.get_camera_list()
        config = self.client.get_camera_config(camera_name)
        config = self.client.save_camera_config(camera_name)
        config = self.client.delete_camera_config(camera_name)

        camera_info = self.client.get_camera_info(camera_name)
        camera_info = self.client.start_camera(camera_name)
        camera_info = self.client.stop_camera(camera_name)

        server_info = self.client.get_server_info()
        server_info = self.client.start_all_cameras()
        server_info = self.client.stop_all_cameras()



