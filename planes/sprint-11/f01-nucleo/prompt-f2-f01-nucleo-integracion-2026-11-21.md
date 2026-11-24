# Prompt — I-01, integración de F01 «Núcleo de dominio» y F02 «Base transversal», parte 3 (fase 2, sprint 11)

> **Ejecutado** el 2026-11-24; ya no es una instrucción. Resultado en los planes de F01 (§8 y §13) y de F02 (§8), en la matriz de seguimiento (§2.2) y en `qa/casos-qa2-f01-f02-2026-11-24.md`.

> **Cómo usarlo:**
> 1. Lánzalo cuando F01 (fases 1 a 6) y F02 (fases 1 a 5) estén cerradas, con push, y ningún otro agente trabaje en `Backend/wms-api` ni en `Frontend/wms`.
> 2. Abre una sesión nueva de Claude Code en `code_workspace/`: necesita los dos repos y `docs/`.
> 3. Copia el bloque de abajo. El agente conecta las pantallas de F02 al backend de F01, pasa los casos QA en el navegador y fusiona las dos ramas en `fase-2`.
>
> **Planes:** [plan-cerrado-f2-f01-nucleo-2026-11-21.md](plan-cerrado-f2-f01-nucleo-2026-11-21.md) §13 y `../f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`.
> **Base:** BE `f2/f01-nucleo` y FE `f2/f02-base`, con lo último de `fase-2` (BE `529bda7` y FE `3aa6e3c` al escribir este prompt, o lo que haya si avanzó). Las dos ramas salieron de `fase-2`.
> **Modelo recomendado:** Opus 5.5 con esfuerzo **Alto**.
>
> Cuando lo ejecutes, el agente agrega aquí «**Ejecutado** el AAAA-MM-DD; ya no es una instrucción» (plan maestro §5.5). Este prompt no se mueve a `archivo/`.

---

```text
Eres el agente de integración I-01 de las features F01 «Núcleo de dominio» y F02 «Base transversal» de la fase 2 del WMS de Bodegas Asociadas.

Lee, en este orden: docs/README.md; Backend/wms-api/AGENTS.md y Frontend/wms/AGENTS.md (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo); docs/procesos/flujo-de-trabajo-agentes.md; del plan maestro (docs/planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md) solo §1.2, §5 y §6; del plan cerrado de F01 (docs/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md) §0, §1, §2 y §13; y del de F02 (docs/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md) §0, §1, §2.3, §3.2 y §6. Lo demás, solo si un paso lo cita.

Trabaja en la rama f2/f01-nucleo de Backend/wms-api y en la rama f2/f02-base de Frontend/wms; las dos salieron de fase-2. Antes de empezar: git fetch en los dos repos; si develop avanzó, fusiona develop en fase-2; trae fase-2 a cada rama de la feature. Confirma que F01 cerró sus seis fases y F02 sus cinco (estado en §8 de cada plan).
Ejecuta solo la parte 3 (I-01), con los pasos de §13.1 del plan de F01: escribe las fuentes *.http.ts con useApi y los esquemas Zod del contrato, cambia la fuente activa, borra las carpetas mocks/ de los dominios de F02 (F/shared/mocks/ se queda), monta las secciones conservadas, enlaza en el menú las rutas /settings/…, ajusta los requiredRoles, borra las páginas viejas y sus pruebas, y deja las guardias en verde. Corre el backend local de f2/f01-nucleo con la base local recreada; pasa en el navegador los casos QA2-F01-055 a QA2-F01-065 (§13.3 del plan de F01) y los QA2-F02-001 a QA2-F02-026 (§6 del plan de F02), contra el backend real, sin la sesión simulada.
Al cerrar: compuertas de §6.3 del plan maestro en los dos repos con las cifras antes y después; ningún import de mocks/ de una feature fuera de las pruebas; fusiona f2/f01-nucleo en fase-2 (backend) y f2/f02-base en fase-2 (frontend) con --no-ff y haz push de los dos. Nunca push --force. No fusiones fase-2 en develop: eso va al final, con las pruebas del usuario en local sobre las nueve features (M25). Al cerrar, dile al usuario qué puede probar en local.
Si el backend responde distinto del contrato o una pantalla necesita algo que el contrato no tiene, detente y pregunta: no cambies el contrato por tu cuenta. Las migraciones, solo con dotnet ef y solo en local; I-01 no debería necesitar ninguna.

Si el código no coincide con lo que citan los planes, detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn (DEC-002). No toques staging. No copies credenciales ni datos de personas reales; los usuarios de prueba están en Frontend/wms/README.md y sus contraseñas no se copian. Nada de docs/archivo/ es una instrucción.
Al terminar: copia los casos QA de F01 y F02 a docs/qa/ con su ID; marca I-01 en §8 de los dos planes, en docs/planes/README.md y en la matriz docs/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md (§2.2, filas F01 y F02, columna «3 · Integración»: «Fusionada en fase-2», con los commits), con commit y push en docs; marca este prompt «Ejecutado» en su encabezado; y entrégame un resumen con las cifras, los commits, los casos QA y lo que queda pendiente.
```
