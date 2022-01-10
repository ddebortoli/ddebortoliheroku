# ddebortoliheroku

API que permite acceder a un listado de usuarios y repositorios

## Comenzando 🚀

Clonar: https://github.com/ddebortoli/ddebortoliheroku.git

Para desplegar: Puede correrse en localhost o bien puede desplegarse en heroku

### Pre-requisitos 📋

requirements.txt


## Ejecutando las pruebas ⚙️

Las pruebas de esta API fueron corridas manualmente. Algunos de los casos testeados se encuentran en la carpeta images

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Principalmente usado para la construccion de metodos
* [MySql](https://flask-mysql.readthedocs.io/en/stable/) - Para la ejecucion de query's
* [Flask JWT Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - Usado para generar los tokens y manejar los metodos bloqueados
* [Flask_swagger_ui](https://pypi.org/project/flask-swagger-ui/) - Usado para manejar el swagger


## Autores ✒️

Damian Debortoli
linkedIn: https://www.linkedin.com/in/damian-debortoli/

# Metodos

## GET_Users
Metodo que obtiene usuarios de la base de datos.
El primer paso es verificar si cuenta con el token JWT. 
Caso afirmativo, obtengo los datos en base name, si name no es enviado, trae todos los usuarios
Luego logea el tipo de query hecha, la fecha y hora, y quien fue el autor.
Esto ultimo se hace mediante obtener el user_id mediante decodificacion del token jwt

## GET_repositories
Metodo que obtiene todos los repositorios, o uno especifico si se envia repository_id
El primer paso es verificar si cuenta con el token JWT. 
Caso afirmativo, obtengo los datos.
Luego logea el tipo de query hecha, la fecha y hora, y quien fue el autor.
Esto ultimo se hace mediante obtener el user_id mediante decodificacion del token jwt

## GET_Token
Metodo que retorna un token JWT si la combinacion de user y password es valida
Si faltan parametros obligatorios o la combinación es invalida, retorna un 401
Caso contrario, genera el token temporario

## GET_Logs
Metodo que retorna todos los logeos
Requiere token JWT para funcionar
Esta funcion no genera logeos dentro de su misma tabla

## Base de datos

La alta de usuarios y repositorios se lleva a cabo desde MySQL. Pero esta todo correctamente construido como para que pueda realizarse un metodo que inserte datos.
