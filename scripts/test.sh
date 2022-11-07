#!/usr/bin/env bash
set -ex
coverage run --source='.' todo/manage.py test "$@"
coverage report

