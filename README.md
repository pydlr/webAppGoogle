### BOLETIN JUDICIAL DEMO APP ###

Nuevos templates en este branch hay que ponerlos como demo_nombre.html.

Tomando en cuenta estos 3 datos para el demo:

Nombre, Email y password. 

Tablas:
- userinfo
- resoluciones
- usercases

Procedimientos:
- sp_create_user
- sp_validateLogin
- sp_insert_resolucion
- sp_insert_usercase
- sp delete_usercase
- sp_delete_user
- sp_insert_resolucion

BUGS y TODOs:
- Error al intentar agregar un caso que ya esta agregado - FIXED
- Cuando se hace fb login, la ventana de aprobacion aparece y desaparece sin esperar confirmacion - PARECE QUE ES NORMAL
- Error: cuando un caso tiene varias resoluciones, hay una qu se no se guarda, o no se puede encontrar. no se que pedo
- Falta notificar con correo electronico o algo
- Faltan botones para cambiar el orden de los resultados de busqueda
- Falta funcion para guardar todos los boletines anteriores
- Falta funcion para guardar el boletin de hoy y revisar si las nuevas son de interes para los usuarios
- Faltan notificaciones, poner una bandera en la gui, emails, fb chat(!?)
- Agregar reaccion de la gui de busqueda cuando se agrega un caso, que refleje que ya se agrego. O cuando se abre la pagina que muestre los casos que el usuario ya guardo antes (mas antes).
- Ampliar criterio de busqueda, para por civil, penal, etc. 
- Refinar la extraccion de info del boletin con el parser, guardar la fecha por separado etc. 
- Bootstrap: reactivo a tamaño de pantalla, iconos en botones y pestaña y fuentes
- Android gui
- Google maps


IDEAS:
- Guardar fecha del ultimo login, para despues limpiar cuentas muertas
- Idiomas?
- Notificacion por medio de fb chat