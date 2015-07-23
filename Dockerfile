FROM python:2-onbuild 
EXPOSE 8888
CMD [ "python", "./webarya/webarya.py", "-p", "8888" ]
