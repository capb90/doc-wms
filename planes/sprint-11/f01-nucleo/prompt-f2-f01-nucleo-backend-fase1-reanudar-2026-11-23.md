# Prompt — Reanudar F01, fase 1 (backend), tras el corte por límite de uso

> **Ejecutado** el 2026-11-23; ya no es una instrucción. Fase 1 cerrada en BE `b089eef`.

> **Cómo usarlo:**
> 1. Abre una sesión **nueva** de Claude Code en `code_workspace/` (Sonnet 5.5 alcanza para terminar una fase ya avanzada; Opus 5.5 si la fase 1 sale con muchas diferencias del contrato).
> 2. Copia el bloque de abajo. No pegues el prompt original de F01: este lo reemplaza para esta fase.
> 3. El agente retoma, termina, verifica y cierra **solo la fase 1**, y se detiene. La fase 2 se pide en otra sesión.
>
> **Estado al cortarse (2026-11-23):** BE `f2/f01-nucleo` en `376245f` (solo `AGENTS.md`), con 90 archivos de la fase 1 **sin commit**: controladores de Configuración, `Settings`, filtros y orden en `Wms.Common/Wrappers`, `FieldPrefix`, `WeeklyExchangeRate`, `EntryReasonCategory`, `PrefixedField` y la migración `20261123133755_AddCatalogSortAndPrefixes`. Nada de eso está verificado.
> **Plan:** `docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`, fase 1 del §8. El prompt original sigue siendo `prompt-f2-f01-nucleo-backend-2026-11-21.md`.
>
> Cuando se ejecute, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción».

---

```text
Eres el agente de backend de F01 «Núcleo de dominio» (fase 2 del WMS de Bodegas Asociadas). Una sesión anterior se cortó por el límite de uso en mitad de la FASE 1. Tu trabajo es terminar y cerrar SOLO la fase 1, y detenerte.

## Lee (solo esto)
docs/README.md; Backend/wms-api/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md) solo §1.2, §5 y §6; y del plan cerrado de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md) solo §0, §1 (D1 a D47 mandan), los endpoints de la fase 1 en §2 (C-F01-00; C-F01-01 a C-F01-68, C-F01-141 y C-F01-163 a C-F01-170), §3, §4 (migración AddCatalogSortAndPrefixes), §5, §6 (QA2-F01-001 a 019), §8 (fase 1) y §12. No leas el plan entero: tiene 2.300 líneas.

## Retoma sin perder lo hecho
1. Backend/wms-api, rama f2/f01-nucleo. git status y git diff --stat. NO uses git stash, reset, checkout ni clean: el árbol de trabajo tiene el avance de la sesión cortada y no está en ningún commit.
2. Inventario contra el plan, con grep acotado: qué endpoints, decisiones D9 a D17, reglas puras y pruebas de la fase 1 ya existen y cuáles faltan. No reescribas lo que ya cumple el contrato; el código existente NO está verificado, así que valida cada pieza contra §2 y §1 (rutas, políticas, campos, mensajes de error).
3. Migración: ya existe 20261123133755_AddCatalogSortAndPrefixes. Compárala con §4 del plan. Si coincide, déjala. Si no, corrige el modelo y regénerala con dotnet ef (borra la sin aplicar con dotnet ef migrations remove, solo en local; nunca edites a mano Migrations/*, *.Designer.cs ni el snapshot). Comprueba que esté aplicada en la base local.
4. Completa solo lo que falte de la fase 1. Nada de las fases 2 a 6 (unidad de medida, entradas, edición, salidas, facturación).

## Cierre de la fase 1
- Compuertas de §6.1 del plan maestro con las cifras antes y después (base: lo que dé `dotnet test` en 529bda7; si no la conoces, dilo): dotnet build Wms.sln; Wms.Tests; Wms.IntegrationTests (Docker); has-pending-model-changes limpio; una prueba de integración por endpoint de la fase. Durante el trabajo corre solo lo de la fase con salida mínima; la suite completa, una vez, al cerrar.
- Casos QA2-F01-001 a QA2-F01-019 en PASA por API.
- Un solo commit con el mensaje de §12 (feat(catalogos): orden y filtros por columna, motivos con categoría, prefijos, tasa semanal y permisos de Configuración (DEC-080, F01)), con la migración dentro, y push de f2/f01-nucleo. Termina el mensaje con la línea de coautoría que indique la sesión.
- Actualiza el estado de la fase 1 en §8 del plan, en docs/planes/README.md y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (§2.2, fila F01, columna «1 · Backend», con el commit), con commit y push en docs.
- Detente con el reporte: cifras antes y después, commit, QA y pendientes. No sigas con la fase 2. Marca este prompt «Ejecutado» en su encabezado.

## Reglas
Si el código no coincide con el plan, o falta una decisión, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No cambies el contrato sin preguntar: F02 maqueta contra él. No toques Frontend/wms. No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
```
