#!/bin/bash

gunicorn --workers 4 -k gevent linebot_with_django3_1_7.wsgi:application