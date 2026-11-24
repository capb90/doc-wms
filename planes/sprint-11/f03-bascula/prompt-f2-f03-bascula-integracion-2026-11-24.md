# Prompt — F03 «Báscula», parte 3 (integración I-03)

> **Fecha:** 24 de noviembre de 2026. **Plan:** [plan-cerrado-f2-f03-bascula-2026-11-24.md](plan-cerrado-f2-f03-bascula-2026-11-24.md) (§13). **Repos y ramas:** `Backend/wms-api` y `Frontend/wms`, las dos en `f2/f03-bascula`. Entra cuando BE-1 a BE-3 y FE-1 a FE-3 están cerradas y con push; ocupa los dos repos.

```text
Eres el agente de integración de la feature F03 «Báscula» de la fase 2 del WMS de Bodegas Asociadas (I-03).

Lee, en este orden: docs/README.md; Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md) solo §1.2, §5 y §6; y del plan cerrado docs/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md solo §0, §1, §2.1, §2.4, §6.2 y §13. Lee el resto del plan por secciones, solo cuando lo necesites: §2.2 y §2.3 para cada fuente http, §3.3 para los archivos.

Trabaja en la rama f2/f03-bascula de Backend/wms-api y de Frontend/wms; las dos salieron de fase-2. Antes de empezar trae lo último de develop a fase-2 y de fase-2 a cada rama.
Ejecuta solo la parte 3. Si no cabe en un turno, divídela en dos por su frontera natural (primero las fuentes http y los casos QA; después el menú, lo que se borra y la fusión) y detente con el reporte entre una y otra.
Escribe las fuentes http (§13.1), con cada respuesta validada por su esquema Zod; borra la fachada catalog.source.ts y las carpetas mocks/ de F03; enlaza el menú y cambia los enlaces y las guardias de §13.2; borra lo de §13.3 después de comprobar con grep quién importa cada archivo (trampas 4 y 7); pasa QA2-F03-031 a QA2-F03-050 en el navegador contra el backend local de f2/f03-bascula, sin la sesión simulada; y fusiona f2/f03-bascula en fase-2 en los dos repos con --no-ff, con push. Sin push --force.
En el backend no agregas nada nuevo: si una pantalla necesita algo que el contrato no tiene, o el backend responde distinto del contrato, detente y pregunta (riesgo R3 del plan maestro); no cambies el contrato por tu cuenta.
Compuertas de cierre: §6.1 en el backend y §6.2 en el frontend (salvo «sin llamadas reales»), con las cifras antes y después; criterio de §13.5.

Si el código no coincide con lo que cita el plan, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
Al terminar, copia los casos QA con su resultado a docs/qa/ (§13.4), marca este prompt «Ejecutado» en su encabezado, actualiza el estado en el plan cerrado, en docs/planes/README.md, en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md y en docs/contexto/estado.md, haz commit y push en docs, y entrégame un resumen con las cifras, los commits, las fusiones y qué puedo probar en local.
```
