
## Primera Inspeccion

Al finalizar la primera inspección en Sonarqube, se presentaron varios issues desde problemas de seguridad, código repetido y problemas en los template por lo tanto hemos dividido esto en dos partes: Seguridad y General.

## Seguridad

En el apartado de Seguridad habían problemas con las llaves de Api al ser subidas a un directorio público por lo tanto el código que se encuentra subido ahora no posee las llaves, estas se guardarán para uso de pruebas locales.
Otro problema presente era en el apartado de views que las funciones de request no presentaban un método de seguridad para el acceso, por lo cual se editó y agregó medidas seguras para pedir requests. Estas se aceptan automáticamente si es que nos encontramos en un apartado local.

## Templates

Con respecto a los templates, se hizo una limpieza y arreglos de headers y htmls para no tuvieran problemas.

## Re-Inspeccion

Luego de esta revisión y de limpiar código repetido, la re-inspección nos arroja un resultado positivo.

## Issues Presentes
Sin embargo, aun quedan issues por resolver las cuales presentan problemas mas para las funciones que posee la pagina que se resolveran mas a futuro.
