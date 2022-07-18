#!/bin/bash

gunicorn --workers 2 -k gevent linebot_with_django3_1_7.wsgi:application