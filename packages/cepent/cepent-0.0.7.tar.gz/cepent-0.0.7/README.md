# cepent

Se encuentra en construccion es una libreria para almacenar errores de procesos ETL



## Ejemplo de uso

Creando captura de error en caso de proceso rechazado

```python
from cepent import ErrorHandling

error = ErrorHandling(usr, pwd, bd_pg, bd_port, bd_company  )
error.handle_error( table_name)

```

## Ejemplo de uso

Creando captura de comienzo , error y fin de procesos de proceso. Para validar sus 3 estados

```python
from cepent import ProcessHandling

process = ProcessHandling(usr, pwd, bd_pg, bd_port, bd_company , process_name)


process.start_process_log()
process.handle_error_log( table_name)
process.end_process_log()
```
proces = ErrorHandling(usr, pwd, bd_pg, bd_port, bd_company )