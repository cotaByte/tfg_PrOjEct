#!/bin/bash

echo $0
pwd
cd `dirname $0`
echo "==========================================================================="
echo "actualizando repositorio backend => $(date)";
git pull -v --rebase
echo "repositorio backend actualizado => $(date)";
echo "==========================================================================="
