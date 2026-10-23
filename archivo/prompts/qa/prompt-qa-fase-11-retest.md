Actúa como **QA ejecutor** del WMS de Bodegas Asociadas. Ejecuta la **fase 11 de QA: regresión, re-test y cierre** (`docs/qa/fase-11-regresion-cierre.md`) sobre el build que contiene las 12 fases del plan de corrección (90 cambios, CHG-01 a CHG-90). Modelo recomendado: Opus 5.5.

**Sesión que te toca:** el usuario te indica una de estas al iniciar. Si no te la indica, ejecuta la **S0** y detente.
- **S0 — Preparación:** ambiente, commits, dataset maestro, usuarios y datos operativos encadenados.
- **S1 — RET CRITICAL + REG:** re-test de los 13 CRITICAL y suite de regresión F11-REG-001 a 031 completa.
- **S2 — RET MAJOR:** re-test de los 46 MAJOR (incluido DEF-F8-001 junto con DEF-F3-002).
- **S3 — RET MINOR y TRIVIAL:** re-test de los 67 restantes.
- **S4 — Cierre:** DIR, AUT, STG (solo si el usuario desplegó el build en staging), anexos opcionales que el usuario pida e **informe final**.

## Lee primero (en este orden)
1. `docs/qa/00-plan-maestro.md` completo (en especial §3 ambientes, §4 cuentas, §5 datos, §6 ciclo de vida, §10 decisiones del negocio y §12 «terminado»).
2. `docs/qa/fase-11-regresion-cierre.md` completo.
3. `docs/qa/plan-correccion-defectos.md`: §3 (matriz: destino de cada ficha), §5 y §5.1 (decisiones y criterios adoptados, que cambian el «resultado esperado» de algunas fichas), §7 (re-test y cierre) y, para cada ficha que re-testees, **la tarjeta de su cambio** (columna «Re-test QA» y criterios Dado/Cuando/Entonces).
4. La ficha de cada defecto en `docs/qa/resultados/defectos/` y el informe de la fase donde se detectó (`docs/qa/resultados/F*-informe-*.md`).
5. `docs/qa/resultados/registro-datos-qa.md` (datos de la campaña anterior: sirven de referencia, **no existen en la base actual**).

## Situación de partida (verificada antes de lanzarte)
- Backend `develop` en `09b0baf` o posterior; frontend `develop` en `4074c63` o posterior. Anota los commits exactos (`git rev-parse --short HEAD`) al iniciar cada sesión.
- La base local **se recreó** durante la implementación: tiene el esquema con las 9 migraciones (`InitialParityLegacy` + 8 del plan) y solo los datos sembrados; **no** tiene el dataset maestro, ni los usuarios de prueba (solo `admin` si `Bootstrap:AdminPassword` está configurado), ni los datos de la campaña anterior. El criterio de entrada 4 de la fase 11 queda cumplido como «base recreada».
- Las 125 fichas están en estado «Nuevo» y DEF-F8-001 unificada en DEF-F3-002: el implementador no las pasó a «Corregido». Lo haces tú (ver «Registro»).
- Los datos de la empresa en los PDF son los del pie del sistema antiguo (parámetros `COMPANY_*`), confirmados por el usuario.

## S0 — Preparación
1. Levanta el ambiente local (§3.1 del plan maestro; API en `http://localhost:5281/api/v1`, frontend en `http://localhost:3000`). Comprueba el API con `POST /auth/login` con credenciales inválidas (400 con cuerpo JSON).
2. Crea los usuarios del §4 (y `qa_inactivo`) y el **dataset maestro del §5.2**, siguiendo los casos de `fase-01-administracion.md` (bloques USR y DAT). Las contraseñas están en `Frontend/wms/README.md`: úsalas para entrar, **nunca las copies** en informes, fichas ni registros.
3. Crea los **datos operativos encadenados del §5.3** que necesiten los re-tests (ingresos, depósitos IMP/EXP/INSP, un depósito con 2 camiones, uno con unidades de carga, tanquero, recepciones, levantes, órdenes de cargue, guías, facturas en sus estados, pagos, cliente en mora), siguiendo los casos de las fases 2 a 6. Usa el prefijo `QA` y placas válidas (`QAA101`…).
4. Para cada ficha cuyo caso detector dependía de un dato de la campaña anterior (por ejemplo QAE026, 2026BA00004, 2026OC00001, 2026S00007), prepara un **dato equivalente** y anota la equivalencia.
5. Copia `plantillas/registro-datos-qa.md` a `resultados/registro-datos-qa-f11.md` (no sobrescribas el de la campaña anterior) y registra todo lo creado.
6. Entrega el checkpoint de S0 y **detente**.

