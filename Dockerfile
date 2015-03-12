# https://github.com/erikdejonge/py27dock
FROM    erikdejonge/py27dock
#FROM    py27dock
WORKDIR /
RUN     git clone https://github.com/erikdejonge/puffin.git
RUN     pip install unittester
WORKDIR /puffin
#RUN     python setup.py install
