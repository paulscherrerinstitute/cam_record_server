[![Build Status](https://travis-ci.org/datastreaming/cam_record_server.svg?branch=master)](https://travis-ci.org/datastreaming/cam_record_server)

# Camera record server
Cam record server is bsread based streaming proxy that acts as an interface between cam_server and the ImageBuffer.
It needs to convert a PUB/SUB stream to a PUSH/PULL and make all the data in the stream ImageBuffer compliant.

# Table of content
1. [Quick start](#quick_start)
2. [Build](#build)
    1. [Conda setup](#conda_setup)
    2. [Local build](#local_build)
    3. [Docker build](#docker_build)
3. [Basic concepts](#basic_concepts)
4. [Configuration](#configuration)
5. [Web interface](#web_interface)
    1. [Python client](#python_client)
    2. [REST API](#rest_api)
6. [Running the servers](#running_the_servers)
7. [Production configuration](#production_configuration)
8. [Examples](#examples)
9. [Deploy in production](#deploy_in_production)


<a id="quick_start"></a>
## Quick start    


<a id="build"></a>
## Build

<a id="conda_setup"></a>
### Conda setup
If you use conda, you can create an environment with the cam_record_server library by running:

```bash
conda create -c paulscherrerinstitute --name <env_name> cam_record_server
```

After that you can just source you newly created environment and start using the server.

<a id="local_build"></a>
### Local build
You can build the library by running the setup script in the root folder of the project:

```bash
python setup.py install
```

or by using the conda also from the root folder of the project:

```bash
conda build conda-recipe
conda install --use-local cam_record_server
```

#### Requirements
The library relies on the following packages:

- cam_server

In case you are using conda to install the packages, you might need to add the **paulscherrerinstitute** channel to
your conda config:

```
conda config --add channels paulscherrerinstitute
```

<a id="docker_build"></a>
### Docker build
**Warning**: When you build the docker image with **build.sh**, your built will be pushed to the PSI repo as the
latest cam_record_server version. Please use the **build.sh** script only if you are sure that this is what you want.

To build the docker image, run the build from the **docker/** folder:
```bash
./build.sh
```

Before building the docker image, make sure the latest version of the library is available in Anaconda.

**Please note**: There is no need to build the image if you just want to run the docker container.
Please see the [Docker Container](#run_docker_container) chapter.


<a id="basic_concepts"></a>
## Basic concepts

<a id="configuration"></a>
## Configuration


<a id="web_interface"></a>
## Web interface

<a id="python_client"></a>
### Python client

<a id="rest_api"></a>
### REST API

<a id="running_the_servers"></a>
## Running the servers


<a id="production_configuration"></a>
## Production configuration

The production configurations are not part of this repository but are available on:
- https://git.psi.ch/controls_highlevel_applications/cam_server_configuration

You can download it using git:
```bash
git clone https://git.psi.ch/controls_highlevel_applications/cam_server_configuration.git
```

And later, when you start the docker container, map the configuration using the **-v** parameter:
```bash
docker run --net=host -it -v /CURRENT_DIR/cam_server_configuration/configuration:/configuration docker.psi.ch:5000/cam_server
```

**WARNING**: Docker needs (at least on OSX) a full path for the -v option. Replace the **CURRENT\_DIR** with your
actual path.

<a id="examples"></a>
## Examples

<a id="deploy_in_production"></a>
## Deploy in production

Before deploying in production, make sure the latest version was tagged in git (this triggers the Travis build) and
that the Travis build completed successfully (the new cam_record_server package in available in anaconda). 
After this 2 steps, you need to build the new version of the docker image (the docker image checks out the latest 
version of cam_record_server from Anaconda). The docker image version and the cam_record_server version should always 
match - If they don't, something went wrong.

### Production configuration
Login to the target system, where cam_record_server will be running. Checkout the production configuration into the root
of the target system filesystem.

```bash
cd /
git clone https://git.psi.ch/controls_highlevel_applications/cam_server_configuration.git
```

### Setup the cam_record_server as a service
On the target system, copy **docker/cam_record_server.service** into **/etc/systemd/system**.

Then need to reload the systemctl daemon:
```bash
systemctl daemon-reload
```

### Verifying the configuration
On the target system, copy **docker/validate_configs.sh** into your home folder.
Run it to verify if the deployed configurations are valid for the current version of the cam_record_server.

```bash
./validate_configs.sh
```

### Run the servers
Using systemctl you then run both servers:
```bash
systemctl start cam_record_server.service
```

### Inspecting server logs
To inspect the logs for each server, use journalctl:
```bash
journalctl -u cam_record_server.service
```

Note: The '-f' flag will make you follow the log file.
