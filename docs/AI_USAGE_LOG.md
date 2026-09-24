# AI Usage Log

## Purpose

Este documento registra de manera resumida las contribuciones relevantes de Inteligencia Artificial durante el desarrollo de ADA-05 (Customer Search) y las decisiones humanas asociadas, permitiendo reconstruir el flujo de trabajo asistido, los cambios reales introducidos en el repositorio y la trazabilidad de las decisiones a lo largo de las distintas etapas del desarrollo spec-driven.

---

## Entry 1 — Delimitación de alcance y restricción al repositorio del proyecto

**Stage:**  
Tasks / Planning

**Objective:**  
Delimitar con precisión el espacio de trabajo del agente de IA exclusivamente al repositorio local del proyecto ADA-05, evitando la exploración o lectura de directorios y proyectos ajenos en la máquina local.

**AI contribution:**  
Al recibir la solicitud inicial para implementar la funcionalidad Customer Search e inspeccionar el entorno, el agente comenzó a escanear rutas fuera del proyecto (`../sales-module`, `../Banquetes-Digitales-Back`, búsquedas en `/Users/monse/Documents`), intentando inferir contexto de otros repositorios y provocando bloqueos de permisos.

**Human decision:**  
El estudiante intervino de forma inmediata interrumpiendo la sesión (`clear`) y proporcionó una instrucción correctiva explícita: trabajar única y exclusivamente dentro del repositorio/workspace actual (`/Users/monse/Documents/ADA 05`), sin cambiar de directorio ni acceder a otros proyectos.

**Product change:**  
Se preservó el aislamiento estricto del proyecto. No se importó código externo ni se contaminó el espacio de trabajo con artefactos o dependencias de otras asignaturas o módulos.

**Evidence:**  
Registro de sesión en transcript `c83ae86e-d276-41d6-9d7d-c17f743f849d` (pasos 35 a 51).

