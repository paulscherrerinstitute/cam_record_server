#!/bin/bash
VERSION=0.0.1
docker build --no-cache=true -t docker.psi.ch:5000/cam_record_server .
docker tag docker.psi.ch:5000/cam_record_server docker.psi.ch:5000/cam_record_server:$VERSION
docker push docker.psi.ch:5000/cam_record_server:$VERSION
docker push docker.psi.ch:5000/cam_record_server
