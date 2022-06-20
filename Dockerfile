FROM razhterize/yolov5qt:dependencies
ARG device /dev/video0:/dev/video0
ARG volume /tmp/.X11-unix:/tmp/.X11-unix
ARG network host
ARG environtment DISPLAY:${DISPLAY}

CMD [ "python3", "main.py"]