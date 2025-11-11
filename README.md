Buscador de Archivos Duplicados (GUI en Python)

## 🖼️ Capturas de Pantalla

![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/01.png)
![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/02.png)
![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/03.png)
![Preview](https://github.com/Azzlaer/WC3_Eliminar_Duplicados/blob/main/04.png)


🔍 DESCRIPCIÓN
Este programa es una herramienta con interfaz gráfica (GUI) desarrollada en Python que permite buscar y eliminar archivos duplicados dentro de una carpeta seleccionada. Utiliza el algoritmo de hash SHA-256 para identificar archivos con contenido idéntico, sin importar su nombre.
El proyecto es una conversión mejorada del script original en Batch (BAT), integrando funcionalidades modernas y una interfaz amigable basada en Tkinter.

🧰 CARACTERÍSTICAS PRINCIPALES
- Interfaz Gráfica (GUI): desarrollada con Tkinter.
- Selección de carpeta: el usuario puede elegir fácilmente la ruta a analizar.
- Cálculo de hashes SHA-256: asegura una comparación precisa entre archivos.
- Detección de duplicados: muestra todos los archivos duplicados encontrados.
- Eliminación controlada: permite borrar duplicados dejando una copia por grupo de hash.
- Modo simulación: ejecuta el análisis sin borrar archivos.
- LOG en vivo: muestra un registro detallado de todas las acciones realizadas.
- Exportación de informe: genera un archivo con nombre REGISTRO_DD_MM_AAAA.log.
- Barra de progreso: indica el avance del análisis.
- Multihilo: evita bloqueos de la interfaz durante el análisis.

💻 REQUISITOS DEL SISTEMA
- Python 3.7 o superior
- Librerías estándar de Python (no requiere instalación adicional)
Opcional:
- send2trash (si se desea mover los duplicados a la papelera en lugar de borrarlos)
pip install send2trash



📥 INSTRUCCIONES DE USO
- Ejecutar la aplicación:
python buscador_duplicados_gui.py
- Seleccionar carpeta:
- Presiona "Seleccionar" y elige la carpeta donde buscar duplicados.
- Marca o desmarca "Incluir subcarpetas" según tus necesidades.
- Analizar archivos:
- Pulsa el botón "Analizar".
- Se mostrarán los archivos duplicados en el panel izquierdo.
- El panel derecho mostrará el registro (LOG) en tiempo real.
- Eliminar duplicados:
- Si se encuentran duplicados, activa "Simular eliminación" para hacer una prueba sin borrar.
- Pulsa "Eliminar duplicados" para borrar los duplicados, manteniendo una sola copia de cada grupo.
- Exportar informe:
- Al finalizar, puedes guardar el log en un archivo .log con nombre tipo REGISTRO_10_11_2025.log.

📁 ESTRUCTURA DEL PROYECTO
📦 Proyecto  
├── buscador_duplicados_gui.py   # Script principal de la aplicación  
└── README.md                    # Este archivo  



⚙️ FUNCIONAMIENTO INTERNO
- Recorre todos los archivos en la carpeta seleccionada (y subcarpetas, si está activado).
- Calcula el hash SHA-256 de cada archivo.
- Registra cada hash en memoria; si un hash ya existe, el archivo se marca como duplicado.
- Muestra los duplicados en la interfaz.
- Permite eliminar los duplicados (manteniendo una copia) y registra los resultados en el LOG.

📄 EJEMPLO DE SALIDA DE LOG
[2025-11-10 14:23:01] Iniciando análisis en: D:\Juegos\Blizzard\Warcraft III\Maps\Download  
[2025-11-10 14:23:03] Nuevo hash: a3c56f9e1b7d... -> D:\Juegos\Blizzard\Warcraft III\Maps\Download\map1.w3x  
[2025-11-10 14:23:04] Duplicado encontrado (hash a3c56f9e1b7d...): D:\Juegos\Blizzard\Warcraft III\Maps\Download\map1_copy.w3x  
[2025-11-10 14:23:06] Total de archivos analizados: 542  
[2025-11-10 14:23:06] Archivos duplicados encontrados: 8  
[2025-11-10 14:23:10] Eliminado: D:\Juegos\Blizzard\Warcraft III\Maps\Download\map1_copy.w3x  
[2025-11-10 14:23:11] Script finalizado correctamente.  


📝 NOTAS ADICIONALES
- Los archivos se eliminan de forma permanente, a menos que se active el modo de simulación o se implemente send2trash.
- Los informes (.log) se guardan en la ubicación que el usuario elija.
- Es posible detener la ejecución cerrando la ventana.

📜 Licencia
Este proyecto se distribuye bajo licencia MIT, lo que permite su uso, copia y modificación libremente con atribución al autor original.

Autor: Conversión automática del script BAT original por ChatGPT (2025)

Si quieres, puedo ayudarte a guardar este texto en un archivo .md o revisar otros documentos que tengan el mismo problema. ¿Te gustaría que lo prepare para tu repositorio o presentación?
