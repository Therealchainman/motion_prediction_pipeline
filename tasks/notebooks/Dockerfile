FROM toddchaney/motion_prediction_base:latest
RUN pip install jupyterlab

RUN mkdir ~/.jupyter
RUN echo "c.NotebookApp.token = ''" >>~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.password = ''" >>~/.jupyter/jupyter_notebook_config.py

RUN mkdir /data
WORKDIR /data
