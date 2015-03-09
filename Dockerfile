FROM    erikdejonge/py2dock
WORKDIR /
RUN     git clone https://github.com/erikdejonge/puffin.git
RUN     pip install unittester
WORKDIR /puffin
#RUN     python setup.py install
