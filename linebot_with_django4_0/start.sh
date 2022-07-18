#!/bin/bash

gunicorn --workers 4 -k gevent linebot_with_django4_0.wsgi:application