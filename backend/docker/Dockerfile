FROM python:3.9

WORKDIR /app
#Clonar repositorio
RUN git clone https://github.com/palmaAvenger/tfg_PrOjEct.git
#COPY requirements.txt requirements.txt
#Instalar requerimientos
RUN pip install --no-cache-dir -r tfg_PrOjEct/backend/requirements.txt

#Instalar cron
RUN apt-get update
RUN apt-get -y install cron
RUN apt-get -y install coreutils

#Dar permisos de ejecucion al shell script
RUN chmod +x tfg_PrOjEct/backend/pull_job_backend.sh

#Add al crontab el job pull
RUN crontab -l | ( cat; echo "* * * * 5 /app/tfg_PrOjEct/backend/pull_job_backend.sh >> /app/messages 2>&1;" ) | crontab -
RUN /etc/init.d/cron start

#Exponer puerto 5000
EXPOSE 5000
#Arrancamos servicios
CMD cron
CMD ["python3.9","tfg_PrOjEct/backend/main_server.py"]
