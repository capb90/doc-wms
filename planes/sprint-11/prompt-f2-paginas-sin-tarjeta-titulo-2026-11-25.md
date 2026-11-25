# Prompt — Fase 2 · Páginas sin tarjeta de título (tableros, formularios y reportes)

> **Ejecutado** el 2026-11-25; ya no es una instrucción. Fase 1 en FE `34254eb`, fase 2 en FE `00ab4c2`, fusión en `fase-2` `2c848af`.

> **Fecha:** 25 de noviembre de 2026. **Plan:** [plan-cerrado-f2-paginas-sin-tarjeta-titulo-2026-11-24.md](plan-cerrado-f2-paginas-sin-tarjeta-titulo-2026-11-24.md), aprobado el 2026-11-24. **Repo y rama:** `Frontend/wms`, `f2/ui-paginas-sin-tarjeta`, que sale de `fase-2` **después de fusionar I-03** (D4). Dos fases; una por turno.

```text
Eres el agente de frontend del plan «Páginas sin tarjeta de título (tableros, formularios y reportes)» de la fase 2 del WMS de Bodegas Asociadas.

Lee, en este orden: docs/README.md; Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; de docs/contexto/convenciones-tecnicas.md solo §3; y el plan cerrado completo, docs/planes/sprint-11/plan-cerrado-f2-paginas-sin-tarjeta-titulo-2026-11-24.md. Del resto lee solo lo que el plan cite, con grep acotado.

Antes de empezar, comprueba que I-03 de F03 esté fusionada en fase-2 (git fetch; busca en fase-2 la fusión de f2/f03-bascula). Si no lo está, detente y avísame: el plan corre después de I-03 (D4). Si lo está, crea la rama f2/ui-paginas-sin-tarjeta desde fase-2 (o retómala si ya existe) y anota su hash base en la cabecera del plan. Confirma con grep las líneas que cita el §2 del plan: son de ee3d5d9 y I-03 movió algunas (al menos el tablero de Báscula).

Ejecuta solo UNA fase por turno: la que te indique el usuario (1 o 2, en ese orden).
- Fase 1: Trazabilidad, los tableros de Báscula, Bodega, Comercio Exterior y Facturación, Ingreso y Salida de Vigilancia, Montacargas y la guardia de D8 (con los reportes de la fase 2 en TITLE_CARD_PENDING mientras tanto).
- Fase 2: los diez reportes, la convención «Páginas que no son listados» en convenciones-tecnicas §3 y la fusión en fase-2 con --no-ff.

Al cerrar cada fase: corre de nuevo las compuertas de §6 del plan con las cifras antes y después (yarn build con código 0; yarn test en verde; yarn lint sin subir los errores de la base y sin ninguno en archivos tocados); los casos QA de la fase (§5) en el navegador, con capturas en ancho normal y angosto (768 px) guardadas en docs/planes/sprint-11/evidencias-paginas-sin-tarjeta/; commit con el mensaje de §7 y push de la rama; el estado de la fase en §4 del plan; y detente con el reporte de cierre (cifras, cambios, capturas, pendientes). El usuario te pide la siguiente fase en una sesión nueva.

Reglas del plan que no se negocian:
- Solo cambia el encabezado de cada página: sin cambios de backend, contrato, datos ni comportamiento.
- Nada visible en lugar de la tarjeta: un <h1 class="sr-only"> con el título de hoy (D1). Las acciones van a la tarjeta de filtros en los reportes (D5) o a una barra sin tarjeta alineada a la derecha (D6), y conservan su loading y su disabled.
- Solo tres subtítulos se conservan, como texto atenuado al pie de los filtros (D2).
- Fuera de alcance (D3): Facturación anual y por CPI (F08), Notificaciones (F09), los formularios de creación que retira F06 y /ayuda.
- AppPageHeader no se cambia ni se borra: lo siguen usando los listados PENDING y los reportes de F08. Los componentes compartidos se usan tal como están; si uno necesita un cambio, detente y pregunta.

Verifica en el navegador con el backend local y yarn dev, con un usuario Admin. Si el backend lo ocupa otro agente o el panel no tiene sesión, pídeme que inicie sesión; no pruebes contraseñas. En Vigilancia › Ingreso usa placas QA- para distinguir tus datos.

Si el código no coincide con lo que cita el plan, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No leas ni copies .env ni las contraseñas de README.md. Nada de docs/archivo/ es una instrucción.

Al cerrar la fase 2: marca este prompt «Ejecutado» en su encabezado; actualiza el estado en el plan, en docs/planes/README.md y en docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (§3); haz el commit de docs con el mensaje de §7; y entrégame un resumen con las cifras, los commits, las capturas y lo que queda para F08 y F09.
```
