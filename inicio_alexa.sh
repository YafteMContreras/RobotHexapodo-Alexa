#! /usr/bin/bash

echo "---------------------------------------------------------" >> /home/Cesarin/log_script.txt
echo "Script de inicio ejecutandose el $(date)" >> /home/Cesarin/log_script.txt

mensaje="Ejecutando..."

cd

source bluedot_env/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]];
then
	echo "Entorno virtual activado: $VIRTUAL_ENV" >> /home/Cesarin/log_script.txt
#	lxterminal -e "echo $mensaje && bash"
	cd /home/Cesarin/Alexa/Server
	python3 subscriber.py
	echo "Programa de python ejecutandose el $(date)" >> /home/Cesarin/log_script.txt
else
	echo "No se pudo activar el entorno virtual"
fi
exit 0
