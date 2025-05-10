
# **CFT: Estimador de Seguridad**

## Descripción

El **Estimador de Seguridad** es una aplicación que permite realizar estimaciones y análisis de seguridad en un entorno de redes. La aplicación está diseñada para ayudar a los usuarios a identificar posibles vulnerabilidades y calcular el riesgo en distintos escenarios. Está diseñada para ser fácil de usar y proporciona resultados detallados y útiles que pueden ser utilizados para mejorar la seguridad de un sistema.

## Características

- **Estimaciones precisas:** Realiza cálculos detallados sobre las posibles vulnerabilidades y riesgos de un sistema.
- **Interfaz gráfica:** Proporciona una interfaz amigable para que los usuarios puedan interactuar con la aplicación de manera sencilla.
- **Generación de informes:** Permite exportar los resultados de las estimaciones a formatos de fácil lectura, como PDF o texto plano.
- **Instalación fácil:** Puedes instalar la aplicación en tu sistema con solo unos pocos pasos.

## Requisitos

Para ejecutar la aplicación, necesitas tener las siguientes dependencias instaladas:

- **Python 3.12** o superior
- **PyInstaller** (para empaquetar la aplicación en un solo archivo ejecutable)
- **Linux** (probado en distribuciones basadas en Debian, como Ubuntu)

## Instalación

### Opción 1: Instalación en Linux usando el paquete `.deb`

1. Descarga el archivo `.deb` desde la sección de releases de GitHub.
2. Abre una terminal y navega hasta el directorio donde descargaste el archivo `.deb`.
3. Ejecuta el siguiente comando para instalar la aplicación:

   ```bash
   sudo dpkg -i EstimadorSeguriadCFTAPP.deb
   ```

4. Para solucionar cualquier dependencia que falte, ejecuta:

   ```bash
   sudo apt-get install -f
   ```

### Opción 2: Usando el código fuente

Si prefieres instalar desde el código fuente, sigue estos pasos:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tuusuario/CFT.git
   ```

2. Accede al directorio del proyecto:

   ```bash
   cd CFT
   ```

3. Ejecuta el programa con el siguiente comando:

   ```bash
   python3 main.py
   ```

## Uso

Una vez instalada la aplicación, puedes acceder a ella a través del menú de aplicaciones en tu sistema o ejecutándola desde la terminal con el siguiente comando:

```bash
/opt/miapp/main
```

### Descripción de la interfaz

- **Pantalla principal:** Aquí podrás ver el resultado de las estimaciones de seguridad y generar informes.
- **Botones de acción:** Acciones rápidas para realizar nuevas estimaciones, exportar resultados y cerrar la aplicación.

## Contribuciones

Si deseas contribuir a este proyecto, ¡serás bienvenido! Puedes hacerlo siguiendo estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu característica o corrección de errores.
3. Realiza tus cambios y asegúrate de que todo esté funcionando correctamente.
4. Envía un Pull Request con una descripción detallada de los cambios.

## Licencia

Este proyecto está bajo la licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto conmigo a través de mi correo electrónico o en los issues del repositorio.
