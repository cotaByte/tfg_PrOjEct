#!/bin/bash
echo "==========================================================================="
echo "actualizando repositorio backend => $(date)";
git pull -v --rebase
echo "repositorio backend actualizado => $(date)";
echo "==========================================================================="
