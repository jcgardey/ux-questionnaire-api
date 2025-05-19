FROM python:3.12-slim

ENV USER=api
ENV HOME=/usr/src/app
WORKDIR ${HOME}

# Create a group and user
RUN addgroup --system ${USER} --gid 1000 && adduser -u 1000 --gid 1000 ${USER} 
RUN usermod -aG sudo ${USER}

RUN apt-get update \
 && apt-get install git pkg-config gcc default-libmysqlclient-dev -y --no-install-recommends  

RUN git clone https://github.com/jcgardey/ux-questionnaire-api.git
WORKDIR ${HOME}/ux-questionnaire-api


RUN pip install -r src/requirements.txt
RUN chown -R ${USER}:${USER} /usr/src/app
RUN chmod 777 start.sh
USER ${USER} 

EXPOSE 8000
CMD ["./start.sh"] 