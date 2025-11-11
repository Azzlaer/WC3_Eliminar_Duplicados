Buscador de Archivos Duplicados (GUI en Python)

## ??? Capturas de Pantalla

![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/01.png)
![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/02.png)
![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/03.png)
![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/04.png)


?? DESCRIPCI車N
Este programa es una herramienta con interfaz gr芍fica (GUI) desarrollada en Python que permite buscar y eliminar archivos duplicados dentro de una carpeta seleccionada. Utiliza el algoritmo de hash SHA-256 para identificar archivos con contenido id谷ntico, sin importar su nombre.
El proyecto es una conversi車n mejorada del script original en Batch (BAT), integrando funcionalidades modernas y una interfaz amigable basada en Tkinter.

?? CARACTER赤STICAS PRINCIPALES
- Interfaz Gr芍fica (GUI): desarrollada con Tkinter.
- Selecci車n de carpeta: el usuario puede elegir f芍cilmente la ruta a analizar.
- C芍lculo de hashes SHA-256: asegura una comparaci車n precisa entre archivos.
- Detecci車n de duplicados: muestra todos los archivos duplicados encontrados.
- Eliminaci車n controlada: permite borrar duplicados dejando una copia por grupo de hash.
- Modo simulaci車n: ejecuta el an芍lisis sin borrar archivos.
- LOG en vivo: muestra un registro detallado de todas las acciones realizadas.
- Exportaci車n de informe: genera un archivo con nombre REGISTRO_DD_MM_AAAA.log.
- Barra de progreso: indica el avance del an芍lisis.
- Multihilo: evita bloqueos de la interfaz durante el an芍lisis.

?? REQUISITOS DEL SISTEMA
- Python 3.7 o superior
- Librer赤as est芍ndar de Python (no requiere instalaci車n adicional)
Opcional:
- send2trash (si se desea mover los duplicados a la papelera en lugar de borrarlos)
pip install send2trash



?? INSTRUCCIONES DE USO
- Ejecutar la aplicaci車n:
python buscador_duplicados_gui.py
- Seleccionar carpeta:
- Presiona "Seleccionar" y elige la carpeta donde buscar duplicados.
- Marca o desmarca "Incluir subcarpetas" seg迆n tus necesidades.
- Analizar archivos:
- Pulsa el bot車n "Analizar".
- Se mostrar芍n los archivos duplicados en el panel izquierdo.
- El panel derecho mostrar芍 el registro (LOG) en tiempo real.
- Eliminar duplicados:
- Si se encuentran duplicados, activa "Simular eliminaci車n" para hacer una prueba sin borrar.
- Pulsa "Eliminar duplicados" para borrar los duplicados, manteniendo una sola copia de cada grupo.
- Exportar informe:
- Al finalizar, puedes guardar el log en un archivo .log con nombre tipo REGISTRO_10_11_2025.log.

?? ESTRUCTURA DEL PROYECTO
?? Proyecto  
念岸岸 buscador_duplicados_gui.py   # Script principal de la aplicaci車n  
弩岸岸 README.md                    # Este archivo  



?? FUNCIONAMIENTO INTERNO
- Recorre todos los archivos en la carpeta seleccionada (y subcarpetas, si est芍 activado).
- Calcula el hash SHA-256 de cada archivo.
- Registra cada hash en memoria; si un hash ya existe, el archivo se marca como duplicado.
- Muestra los duplicados en la interfaz.
- Permite eliminar los duplicados (manteniendo una copia) y registra los resultados en el LOG.

?? EJEMPLO DE SALIDA DE LOG
[2025-11-10 14:23:01] Iniciando an芍lisis en: D:\Juegos\Blizzard\Warcraft III\Maps\Download  
[2025-11-10 14:23:03] Nuevo hash: a3c56f9e1b7d... -> D:\Juegos\Blizzard\Warcraft III\Maps\Download\map1.w3x  
[2025-11-10 14:23:04] Duplicado encontrado (hash a3c56f9e1b7d...): D:\Juegos\Blizzard\Warcraft III\Maps\Download\map1_copy.w3x  
[2025-11-10 14:23:06] Total de archivos analizados: 542  
[2025-11-10 14:23:06] Archivos duplicados encontrados: 8  
[2025-11-10 14:23:10] Eliminado: D:\Juegos\Blizzard\Warcraft III\Maps\Download\map1_copy.w3x  
[2025-11-10 14:23:11] Script finalizado correctamente.  


?? NOTAS ADICIONALES
- Los archivos se eliminan de forma permanente, a menos que se active el modo de simulaci車n o se implemente send2trash.
- Los informes (.log) se guardan en la ubicaci車n que el usuario elija.
- Es posible detener la ejecuci車n cerrando la ventana.

?? Licencia
Este proyecto se distribuye bajo licencia MIT, lo que permite su uso, copia y modificaci車n libremente con atribuci車n al autor original.

Autor: Conversi車n autom芍tica del script BAT original por ChatGPT (2025)

Si quieres, puedo ayudarte a guardar este texto en un archivo .md o revisar otros documentos que tengan el mismo problema. ?Te gustar赤a que lo prepare para tu repositorio o presentaci車n?
