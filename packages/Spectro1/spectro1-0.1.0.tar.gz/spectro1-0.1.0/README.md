
# Hack Academy Courses Librery

Una Biblioteca Python para consultar coursos de la academia Hack.

## Cursos disponibles:
- Introducción a Linux [15 horas]
- Personalización de Linux [3 horas]
- Introducción al Hacking [53 horas]

## Instalación 
Instala el paquete usando 'pip3':

```python3 
pip3 install courses
```

## Uso Basico

### Listar todos los cursos 

```python 
from hack import list_courses

for course in list_courses():
    print(course)
```

### Obtener curso por su nombre 

```python 
from hack import search_course_by_name

course= search_course_by_name("Introducción a Linux")
    print(course)
```

### Calcular duración total de los cursos 

```python3
from hack.utils import total_duraction

print(f"Duracion total: {total_duraction()} horas")
```
