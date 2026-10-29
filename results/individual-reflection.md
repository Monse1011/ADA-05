# Reflexión individual — ADA-08 (BORRADOR)

> **Estado: borrador preparado por el agente (Claude Code) a partir de la evidencia del proyecto. Todavía no está confirmado por la autora.**
> Las respuestas citan hechos documentados en `results/` y `REPOSITORY_READINESS_AUDIT.md`. Lo marcado con **[REQUIERE TU RESPUESTA]** depende de tu experiencia, opinión o planes, y el agente no debe inventarlo. Revisa, corrige y reescribe con tu voz antes de entregar.

## 1. ¿Cuál fue el principal obstáculo para el agente en la ejecución BEFORE?

**Evidencia (`results/before-agent-run.md`):** el obstáculo fue validar el cambio, no implementarlo.
- El único comando documentado, `pytest -v`, falló con `command not found`, y `python3 -m pytest -v` falló con `No module named pytest`.
- Para validar, el agente tuvo que encontrar `~/.venv` fuera del repositorio. Ningún archivo lo mencionaba y el preámbulo le pedía trabajar solo dentro de la carpeta.

**[REQUIERE TU RESPUESTA]:** ¿coincide con lo que tú percibiste como el mayor problema?

## 2. ¿Qué información tuvo que inferir el agente que un desarrollador experimentado ya conocía?

**Evidencia:**
- Dónde está el intérprete con pytest (`~/.venv`) y que su Python 3.9.6 no cumple `requires-python >=3.10`.
- Que pytest no está declarado como dependencia.
- Que los documentos de especificación no se deben editar. Esa regla solo estaba en `docs/AGENT_REPORT.md`, como intervención humana de ADA-05.
- Que las preguntas Q-01..Q-05 están abiertas. En este caso la tarea lo indicaba explícitamente.

**[REQUIERE TU RESPUESTA]:** ¿qué otro conocimiento tuyo del proyecto notaste que faltaba?

## 3. ¿Qué mejora produjo el mayor impacto y por qué?

**Evidencia:** la diferencia más visible entre las ejecuciones fue pasar de 2 comandos fallidos a 0, y validar con `scripts/verify_repo.sh` usando el intérprete documentado. Esto coincide con la sección "Environment" de `AGENTS.md` y con el script de verificación.

**Interpretación:** con una sola ejecución por fase no se puede aislar qué mejora causó qué; ver la limitación 1 del informe, §10.

**[REQUIERE TU RESPUESTA]:** tu valoración personal de cuál fue la mejora más útil.

## 4. ¿Qué información pertenece en AGENTS.md y qué información NO debería vivir ahí?

**En este proyecto, `AGENTS.md` contiene:**
- las fuentes de verdad y el orden de lectura;
- el comando de verificación como Definition of Done;
- el entorno;
- los archivos protegidos;
- las capas;
- las condiciones para detenerse (Q-01..Q-05);
- los stubs conocidos;
- las reglas sobre pruebas y operaciones prohibidas.

**Lo que se dejó fuera a propósito:**
- los requisitos y criterios de aceptación, que siguen en ` REQUIREMENTS.md` y `SPEC.md` y no se copian;
- el mapa detallado del código, que está en `docs/REPO_MAP.md`;
- pistas de la solución de la tarea de prueba.

**[REQUIERE TU RESPUESTA]:** tu criterio general para futuros proyectos.

## 5. ¿Qué regla convertiste en software/hook/script en lugar de dejarla como instrucción?

**Evidencia (`scripts/check_repo_contract.py`):**
- **No modificar especificaciones ni la evidencia de ADA-05:** se comprueba con hashes SHA-256.
- **Dirección de capas** (la API no importa el repositorio): se analizan las importaciones del código.
- **Cada FR/NFR debe estar en la matriz de trazabilidad:** su primera ejecución detectó FR-07, FR-08 y NFR-04.

Las tres tienen corridas negativas que fallan con exit 1.

**[REQUIERE TU RESPUESTA]:** ¿por qué elegirías o priorizarías estas reglas?

## 6. ¿Qué diferencia observaste entre "más contexto" y "mejor contexto"?

**Evidencia:**
- El `AGENTS.md` de BEFORE tenía 13 líneas, y su único dato concreto (`pytest -v`) era incorrecto para el entorno real.
- El de AFTER es más largo, pero sobre todo es verificable: cada regla apunta a un comando, un archivo o una comprobación.
- `CLAUDE.md` no repite nada; solo importa `AGENTS.md`.

