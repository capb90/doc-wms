# Prompt — F04 «Bodega», parte 1 (backend)

> **Ejecutado** el 2026-11-25; ya no es una instrucción. BE-1 (`fb707f7`), BE-2 (`b80f8f4`) y BE-3 (`b8cbd07`) en `f2/f04-bodega`; estado en el plan §8.1 a §8.3.

> **Fecha:** 25 de noviembre de 2026. **Plan:** [plan-cerrado-f2-f04-bodega-2026-11-25.md](plan-cerrado-f2-f04-bodega-2026-11-25.md) (§8.1 a §8.3). **Repo y rama:** `Backend/wms-api`, `f2/f04-bodega`, que sale de `fase-2` (base `eb4e428`, o lo que haya en `fase-2` si avanzó). Corre en paralelo con la maquetación (otro agente, en el frontend).

```text
Eres el agente de backend de la feature F04 «Bodega» de la fase 2 del WMS de Bodegas Asociadas.

Lee, en este orden: docs/README.md; Backend/wms-api/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md) solo §1.2, §5 y §6; y del plan cerrado docs/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md solo §0, §1, §2.1 y la sección de tu fase en §8 (BE-1 es §8.1, BE-2 es §8.2, BE-3 es §8.3). Lee el resto del plan por secciones, solo cuando tu fase lo cite: las fichas de §2.2 y los esquemas de §2.3 de tus endpoints, §3.2 (archivos), §4 (migración), §5 (pruebas), §6.1 (casos QA) y §7 (transición).

Trabaja en la rama f2/f04-bodega de Backend/wms-api, que sale de fase-2 (base eb4e428, o lo que haya en fase-2 si avanzó). Antes de empezar trae lo último de develop a fase-2 y de fase-2 a tu rama. Si la rama ya existe, retómala.
Ejecuta solo la parte 1 y solo UNA fase por turno: la que te indique el usuario (BE-1, BE-2 o BE-3, en ese orden). Al cerrarla: compuertas de §6.1 del plan maestro con las cifras antes y después (dotnet build Wms.sln; Wms.Tests; Wms.IntegrationTests, con Docker; has-pending-model-changes limpio; una prueba de integración por endpoint nuevo o modificado de tu fase), los casos QA de tu fase en PASA por API, commit con el mensaje sugerido de §12 y push de tu rama, el estado de tu fase en §8 del plan y en la matriz, y detente con el reporte de cierre. El usuario te pide la siguiente fase en una sesión nueva.
Migraciones solo con dotnet ef y solo contra la base local, con el nombre y el contenido de §4: BE-1 genera AddWarehouseDelayAlerts, BE-2 genera ReceptionPerEntry y BE-3 genera ForkliftRequiresInvoice. Si una migración no sale como dice §4, corrige el modelo y regénérala; nunca edites a mano Migrations/*.
El trabajo en segundo plano de los relojes (BE-1) no corre en la suite: pruébalo llamando a WarehouseDelayAlertService.RunOnceAsync con un now fijo (§8.1). La suite comparte la base y la cola de báscula corta en 100 camiones: libera los camiones que abran tus pruebas (trampa 12).
No toques el frontend: lo maqueta otro agente en paralelo con el contrato de §2. Un mensaje de error del contrato cambia solo si cambias el contrato, y eso exige preguntar.

Si el código no coincide con lo que cita el plan, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
Al terminar la parte (BE-3 cerrada), marca este prompt «Ejecutado» en su encabezado, actualiza el estado en el plan cerrado, en docs/planes/README.md y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md, haz commit y push en docs, y entrégame un resumen con las cifras, los commits y lo que queda pendiente para I-04.
```
