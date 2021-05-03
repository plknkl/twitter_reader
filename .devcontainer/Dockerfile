FROM jupyter/scipy-notebook

USER root
RUN apt update
RUN apt install -y libpq-dev
USER $NB_UID