**[REQUIERE TU RESPUESTA]:** lo que tú observaste.

## 7. ¿Qué riesgo aparece cuando CLAUDE.md/GEMINI.md/copilot instructions duplican información del proyecto?

**Respuesta basada en el diseño de este repositorio:** las copias divergen con el tiempo. Un agente puede leer una versión desactualizada y actuar sobre ella. Un caso real de información desactualizada en este proyecto:
- `AGENTS.md` en BEFORE decía `pytest -v`, que no funcionaba.
- `AI_USAGE_LOG.md` decía "No commits" después de que sí se hizo uno; se corrigió en la Fase 5.

Por eso `CLAUDE.md` solo importa `AGENTS.md`.

**[REQUIERE TU RESPUESTA]:** tu opinión.

## 8. ¿Qué checks comparten ahora el agente, el desarrollador humano y CI?

**Evidencia:** los tres ejecutan `scripts/verify_repo.sh`:
- el contrato del repositorio;
- la suite completa de pytest.

Lo invocan `AGENTS.md` (Definition of Done), `docs/REPO_MAP.md` (comandos) y `.github/workflows/verify.yml`.

**Limitación:** el workflow de CI **nunca se ha ejecutado** en GitHub, porque no hubo push.

## 9. ¿Qué parte del proceso sigue requiriendo decisión humana?

**Evidencia (informe §11):**
- responder Q-01..Q-05;
- aprobar cambios a documentos protegidos y actualizar sus hashes;
- decidir la versión de Python;
- hacer push y revisar CI;
- corregir el autorizador fail-open en una tarea acotada;
- agregar el README;
- hacer commit de la Fase 5;
- configurar el sandbox para que el agente no salga del repositorio.

En este proyecto, además, tú decidiste:
- aceptar el venv con Python 3.9.6;
- aprobar `TASK_UNDER_TEST.md`;
- hacer el commit `7d0618d`;
- aprobar el plan de consolidación.

## 10. ¿Qué evidencia demuestra que el AFTER es realmente mejor?

**Hechos:**
- **Auditoría:** 39 → 77 (+38) con la misma rúbrica.
- **Comandos fallidos:** 2 en BEFORE, 0 en AFTER.
- **Prueba fallando antes del cambio:** AFTER la mostró (5 failed antes del cambio); BEFORE no.
- **Validación:** AFTER usó el contrato del repositorio y las pruebas (13 passed); BEFORE solo pytest.
- **Pruebas de AFTER:** fallan sobre el código de `7d0618d` (5 failed), verificado de forma independiente.

**Matiz:** las dos ejecuciones terminaron en PASS, así que la mejora está en el proceso y en la evidencia, no en el resultado. Con una sola ejecución por fase no se puede afirmar causalidad.

**[REQUIERE TU RESPUESTA]:** ¿te parece suficiente esta evidencia?

## 11. ¿Qué mejora realizada para el agente también beneficia a un desarrollador que entra por primera vez al proyecto?

**Evidencia:**
- `docs/REPO_MAP.md`: capas, comandos y diferencias entre la documentación y el código.
- `scripts/verify_repo.sh`, que ahora indica cómo instalar si falta pytest.
- La lista de fuentes de verdad y de stubs conocidos en `AGENTS.md`.
- La matriz de trazabilidad completa.

**[REQUIERE TU RESPUESTA]:** ¿cuál consideras más útil para una persona nueva?

## 12. ¿Qué variable no controlada podría afectar tu comparación BEFORE/AFTER?

**Evidencia (informe §10):**
- El modelo no es determinista y hubo una sola ejecución por fase.
- La sesión AFTER vio que existía la sesión BEFORE (no la usó).
- El árbol AFTER incluía `implicit-knowledge.md`, que describe en términos generales los problemas de BEFORE.
- Tu configuración global (`~/.claude/CLAUDE.md` y el plugin ponytail) aplicó a ambas.
- El mismo agente diseñó las mejoras y las evaluó.
- El transcript no muestra qué archivos se leyeron.

## 13. ¿Qué elementos de este ADA conservarás como base para tu proyecto final?

**[REQUIERE TU RESPUESTA]:** depende de tus planes. Candidatos, según lo construido:
- `AGENTS.md` con su Definition of Done;
- `docs/REPO_MAP.md`;
- `scripts/verify_repo.sh` compartido con CI;
- un contrato de archivos protegidos;
- el protocolo de evaluación BEFORE/AFTER con worktrees.
