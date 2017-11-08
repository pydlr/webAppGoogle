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

BUGS y TODOs:
- Error cuando buscas con un numero cualquiera (123/234 esta bien porque tiene diagonal)
- Error al intentar agregar un caso que ya esta agregado
- Agregar reaccion de la gui de busqueda cuando se agrega un caso, que refleje que ya se agrego. O cuando se abre la pagina que muestre los casos que el usuario ya guardo antes (mas antes).
- Bootstrap: reactivo a tamaño de pantalla, iconos en botones y pestaña y fuentes
- Android gui
- Google maps
