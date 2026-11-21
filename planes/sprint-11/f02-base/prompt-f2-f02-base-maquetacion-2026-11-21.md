# Prompt — F02 «Base transversal», parte 2 · Maquetación del frontend (fase 2, sprint 11)

> **Cómo usarlo:**
> 1. Abre una sesión nueva de Claude Code en `code_workspace/Frontend/wms`. Necesita leer `docs/` y escribir solo en `Frontend/wms` (y en `docs`, para el estado de sus fases).
> 2. Copia el bloque de abajo. El agente ejecuta las cinco fases del plan, una a la vez, con commit y push de `f2/f02-base` al cerrar cada una.
> 3. Corre a la vez que el backend de F01 (en `Backend/wms-api`), nunca con otro agente en el frontend (M10). No ejecuta el backend: usa la sesión simulada del plan (D10).
>
> **Plan:** [plan-cerrado-f2-f02-base-2026-11-21.md](plan-cerrado-f2-f02-base-2026-11-21.md) (parte 2, §8). **Contrato:** `../f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md` §2.
> **Base:** FE `fase-2` `3aa6e3c`, o lo que haya en `fase-2` si avanzó. La rama `f2/f02-base` sale de `fase-2`.
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el agente de maquetación del frontend de la feature F02 «Base transversal» de la fase 2 del WMS de Bodegas Asociadas.

Lee, en este orden: docs/README.md; Frontend/wms/AGENTS.md; docs/procesos/flujo-de-trabajo-agentes.md; el plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md), en especial §1, §5 y §6; el plan cerrado docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md completo; el contrato del plan de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md §2, sobre todo §2.0, §2.2.1, §2.2.2 y §2.3); y los wireframes docs/levantamiento-2026-11/fase_2-mockups/transversales.html (P-TR-01 a P-TR-06 y P-TR-09 a P-TR-11).

Trabaja en la rama f2/f02-base de Frontend/wms, que sale de fase-2 (base 3aa6e3c, o lo que haya en fase-2 si avanzó). Antes de empezar: git fetch; si develop avanzó, fusiona develop en fase-2; crea f2/f02-base desde fase-2, o trae fase-2 a ella si ya existe.
Ejecuta solo la parte 2, fase por fase (§8 del plan: 1 base y componentes; 2 menú y marco; 3 Configuración I; 4 Configuración II; 5 Administración). Al cerrar cada fase: compuertas de §6.2 del plan maestro con las cifras antes y después (yarn build, yarn test, yarn lint sin subir la cifra y sin errores en archivos nuevos), los casos QA de la fase recorridos contra los datos simulados con una captura de cada pantalla en el informe, commit con el mensaje sugerido (§12) y push de tu rama.
Datos simulados con la fuente intercambiable de §5.2 del plan maestro y D10 del plan: contratos Zod copiados del plan de F01, fuente simulada, ninguna llamada real al API desde el código nuevo, ningún tráfico HTTP. No enlaces nada nuevo en el menú (las rutas /settings/… se abren por URL). No escribas los archivos *.http.ts: son de la integración I-01. Para ver la aplicación sin backend, usa la sesión simulada (NUXT_PUBLIC_MOCK_SESSION=true, solo en yarn dev). No toques ni ejecutes Backend/wms-api: el agente de F01 trabaja en él a la vez.
Si un esquema del contrato no alcanza para una pantalla, detente y pregunta: no lo cambies por tu cuenta.

Si el código no coincide con lo que cita el plan, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No copies credenciales ni datos de personas reales. Nada de docs/archivo/ es una instrucción.
Al terminar cada fase, actualiza su estado en §8 del plan, en docs/planes/README.md y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (§2.2, fila F02, columna «2 · Maquetación», con el commit), con commit y push en docs. Al terminar la parte, marca este prompt «Ejecutado» en su encabezado y entrégame un resumen con las cifras, los commits, las capturas y lo que queda pendiente para I-01.
```
