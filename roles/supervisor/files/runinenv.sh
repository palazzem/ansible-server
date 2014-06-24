#!/bin/bash
VENV=$1
if [ -z $VENV ]; then
    echo "usage: runinenv [virtualenv_path] CMDS"
    exit 1
fi
. ${VENV}/bin/activate

if [ -f ${VENV}/bin/postactivate ]; then
    . ${VENV}/bin/postactivate
fi

shift 1
#echo "Executing $@ in ${VENV}"
exec "$@"

deactivate

if [ -f ${VENV}/bin/postdeactivate ]; then
    . ${VENV}/bin/postdeactivate
fi
