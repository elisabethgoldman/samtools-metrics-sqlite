# Python Project Template

## Project Init

- [ ] Update the `python_project/` example directory to the new package name. Be sure to fix imports in `__init__.py` and `__main__.py`
- [ ] Create a virtualenv for the minimum supported Python version. `Python>=3.8` should be sufficient for most projects.
- [ ] Update the `write_to` entry in `pyproject.toml`
- [ ] Update the specified lines in the `Makefile`
- [ ] Update the specified lines in `setup.cfg`
- [ ] Update the package name in `tox.ini`

## Adding or updating dependencies

New dependencies should be added to the `install_requires` section of the `setup.cfg` file.

Then, the `make requirements` command will create or update the `requirements.txt` file.

Finally, run `make init-pip` to sync the requirements to the currently activated virtualenv.

To update existing dependencies, use the `pip-tools` utility:

`pip-compile --update --upgrade-package package`

NOTE: Constrain dependency versions in the `setup.cfg` file e.g. `requests>=3.0.0`.

Libraries should never have pinned versions in the `setup.py` file.

## New and Existing Projects

When cloning or revisiting a project after some time, the `make init` command will update dependencies and pre-commit hooks.

The `make init-pip` command should be called if the `requirements.txt` file has been updated.

The `make init-hooks` command should be run whenever the `.pre-commit-config.yml` file is updated.

This make target will install the pip requirements specified in the `requirements.txt` file, install the python package under development mode, and install `pre-commit` hooks.


## Docker

This project leverages Docker multi-stage builds to provide a controlled initial test and build environment for unit and functional testing, and then a final, smaller image to install the project into.

### Dockerfile
```Dockerfile
FROM quay.io/ncigdc/python38-builder as builder

COPY ./ /opt

WORKDIR /opt

RUN pip install tox && tox -p

FROM quay.io/ncigdc/python38

COPY --from=builder /opt/dist/*.tar.gz /opt
COPY requirements.txt /opt

WORKDIR /opt

RUN pip install -r requirements.txt *.tar.gz \
	&& rm -f *.tar.gz requirements.txt

ENTRYPOINT ["python_project"]

CMD ["--help"]
```

### Build and Test Step

```Dockerfile
FROM quay.io/ncigdc/python38-builder as builder

COPY ./ /opt

WORKDIR /opt

RUN pip install tox && tox -p
```

The GDC org has created several base Python images, and the `-builder` tag here includes extras needed for testing and building Python applications.

The first step is to simply copy the full working directory into the container, setting the destination path as the working directory.

Next, tox is installed an run in order to:

1. Run unit tests
2. Run linting via `flake8`
3. Check types via `mypy`
4. Package and check the application usilng `build` and `twine`, respectfully.

This final step produces the distribution files for the project under the `/opt/dist` directory. It is the tarball in this directory that is installed into the final image:

```Dockerfile
FROM quay.io/ncigdc/python38

COPY --from=builder /opt/dist/*.tar.gz /opt
COPY requirements.txt /opt

WORKDIR /opt

RUN pip install -r requirements.txt \
	&& pip install *.tar.gz \
	&& rm -f *.tar.gz requirements.txt

ENTRYPOINT ["python_project"]

CMD ["--help"]
```

First, the smaller `python38` image is used as the new base image, while the tarball from the build image is copied into it.

The local requirements.txt file is also copied in.

Finally, the requirements and then the project itself are installed via pip.

After installation, the requirements file and tarball are no longer needed in the image and are removed to save space.

Finally, the entrypoint and default help command are set. Thus, when running this image the path to the executable is not needed.

----

# Project Name

Add a short description of your project here.

## Installation

Add any extra steps needed for installation here, including external dependencies.
