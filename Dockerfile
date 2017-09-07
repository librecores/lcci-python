FROM librecores/librecores-ci
LABEL Description="LCCI Python Image" Vendor="LibreCores project" Version="0.1"

VOLUME /tools

WORKDIR /home/lcci-python
COPY ./ /home/lcci-python

RUN python setup.py build
RUN python setup.py install

COPY lcci.sample.yml /home/lcci-python/lcci.yml