**Outcome:**  
El agente reorientó su análisis de forma disciplinada hacia los artefactos formales locales del repositorio (`REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `AGENTS.md`).

---

## Entry 2 — Selección de stack tecnológico y scaffolding arquitectónico para T-01

**Stage:**  
Architecture / Implementation

**Objective:**  
Definir la plataforma técnica para la implementación de la tarea `T-01 Project setup` (dado que la especificación original era tecnológicamente agnóstica) y generar la estructura base de componentes de acuerdo con el diseño de arquitectura por capas.

**AI contribution:**  
La IA analizó los requerimientos de arquitectura (`ARCHITECTURE.md`) y formuló una consulta estructurada al estudiante presentando tres alternativas de stack tecnológico:
1. Python (arquitectura en capas desacoplada con pytest) [Recomendada].
2. TypeScript / Node.js (arquitectura en capas con test runner nativo de Node).
3. C# / .NET (Clean Architecture con xUnit).  
Tras la elección, la IA generó la configuración del proyecto (`pyproject.toml`, `.gitignore`) y el andamiaje completo de paquetes de `customer_search` (`api`, `services`, `repositories`, `models`, `validation`, `auth`).

**Human decision:**  
El estudiante evaluó las opciones y seleccionó expresamente: `(Recommended) Python (clean layered architecture with pytest)`, validando posteriormente que la distribución de paquetes correspondiera fielmente al diagrama de componentes de `ARCHITECTURE.md`.

**Product change:**  
Creación de `pyproject.toml`, `.gitignore` y los módulos base del backend:
- `customer_search/models/customer.py`
- `customer_search/repositories/customer_repository.py`
- `customer_search/validation/validator.py`
- `customer_search/auth/authorizer.py`
- `customer_search/services/search_service.py`
- `customer_search/api/controller.py`

**Evidence:**  
- Transcript `c83ae86e-d276-41d6-9d7d-c17f743f849d` (interacción de selección en líneas 93–94 y llamadas de creación en líneas 96–135).
- Archivos en `customer_search/` y `pyproject.toml`.
- Commits `e97dd36` y `f3bb7c4aba576285924c0e1f0e1e73a740db97c1`.

**Outcome:**  
Se estableció un entorno ejecutable y modular para el proyecto, desacoplando la capa de presentación de la capa de acceso a datos según el patrón establecido en `ARCHITECTURE.md`.

---

## Entry 3 — Implementación y ejecución de la suite automatizada inicial (T-01 / T-05)

**Stage:**  
Testing

**Objective:**  
Verificar mediante pruebas automatizadas que las capas arquitectónicas recién creadas para `T-01` compilan correctamente, pueden instanciarse y se comunican entre sí sin errores de sintaxis, tipos o referencias.

**AI contribution:**  
La IA redactó un conjunto de pruebas automatizadas en `tests/test_project_setup.py` que abarca:
1. Instanciación del modelo de dominio `Customer` y el DTO `CustomerSearchResult`.
2. Cumplimiento de la interfaz `ICustomerRepository` por parte de `InMemoryCustomerRepository`.
3. Ejecución básica de los componentes `SearchInputValidator` y `CustomerSearchAuthorizer`.
4. Cableado integral de capas desde `CustomerSearchController` hasta el repositorio.  
Asimismo, ejecutó la suite con el comando `pytest -v`.

**Human decision:**  
El estudiante revisó el código de las pruebas, verificó que los resultados fueran auténticos (4 pruebas recolectadas, 4 pasadas en 0.02s) y aceptó la suite reconociendo que cubría la verificación estructural de T-01 sin pretender falsamente validar la lógica de negocio pendiente (T-03 / T-04).

**Product change:**  
Creación de `tests/__init__.py` y `tests/test_project_setup.py`, y verificación exitosa de la suite de pruebas bajo `pytest`.

**Evidence:**  
- Archivo `tests/test_project_setup.py`.
- Ejecución verificable de `pytest -v` (4 passed in 0.02s).
- Commit `e97dd360af44c7575d8f3cccdbba2a8e2becf71b` ("Customer Search: implement feature").

**Outcome:**  
El proyecto quedó provisto de una batería de pruebas automatizada y funcional para prevenir regresiones arquitectónicas en tareas sucesivas.

---

## Entry 4 — Elaboración honesta de la matriz de trazabilidad y pautas de prueba (Fases 8 y 9)

**Stage:**  
Traceability / Verification

**Objective:**  
Consolidar la trazabilidad integral de los requisitos definidos en `REQUIREMENTS.md` contra la especificación (`SPEC.md`), tareas (`TASKS.md`), código y pruebas reales, reportando el estado exacto de cada requisito con total honestidad técnica.

**AI contribution:**  
La IA analizó minuciosamente el estado del repositorio frente a cada uno de los 9 requisitos (FR-01 a FR-06 y NFR-01 a NFR-03). En lugar de declarar la funcionalidad como completa, documentó con precisión:
- Requisitos con implementación parcial (`Partial`): FR-01, FR-02, FR-03, FR-05, FR-06 y NFR-02 (debido a la presencia de stubs en el repositorio y la falta de filtrado real por permisos).
- Requisitos ausentes (`Missing`): FR-04 (ordenamiento por relevancia no implementado al quedar abierta la pregunta Q-02) y NFR-03 (ausencia total de interfaz de usuario frontend).
- Requisitos no verificados (`Not verified`): NFR-01 (sin suite de pruebas de rendimiento ni datos de prueba masivos).  
Además, la IA redactó las directrices de ejecución de pruebas en `AGENTS.md`.

**Human decision:**  
El estudiante auditó la matriz generada para cerciorarse de que no existiera inflación de resultados ni afirmaciones no fundamentadas, aprobó la clasificación honesta de los estados, ubicó la matriz formalmente en `docs/TRACEABILITY.md` y versionó los cambios en el historial de Git.

**Product change:**  
- Creación de `docs/TRACEABILITY.md`.
- Actualización de `AGENTS.md` con las instrucciones de ejecución de pruebas con `pytest -v`.
- Ninguna alteración a `REQUIREMENTS.md` ni a `SPEC.md`.

**Evidence:**  
- `docs/TRACEABILITY.md`.
- `AGENTS.md`.
- Commit `f3bb7c4aba576285924c0e1f0e1e73a740db97c1`.
- Transcript `e68e3c67-c580-4d3b-8a7f-3e15d06c72b8` (pasos 59 a 71).

**Outcome:**  
Se obtuvo un estado de trazabilidad transparente, auditable y alineado con los estándares de ingeniería de software, documentando con fidelidad tanto los componentes completados como las brechas pendientes de desarrollo.
