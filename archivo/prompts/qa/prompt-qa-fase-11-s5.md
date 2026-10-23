Eres el ejecutor de QA de la **sesión S5** de la fase 11 (regresión, re-test y cierre) del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5**. La S5 la pidió el usuario el 2026-10-06 después del informe final de S4. Tiene dos partes, en este orden:

- **Parte A — Re-test posterior a S4 (P0).** Verifica la corrección de DEF-F11-017 (CRITICAL) y DEF-F11-016 (MAJOR). Decide el veredicto.
- **Parte B — P1 de la regresión dirigida.** Ejecuta, por ID, los P1 de **Báscula (F3), Comercio Exterior (F5) y Facturación (F6)** que no se re-ejecutaron en la fase 11. Es la condición 4 del §7 del informe final.

Al terminar, **actualizas el informe final**.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/archivo/prompts/qa/prompt-qa-fase-11-retest.md`. Es el marco de la fase 11: **sus reglas de registro, restricciones y entrega valen aquí sin cambios.**
3. `docs/qa/resultados/informe-final.md`, en especial §4, §7 y §8, y `F11-informe-S4-2026-10-06.md`, en especial §4.3 DIR y §8.
4. Las fichas `docs/qa/resultados/defectos/DEF-F11-016.md` y `DEF-F11-017.md`, con su fila «Corregido».
5. `docs/qa/fase-03-bascula.md`, `fase-05-comercio-exterior.md` y `fase-06-facturacion.md`: los casos P1.
6. `docs/qa/resultados/registro-datos-qa-f11.md`: datos disponibles y equivalencias con la campaña.

## Situación de partida
- **Build:** BE **`00d6ac3`** (corrección de DEF-F11-016 y DEF-F11-017) / FE **`bd729e5`** (último cambio de código: `e41decf`). El usuario reinicia el API sobre `00d6ac3` antes de lanzarte. Anota en el informe los commits que encuentres corriendo.
- **Ambiente:** local. La base es la del re-test, con el dataset de S0 a S4: **no la recrees**.
- **Decisiones vigentes del usuario (2026-10-06):**
  - todo el re-test es local;
  - el bloque STG y PRF-002 están **«Diferido a staging»** y no se ejecutan;
  - el veredicto se basa en local.

---

## Parte A — Re-test posterior a S4 (hazla primero)

1. **DEF-F11-017, recálculo del almacenamiento.**
   - Repite el caso de la ficha: depósito de 40 bultos confirmado, 30 cargados y despachados dentro del período, y un CE-7 (41 y luego 40) que dispara el recálculo.
   - **Esperado:** la línea cobra 41 y luego 40 bultos (no 11 y 10). La factura conserva su N.º y su aprobación, y Facturación recibe el aviso con el total anterior y el nuevo.
   - Anota los totales antes del despacho, después del primer recálculo y después del segundo.
   - Ejecuta además, con despachos parciales:
     - F6-REC-001, 002 y 004;
     - F6-ALM-002 y 012;
     - F11-REG-021.
   - Si un caso necesita una renovación o un cierre de período, usa la palanca correspondiente **solo en la base local** y anótalo.
2. **DEF-F11-016, camión que salía de la cola de báscula.**
   - **QAK504**, el ingreso que quedó fuera en S4, debe aparecer en la cola sin tocar datos.
   - Ejecuta F2-COR-011 con un ingreso nuevo con conductor: tras corregir el motivo, sigue en la cola con el motivo nuevo.
   - Edita un ingreso desde Vigilancia: sigue en la cola. Registra la salida: sale de la cola.
   - Ejecuta también F11-REG-005 y 006.
3. **Registro.** En las dos fichas y en `INDICE.md`, «Verificado» o «Reabierto», con la fila de Historial que pide el marco y el commit `00d6ac3`.

**Si cualquiera de los dos se reabre, detente al terminar la Parte A** y entrega el checkpoint. No hagas la Parte B ni toques el veredicto.

---

## Parte B — P1 de Báscula, Comercio Exterior y Facturación

1. **Inventario.** Arma la lista de los casos **P1** de `fase-03-bascula.md`, `fase-05-comercio-exterior.md` y `fase-06-facturacion.md` que **no** se ejecutaron por ID en la fase 11.
   - Crúzala con las evidencias de S0 a S4 y con §4.3 DIR del informe de S4: los 94 P1 ya ejecutados no se repiten.
   - Deja el inventario en `resultados/F11-S5-inventario-P1.md` con ID, módulo, título y estado.
   - **Cuenta esperada:** unos 170. Si la cifra difiere más de un 10 %, anota por qué.
2. **Ejecución.**
   - Ejecuta cada caso por ID, con el rol dueño, por API y en pantalla según lo que pida el caso.
   - Reutiliza los datos de `registro-datos-qa-f11.md` antes de crear datos nuevos, y anota los que crees.
   - Un caso que dependa del ambiente desplegado (correo real, DIAN desde staging, respaldos) se marca «Diferido a staging» y se agrega a §8 del informe final.
3. **Fallas.**
   - Un FALLA que corresponde a una ficha existente → **«Reabierto»** en esa ficha.
   - Un FALLA nuevo → ficha **`DEF-F11-018`** en adelante, con `plantillas/defecto.md`.
   - Las diferencias de texto o de formato que no bloqueen el caso van como observación, en la misma clasificación de S4 (§4.4 y §4.5): «aceptada para el corte» o «backlog». No abras ficha por ellas.
4. **Si la sesión no alcanza**, divídela:
   - **S5-A:** Parte A y P1 de Báscula;
   - **S5-B:** P1 de Comercio Exterior y Facturación, y la actualización del informe final.

   Al final de S5-A, entrega el checkpoint y **detente**. El usuario lanza S5-B con otro agente usando este mismo prompt.

---

## Informe de la sesión y actualización del informe final

1. **Informe de la sesión.** `resultados/F11-informe-S5-2026-10-06.md` (o `S5-A` y `S5-B` si la divides), con la plantilla `plantillas/informe-fase.md` y la misma estructura de S4:
   - datos de ejecución;
   - resumen por bloque;
   - resultado por caso;
   - defectos nuevos;
   - riesgos;
   - datos creados;
   - criterios de salida;
   - checkpoint.
2. **Informe final (`informe-final.md`)**, solo al cerrar la Parte B completa:
   - **§2.2:** agrega la fila S5; actualiza los P1 DIR (94 + los ejecutados en S5, de 341).
   - **§2.3 y §2.4:** las cifras de fichas con lo que cambie.
   - **§4 y §7, veredicto:**
     - **sin CRITICAL ni BLOCKER abiertos** → **«GO condicionado»**;
     - con algún CRITICAL o BLOCKER abierto → sigue **NO-GO**, con la causa.
   - **Condiciones que quedan para pasar a GO:**
     - el bloque de staging y PRF-002 (§8);
     - el Anexo A, si el corte usa datos migrados;
     - los MAJOR o MINOR que abra la S5, para corregir o aceptar por escrito;
     - los P1 de los demás módulos (F0, F1, F2, F4, F7, F8, F9 y F10) que siguen sin ejecución por ID. Anótalos como **«aceptados con cobertura indirecta»**: el RET de las fichas y las pruebas automatizadas. Indica la cifra.
   - **§8:** agrega los casos que hayas marcado «Diferido a staging».
   - El corte y la fecha del encabezado pasan a los de la S5.

## Restricciones (obligatorias, además de las del marco)
- **No modifiques código, configuración, permisos ni migraciones.** Solo escribes en `docs/qa/resultados/`.
- No copies contraseñas, tokens ni secretos en ningún archivo ni en tu respuesta.
- **Palancas y SQL de escritura solo en la base local**, solo para los casos que los necesiten, y anotados en el informe. Si creas una palanca nueva, guárdala como `resultados/f11_palanca_s5.sql`. Fuera de las palancas, SQL solo de lectura.
- **No reinicies el API ni el frontend.** Si un caso lo necesita (por ejemplo, la corrida de un job), pídeselo al usuario y espera.
- No recrees ni borres la base. Restaura los datos de prueba que cambies para un caso, como en S3 y S4.
- Textos en español.

## Entrega y detención
Responde con el checkpoint del §6.3 del plan maestro:
- ejecutados, pasa, falla, bloqueado, no ejecutado y diferido a staging, por parte y por módulo;
- fichas Verificadas y Reabiertas (con enlace) y fichas nuevas;
- riesgos confirmados o descartados;
- el veredicto actualizado del informe final, o por qué no se actualizó;
- la lista de casos que deben re-ejecutarse;
- el mensaje de commit de la documentación, listo para pegar: `docs(qa-f11): sesión S5, re-test de DEF-F11-016 y DEF-F11-017, P1 de Báscula, Comercio Exterior y Facturación, e informe final actualizado`, con un resumen por línea y la línea de coautoría que corresponde a tu modelo.

**Detente ahí.**
