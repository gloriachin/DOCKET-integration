FROM jupyter/scipy-notebook:3deefc7d16c7

USER root
RUN mkdir /install
COPY requirements.txt /install

# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook
# jupyter/scipy-notebook comes installed with gcc
# pandas, matplotlib, scipy, seaborn, scikit-learn, cython, Click
# uses apt-get to install system packages
# uses conda to install python libraries

# subversion is needed for the svn to only download Perl data-fingerprints bin
# Perl data-fingerprints has hardcoded the location of env so softlink it
RUN apt-get update && apt-get install -y openjdk-8-jdk \
  libjson-perl libgd-perl subversion \
  && ln -s /usr/bin/env /bin/env

USER jovyan
# Add nextflow to /home/jovyan/bin so that it's in PATH
RUN mkdir /home/jovyan/bin
WORKDIR /home/jovyan/bin

RUN wget -qO- https://get.nextflow.io | bash \
&& pip install -r /install/requirements.txt

# set perl environment variables
ENV PERL_PATH=/app/data-fingerprints
ENV PERL5LIB=$PERL_PATH:$PERL_PATH/lib/perl5:$PERL5LIB
ENV PATH="/app:/home/jovyan/bin:$PERL_PATH:$PATH"

# Commented out because the directory has been committed as data-fingeprints
# Download only the Perl bin directory from gglusman/data-fingerprints to /home/jovyan
#RUN svn export https://github.com/gglusman/data-fingerprints.git/trunk/bin

COPY . /app
WORKDIR /app
