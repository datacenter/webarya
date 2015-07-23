FROM python:2-onbuild 
EXPOSE 80
CMD [ "python", "./webarya/webarya.py", "-p", "80" ]
