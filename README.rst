LibreCores.org CI Tool
======================

This is the tool to administrate LibreCores.org Continuous Integration (lcci) instances.

### Usage

TODO: Guidelines will be deployed soon

### Docker image for deploying tools

Current image version uses a hardcoded "lcci-tools" volume to deploy tools.
All available tools are listed here: https://github.com/lccitools

Install a particular tool:

```
docker run --rm -e DOCKER_HOST=${DOCKER_HOST} librecores/lcci-python lcci tools install verilator:3.902
```

Install a whole „standard tool package“:

```
docker run --rm -e DOCKER_HOST=${DOCKER_HOST} librecores/lcci-python lcci tools install lcci-2017.1
```