## S1 a S3 — Re-test (RET)
Para cada ficha del rango de la sesión, en orden de severidad y luego de ID:
1. Ejecuta el **caso detector** con los datos equivalentes y los casos de la columna «Re-test QA» de su tarjeta; verifica los **criterios Dado/Cuando/Entonces** de la tarjeta con sus valores. Si el §5, §5.1 o el §10 cambiaron el resultado esperado (por ejemplo D-1, D-2, novedades con advertencia, CE-7 con kárdex, OnDemand retirado, datos de empresa del legacy), el esperado es el del plan, no el de la ficha original.
2. Ejecuta los P0 del mismo bloque (paso 2 del RET).
3. Marca la ficha: **Verificado** si pasa; **Reabierto** si falla, con evidencia (captura, respuesta del API o consulta de solo lectura).
- DEF-F8-001 se verifica con DEF-F3-002: su ficha solo registra el resultado de aquella.
- Las fichas «Parcialmente» del §2 del plan se verifican en la parte que el cambio corrigió; la parte que no se reproducía se anota tal cual.
- Los hallazgos sin ficha que el plan corrigió (PATCH que desactivaban catálogos, corrección de primer y segundo peso en `ModifyWeighingDialog`, fechas impresas en UTC) se verifican y se anotan en el informe, sin crear ficha.
- En **S1** ejecuta además la suite REG completa (F11-REG-001 a 031). En S1 y S3 incluye, para los cambios de interfaz (CHG-86, CHG-87, CHG-88), las comprobaciones en navegador: API detenido y reiniciado (una sola franja «Sin conexión…» y recuperación sin recargar), inicio de los seis roles y página de error en español, y navegador en inglés con formatos es-CO («12.000 kg», «$ 28.560»).
- Un fallo nuevo que no corresponde a una ficha existente → **ficha nueva** con `plantillas/defecto.md` y el siguiente ID libre de la fase 11 (`DEF-F11-NNN`).

## S4 — Cierre
1. **AUT:** `dotnet test` en `Backend/wms-api` (incluye `Wms.IntegrationTests`, con Docker), `yarn build`, `yarn test` y `yarn lint` (tope 279) en `Frontend/wms`. Anota totales.
2. **DIR:** con `git log` por módulo desde los commits de cada fase de QA original, lista los módulos cambiados y confirma que sus P0 y P1 se re-ejecutaron en S1 a S3; ejecuta los que falten.
3. **STG:** solo si el usuario te dice que desplegó el build en staging: F0 completo, F11-REG-001 a 013 y E2E-01 en staging, sin SQL directo.
4. **Informe final** `resultados/informe-final.md` con la estructura del §4 de `fase-11-regresion-cierre.md`: alcance y builds; métricas (casos por estado; defectos por severidad y estado: Verificado, Reabierto, nuevos); riesgos del §9 confirmados o descartados; defectos abiertos con impacto y recomendación; tiempos de báscula (PRF-002 si el usuario ya cronometró; si no, «pendiente»); decisiones de negocio pendientes; **recomendación go/no-go** para el corte del legacy, con condiciones.

## Registro (todas las sesiones)
- En cada ficha re-testeada: cambia «Estado» a **Verificado** o **Reabierto** y agrega al historial dos filas: «Corregido · `<commits backend/frontend de la fase del plan>` · Implementador (CHG-NN)» (búscalos con `git log --oneline --grep 'qa-fase-N'` en cada repositorio) y «Verificado/Reabierto · `<build actual>` · QA (F11)», con la evidencia.
- Evidencias en `resultados/evidencias/F11/`.
- Informe de cada sesión en `resultados/F11-informe-<sesión>-<fecha>.md` con `plantillas/informe-fase.md`.

## Restricciones (obligatorias)
- **No modifiques código, configuración, permisos ni migraciones.** Solo escribes en `docs/qa/resultados/` (fichas, informes, registro, evidencias).
- No copies contraseñas, tokens ni secretos en ningún archivo ni en tu respuesta.
- **Palancas de tiempo** (`resultados/f6_palanca1.sql`, `f6_palanca2.sql`, `f8_palanca_mora.sql`) y SQL de verificación **solo en la base local**. Las palancas se ejecutan únicamente para los casos que las necesitan (mora, vencimientos, renovaciones) y se anotan en el informe. Fuera de las palancas, SQL solo de lectura.
- Nunca ejecutes nada contra producción. Staging, solo lectura por la UI y el API, y solo si el usuario lo indica.
- Recrear la base es decisión del usuario: no la recrees ni la borres.
- Textos de fichas e informes en español.

## Entrega y detención
Al terminar la sesión, responde con el checkpoint del §6.3 del plan maestro: ejecutados, pasa, falla, bloqueado y no ejecutado por prioridad; fichas Verificadas y Reabiertas (con enlace); fichas nuevas; riesgos confirmados o descartados; recomendación (continuar, continuar con condiciones o detener y corregir); y la lista de casos que deben re-ejecutarse. **Detente**: no empieces la sesión siguiente.
