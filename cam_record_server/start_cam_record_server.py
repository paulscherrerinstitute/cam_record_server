import argparse
import logging
import os

import bottle

from cam_server import CamClient
from cam_server.instance_management.configuration import ConfigFileStorage

from cam_record_server import config
from cam_record_server.configuration import CamRecordConfigManager
from cam_record_server.manager import CamRecordInstanceManager
from cam_record_server.rest_api.rest_server import register_rest_interface

_logger = logging.getLogger(__name__)


def start_record_server(host, port, config_directory, cam_server_api_address, hostname=None):
    if not os.path.isdir(config_directory):
        _logger.error("Configuration directory '%s' does not exist." % config_directory)
        exit(-1)

    if hostname:
        _logger.warning("Using custom hostname '%s'." % hostname)

    app = bottle.Bottle()

    cam_client = CamClient(cam_server_api_address)
    config_manager = CamRecordConfigManager(config_provider=ConfigFileStorage(config_directory))

    instance_manager = CamRecordInstanceManager(cam_client=cam_client, config_manager=config_manager)

    register_rest_interface(app, instance_manager)

    try:
        bottle.run(app=app, host=host, port=port)
    finally:
        instance_manager.stop_all_cameras()


def main():
    parser = argparse.ArgumentParser(description='Camera record server')
    parser.add_argument("-c", '--cam_server', default="http://0.0.0.0:8888", help="Cam server rest api address.")
    parser.add_argument('-p', '--port', default=config.DEFAULT_API_PORT, help="Server port")
    parser.add_argument('-i', '--interface', default='0.0.0.0', help="Hostname interface to bind to")
    parser.add_argument('-d', '--directory', default=config.DEFAULT_RECORD_CONFIG_FOLDER,
                        help="Record configuration base directory")
    parser.add_argument('-n', '--hostname', default=None, help="Hostname to use when returning the stream address.")

    parser.add_argument("--log_level", default=config.DEFAULT_LOGGING_LEVEL,
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        help="Log level to use.")

    arguments = parser.parse_args()

    logging.basicConfig(level=arguments.log_level)

    start_record_server(arguments.interface, arguments.port, arguments.directory, arguments.cam_server,
                        arguments.hostname)


if __name__ == "__main__":
    main()
