# Prompt — F01 «Núcleo de dominio», parte 1 · Backend (fase 2, sprint 11)

> **Ejecutado** el 2026-11-24; ya no es una instrucción. Parte 1 cerrada en BE `f2/f01-nucleo`: fases 1 a 6 en `b089eef`, `9bb205b`, `5a44a71`, `4f4a78b`, `202a42d` y `f567f40`.

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/Backend/wms-api`. Necesita leer `docs/` y escribir solo en `Backend/wms-api` (y en `docs`, para el estado de sus fases).
> 2. Copia el bloque de abajo. El agente ejecuta las seis fases del plan, una a la vez, con commit y push de `f2/f01-nucleo` al cerrar cada una.
> 3. Corre a la vez que la maquetación de F02 (en `Frontend/wms`), nunca con otro agente en el backend (M10).
>
> **Plan:** [plan-cerrado-f2-f01-nucleo-2026-11-21.md](plan-cerrado-f2-f01-nucleo-2026-11-21.md) (parte 1, §8).
> **Base:** BE `fase-2` `529bda7`, o lo que haya en `fase-2` si avanzó. La rama `f2/f01-nucleo` sale de `fase-2`.
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el agente de backend de la feature F01 «Núcleo de dominio» de la fase 2 del WMS de Bodegas Asociadas.

Lee, en este orden: docs/README.md; Backend/wms-api/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md) solo §1.2, §5 y §6; y del plan cerrado docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md solo §0, §1 (decisiones D1 a D47, que mandan), los endpoints de §2 que tocan tu fase y la sección de tu fase en §8, §3, §4, §5 y §6. No leas el plan entero: es de 2.300 líneas.

Trabaja en la rama f2/f01-nucleo de Backend/wms-api, que sale de fase-2 (base 529bda7, o lo que haya en fase-2 si avanzó). Antes de empezar: git fetch; si develop avanzó, fusiona develop en fase-2; crea f2/f01-nucleo desde fase-2, o trae fase-2 a ella si ya existe.
Ejecuta solo la parte 1 y solo UNA fase por turno, la que te indique el usuario (§8 del plan: 1 base y catálogos; 2 unidad de medida; 3 entradas y pesos; 4 edición del ingreso; 5 salidas; 6 facturación). No pases a la siguiente aunque esta haya salido bien: detente con el reporte de cierre; el usuario pide la siguiente en una sesión nueva. Durante el trabajo corre solo las pruebas de la fase con salida mínima; la suite completa, al cerrar. Al cerrar la fase: compuertas de §6.1 del plan maestro con las cifras antes y después (build, Wms.Tests, Wms.IntegrationTests, una prueba de integración por endpoint de la fase), los casos QA de la fase en PASA por API (§6 del plan), commit con el mensaje sugerido (§12) y push de tu rama.
Migraciones solo con dotnet ef y solo contra la base local: las cuatro de §4 del plan, cada una en el commit de su fase; has-pending-model-changes limpio al cerrar cada fase. Las fases 4 y 6 no llevan migración: si no sale limpio, detente y pregunta. Nunca edites a mano Migrations/*, los *.Designer.cs ni el snapshot.
El contrato de §2 es la única fuente del frontend: no cambies una ruta, un campo ni un mensaje de error sin preguntar. Ajusta las pruebas en sus helpers, no prueba por prueba (§0.5 del plan).
No toques Frontend/wms: F02 lo maqueta a la vez y la integración I-01 es otro agente.

Si el código no coincide con lo que cita el plan, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
Al terminar cada fase, actualiza su estado en §8 del plan, en docs/planes/README.md y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (§2.2, fila F01, columna «1 · Backend», con el commit), con commit y push en docs. Al terminar la parte, marca este prompt «Ejecutado» en su encabezado y entrégame un resumen con las cifras, los commits y lo que queda pendiente para I-01.
```
