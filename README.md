# FIBONACCI-FINAL-MODULOS-API-MAESTRO

## Informe de Automatización, Uso de Tokens, Evaluación y Configuración

### 1. Automatización

Se ha implementado un flujo automatizado de integración que permite:

- Clonación del repositorio principal y los submódulos requeridos.
- Agregado de submódulos mediante script Bash para mantener la estructura modular.
- Inicialización y actualización automática de submódulos.
- Generación automatizada del archivo `docker-compose.yml` para el despliegue simultáneo de todos los servicios.
- Creación de ejemplos listos para conexión a APIs externas (Hugging Face) y despliegue en plataformas cloud (Heroku).

Ventajas:
- Reducción de pasos manuales.
- Facilidad para incorporar nuevos módulos.
- Despliegue reproducible y escalable.

### 2. Uso de Tokens

Al conectar con servicios de terceros (por ejemplo, Hugging Face), es necesario usar tokens de autenticación. El script incluye un archivo de ejemplo (`examples/connect_huggingface.py`) donde se utiliza el parámetro `token` para acceder a la API.

Recomendaciones:
- Jamás incluir tokens reales en scripts públicos.
- Usar variables de entorno (`.env`) para gestionar credenciales.
- En Docker, mapear el archivo `.env` y referenciar variables en los servicios.

Ejemplo de uso seguro:

```python
import os
from huggingface_hub import InferenceApi

api = InferenceApi(repo_id="nombre-modelo", token=os.getenv("HF_TOKEN"))
result = api(inputs="Tu entrada aquí")
print(result)
```

### 3. Evaluación

El flujo automatizado permite evaluar fácilmente:

- Integridad de submódulos: Verificando que todos los módulos se inicializan correctamente con `git submodule update --init --recursive`.
- Despliegue de servicios: Mediante `docker compose up`, comprobar que cada módulo inicia y expone su endpoint.
- Interoperabilidad: Probar la comunicación entre módulos y la integración con APIs externas.
- Despliegue en la nube: Validar el despliegue en Heroku usando el `Procfile` generado.

Métricas sugeridas:
- Tiempo de despliegue.
- Disponibilidad de endpoints.
- Pruebas de integración (respuesta de los módulos bajo distintas entradas).
- Seguridad en el manejo de tokens y variables sensibles.

### 4. Configuración

Submódulos
- Todos los repositorios externos se agregan en rutas bajo `modules.json` y se gestionan con `scripts/add_submodules.sh`.
- Inicialización garantizada con el script.

Docker Compose
- Cada módulo es un servicio independiente (si el módulo tiene Dockerfile).
- Puertos configurables y aislados.
- Facilidad para escalar servicios o agregar nuevos módulos mediante `modules.json` y el generador.

Hugging Face API
- Ejemplo listo para modificar según necesidades en `examples/connect_huggingface.py`.
- Token gestionado como variable de entorno (`HF_TOKEN`).

Heroku
- `Procfile` incluido en la raíz como ejemplo de despliegue.
- Ajustar el comando según el módulo/servicio a publicar.

Recomendaciones generales
- Mantener un archivo `.env.example` con las variables necesarias.
- Documentar endpoints y dependencias en el README.
- Realizar revisiones periódicas de seguridad (dependencias y manejo de claves).

---

Conclusión: El flujo implementado permite una rápida integración, despliegue seguro y evaluación continua de los módulos del laboratorio. Permite el uso controlado de credenciales y la configuración modular facilita el mantenimiento y la expansión del proyecto.

## Uso rápido

- Copiar variables: `cp .env.example .env` y editar valores.
- Agregar/actualizar submódulos: `bash scripts/add_submodules.sh`.
- Generar docker-compose: `python3 scripts/generate_docker_compose.py`.
- Levantar servicios: `docker compose up -d`.

## Repositorios y Enlaces Útiles

A continuación, una lista curada de repositorios y recursos que puedes clonar o agregar como submódulos en los ámbitos de IA médica, simulación 3D y cirugía plástica.

### 1. IA Médica
- elmerpuma/Asistente-Medico-IA: https://github.com/elmerpuma/Asistente-Medico-IA
- IAARhub/awesome-ia: https://github.com/IAARhub/awesome-ia
- aibase.com – Repositorios AI Medical: https://www.aibase.com/es/repos/topic/ai-medical
- 5 Repositorios IA y ML (Toolify): https://www.toolify.ai/es/ai-news-es/5-repositorios-de-github-imprescindibles-para-ia-y-machine-learning-3434094

### 2. Simulación 3D Médica
- OswaldoCG/simulacion-flujo-hospitalario: https://github.com/OswaldoCG/simulacion-flujo-hospitalario
- GitHub Topic – simulations: https://github.com/topics/simulations
- aibase.com – Repositorios 3D: https://www.aibase.com/es/repos/topic/3d
- Voka Anatomía 3D: https://voka.io/es/3d-human-anatomy-software-for-students/

### 3. Cirugía Plástica Médica
- SurgicalRoboticsUMA/TFG_Duna: https://github.com/SurgicalRoboticsUMA/TFG_Duna
- Repositorio UNAL – Cirugía Plástica: https://repositorio.unal.edu.co/collections/236f73e6-800e-4295-bb31-d9859421d5af
- Repositorio PUCE – Cirugía Plástica, Reconstructiva y Estética: https://repositorio.puce.edu.ec/collections/73db03df-4135-4063-9883-2b8fe8b1b8a1
- Repositorio UDEM – Microcirugía y cirugía plástica: https://repositorio.udem.edu.mx/browse/title?scope=41da0772-c764-413e-bc05-5eeed137c93a

Sugerencia: Si quieres agregarlos como submódulos, usa el patrón `git submodule add <repo_url> external/<nombre>` y luego `git submodule update --init --recursive` para inicializarlos.
