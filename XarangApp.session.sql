SELECT column_name                  --Seleccionamos el nombre de columna
FROM information_schema.columns     --Desde information_schema.columns
WHERE table_schema = 'public'       --En el esquema que tenemos las tablas en este caso public
AND table_name   = 'banda'