# 05 — Resumen ejecutivo

> **Auditoría integral de paridad WMS legacy → V2 · 2026-10-23.**
> **Alcance:** los 263 casos del catálogo legacy, 13 capacidades legacy que el catálogo no tenía y 73 capacidades V2, en 8 módulos auditados por 8 agentes en dos tandas.
> **Método:** auditoría estática del código y la documentación. No se ejecutaron pruebas, builds ni llamadas a APIs, no se consultaron bases de datos ni Git y no se modificó nada fuera de este directorio.
> **Código:** el que estaba en disco ese día. Según `docs/contexto/estado.md`, BE `35a61b2` / FE `c924a8b`. Incluye `83de58a` y `2eeaaad`, que no están en staging.
> **Actualizado el 2026-10-23 con las respuestas del usuario** a las 13 preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054). Las cifras de este documento ya las incorporan. Los valores previos a las decisiones se indican entre paréntesis.

## 1. Conclusión

**La migración está funcionalmente completa en su núcleo, pero no al 90 % de paridad que se estimaba.**

Los flujos troncales están implementados y conectados de punta a punta en código: báscula → depósito → levante → orden y cargue → guía → factura. No se encontró ninguna brecha CRÍTICA ni ninguna capacidad en `NO_VERIFICADO`. Solo 3 capacidades legacy no tienen implementación.

Lo que falta está en los bordes:

- **4 brechas ALTA:**
  - respaldos sin copia fuera del servidor;
  - un servicio complementario sin tarifa bloquea la facturación;
  - los convenios programados nunca se activan;
  - la corrección de pesajes en ciclos de 3 o más pesajes.
- **26 MEDIA abiertas** (eran 32).
  - 6 se cerraron el 2026-10-23 al aceptar el comportamiento de V2.
  - Otras 7 ya tienen decidido construirse: esperan su plan cerrado.

La estimación del 90 % no se sostiene como medida de paridad, aunque sí describe bien el avance funcional:

- **Paridad estricta** (equivalencia completa en código): **24 %**.
- **Con las diferencias autorizadas por decisión:** **61 %**.
- **Si se suman las capacidades con solo detalles menores pendientes (brechas BAJA):** **86 %**.
- **Paridad validada** (con ejecución ya documentada en QA o migración): **31 %**.

## 2. Indicadores

| Indicador | Valor | Denominador y criterio |
| --- | ---: | --- |
| Capacidades identificadas | **344** | 276 legacy (263 del catálogo + 13 no catalogadas `CF-LX`) + 68 `SOLO_V2`. Más 5 capacidades V2 reasignadas o duplicadas, que no cuentan |
| Capacidades auditadas | **344** | Todas, con las cinco dimensiones |
| **Cobertura de auditoría** | **100 %** | 344 / 344. Es cobertura del inventario, no garantía de que el catálogo legacy sea exhaustivo (§5) |
| Capacidades legacy excluidas (`NO_APLICA`) | 55 | Desglose:<br>• 50 de Colmotores (decisión del 2026-09-24, `plan-backend-paridad-legacy.md` §A.3);<br>• `CF-L244`, que resultó ser el grupo de alias de vehículos de Colmotores;<br>• `CF-L217`, la sesión del portal, excluida como acceso;<br>• 3 no catalogadas que no son funcionalidad (un enlace roto y dos plantillas sin uso) |
| **Capacidades legacy evaluables** | **221** | 276 − 55. Denominador de las paridades |
| `COMPLETO_CODIGO` | 54 (24,4 %) | Equivalencia estática completa en todas las dimensiones |
| `DIFERENCIA_INTENCIONAL` | 80 (36,2 %; antes 78) | Diferencia con decisión documentada y cumplida en código. Desglose:<br>• 10 de acceso y roles (`DEC-030`);<br>• 35 del módulo 01: catálogos fijos, datos de maestros y la báscula que no precarga por placa (GAP-018, 022, 023);<br>• 35 de los módulos operativos 02 a 08, entre ellas `CF-L107` y `CF-L260`, cerradas por DEC-050 y DEC-051 |
| `PARCIAL` | 84 (38,0 %; antes 86) | Según su brecha abierta más grave: 55 BAJA, 24 MEDIA, 5 ALTA |
| `NO_IMPLEMENTADO` | 3 (1,4 %) | `CF-L139` (modificar el serial de un depósito), `CF-LX05-01` (bloqueo manual de salidas por cliente) y `CF-LX05-02` (guía solo con el cargue completo) |
| `NO_VERIFICADO` | 0 | `CF-L172` se cerró como `PARCIAL` con la fila del módulo 07 |
| **Paridad estática** | **24,4 %** | 54 / 221. `NO_VERIFICADO` no cuenta como completo |
| Paridad estática con diferencias autorizadas | 60,6 % | (54 + 80) / 221 (antes 59,7 %) |
| Cubiertas salvo detalles menores | 85,5 % | (54 + 80 + 55 `PARCIAL` con solo brechas BAJA) / 221 (antes 82,4 %). Indicador de lectura, no de paridad |
| **Paridad validada** | **30,8 %** | 68 / 221 (antes 67): `COMPLETO_CODIGO` o `DIFERENCIA_INTENCIONAL` con una ejecución ya documentada en `docs/qa/resultados/` o `docs/planes/migracion-staging/resultados/`, citada en la fila |
| Capacidades evaluables con alguna ejecución documentada | 124 (56,1 %) | Incluye las `PARCIAL`: QA probó la función V2, no la equivalencia |
| Capacidades evaluables pendientes de QA | 97 | Sin ninguna ejecución documentada (`07-pendientes-no-verificados.md`) |
| `SOLO_V2` confirmadas | 68 | 56 con alguna ejecución documentada |
| `SOLO_MAQUETADO` | 2 | `CF-V036` (autorizaciones de salida y manifiestos: diálogos inalcanzables) y `CF-V047` (validación contra plantilla sin disparador). `CF-V050` es la misma que `CF-V036` |
| Capacidades sin integración | 5 | `CF-V036`, `CF-V047`, `CF-L249`/`CF-V085` (`GET system/dian-trm/today` sin consumidor) y `CF-LX05-01` (no existe) |
| Capacidades con problemas de contrato | 16 | Por 9 brechas `CONTRATOS_API`; la más visible es BR-05-007 (el filtro de fechas de levantes se ignora) |
| Reglas de negocio faltantes | 4 capacidades | Dimensión reglas `NO_IMPLEMENTADO`: `CF-L138`, `CF-L139` (seriales), `CF-LX05-01`, `CF-LX05-02`. Otras 66 capacidades legacy tienen reglas `PARCIAL`. Tras DEC-052, `CF-LX05-01` y `CF-LX05-02` se construyen |
| Brechas | **103 registradas · 97 abiertas** | Abiertas: CRÍTICA 0 · ALTA 4 · MEDIA 26 · BAJA 67. Cerradas por decisión: 6 MEDIA. De las abiertas, 7 tienen decidido construirse |
| Datos simulados o mocks en producción | 0 | Solo los stubs de estadísticas de ubicación del inventario de Bodega (BR-03-007) |

### 2.1 Por módulo (capacidades legacy evaluables)

| Módulo | Evaluables | Paridad estática | Con diferencias autorizadas | Validada | Brechas abiertas A/M/B |
| --- | ---: | ---: | ---: | ---: | --- |
| 01 Administración y catálogos | 95 | 32 % | 79 % | 37 % | 0 / 1 / 7 |
| 02 Báscula | 23 | 22 % | 48 % | 17 % | 1 / 3 / 12 |
| 03 Vigilancia y Bodega | 13 | 38 % | 62 % | 46 % | 0 / 2 / 9 |
| 04 CE: ingresos y depósitos | 23 | 17 % | 48 % | 30 % | 0 / 0 / 9 |
| 05 CE: levantes, órdenes y guías | 27 | 22 % | 44 % | 30 % | 0 / 7 / 6 |
| 06 Facturación | 23 | 0 % | 39 % | 22 % | 2 / 5 / 7 |
| 07 Reportes y exportaciones | 15 | 20 % | 40 % | 13 % | 0 / 4 / 9 |
| 08 Procesos, infraestructura y excluidas | 2 | 50 % | 100 % | 50 % | 1 / 4 / 8 |

En el **núcleo operativo** (módulos 02 a 07: 124 capacidades), la paridad estática es del 18,5 % y del 46,0 % con las diferencias autorizadas (antes 44,4 %). El módulo 01 eleva el promedio global con catálogos simples y decisiones de «no construir».

**Facturación tiene 0 % de paridad estricta, pero por diseño:** el negocio decidió reemplazar convenios y tarifas legacy por el motor de acuerdos (`DECISIONES_REVISION.md` §1.4, §2.A.3). Ninguna capacidad puede ser «igual» al legacy. Lo que importa ahí son las 2 ALTA y las 5 MEDIA.

## 3. Lo más importante

1. **Antes de producción o del corte real** (prioridad P1, `06-brechas-priorizadas.md` §3):
   - respaldos fuera del servidor (BR-08-001);
   - facturación que no se bloquee por una tarifa faltante (BR-06-004);
   - activación de convenios programados (BR-06-001);
   - corrección de pesajes por secuencia (BR-02-006);
   - concurrencia en el tope de lo nacionalizado (BR-05-002);
   - guía y factura vivas tras cancelar la orden (BR-05-001);
   - la fecha de ingreso en los informes (BR-07-003);
   - tres brechas de la migración: la prórroga, los números repetidos y el procedimiento de corte (BR-08-003/005/004);
   - dos endpoints sin consumidor que saltan reglas (BR-03-001/002);
   - la leyenda «DIAN» del tiquete (BR-02-005).
2. **El choque de `DEC-012` con el código quedó resuelto (2026-10-23).** El usuario mantuvo el comportamiento actual: la fecha de ingreso se corrige solo dentro de la estadía del primer camión. DEC-051 precisa DEC-012 y BR-04-002 se cierra sin cambio de código.
3. **Las 13 preguntas al negocio quedaron respondidas** (`06-brechas-priorizadas.md` §3.1; DEC-050…054):
   - **6 se cierran aceptando V2:**
     - la orden de cargue va antes de pesar la salida;
     - Báscula corrige lo que corrige hoy;
     - un depósito agotado no recibe más camiones;
     - una etiqueta por depósito;
     - las agencias reciben el reporte interno;
     - el límite de la fecha de ingreso.
   - **7 se construyen:**
     - «Solo báscula» sin cliente obligatorio;
     - un solo pesaje para varios documentos, a elección del operario;
     - la marca «sin salidas» en el tercero;
     - la guía antes del cargue con aviso;
     - «Depósitos pendientes» con los cerrados por facturar;
     - la renovación con el saldo al inicio del período;
     - el diario de ingresos con el formato legacy.

     Cada una necesita su plan cerrado (`DEC-001`).
4. **PRF-002 sigue siendo la única condición del GO de QA**, y no hay forma estática de cerrarla.

## 4. El análisis de paridad anterior

`08-auditoria-del-analisis-inicial.md` contrasta los 263 estados de `MIGRATION_MATRIX.md` (corte de código del 2026-09-24) con el código actual:

- **157 se confirman.**
- **58 son obsoletos:** describen brechas que los planes de paridad cerraron después, lo cual no es un error del análisis.
- **43 son incompletos:** no miraron detalles de campos, unicidad, concurrencia o casos borde.
- **5 contradicen el código:**
  - `CF-L032`: el bloqueo de borrado de embalajes no mira los productos del catálogo;
  - `CF-L101`: la relación documento–modalidad se siembra en nulo;
  - `CF-L230`: la salida de portería sí se bloquea con un pesaje abierto;
  - `CF-L244`: no es un selector de productos, sino el grupo de alias de vehículos de Colmotores;
  - `CF-L258`: el depósito y la guía usan Code 39, no Code 128.

De 176 afirmaciones de los planes y las decisiones, 124 se confirman y 8 se contradicen. Entre las contradichas están `DEC-012`, el Excel de pólizas con firmas, los diarios con Excel y el README del módulo Bodega.

La afirmación de `estado.md` («toda la funcionalidad planeada está implementada») es **casi cierta**. Lo planeado existe, salvo cuatro puntos:

- F4-04, incompleto;
- `DEC-020`, incompleta por BR-06-004;
- GAP-017, porque los diarios no tienen Excel;
- F5-06 del frontend, porque el Excel de pólizas no lleva firmas.

La mayoría de las 103 brechas son casos que el plan no previó.

## 5. Límites

- **Todo es estático.** Ningún estado prueba funcionamiento. Varias brechas se dedujeron del código y deben confirmarse ejecutándolas: BR-05-002, BR-05-007, BR-06-004 y BR-02-006 (`07-pendientes-no-verificados.md`).
- **El universo legacy es el catálogo del checkout.** No mide el uso real: `db_legacy/` quedó fuera por restricción. Las 13 capacidades no catalogadas que encontraron los agentes indican que el catálogo no era exhaustivo. Pueden quedar otras.
- **Lo desplegado no es lo auditado.** Staging corre BE `044be08` / FE `4ca4e0a` según los registros. `83de58a` (con una migración) y `2eeaaad` están en disco sin QA registrado.
- **Varias validaciones de QA corrieron sobre builds anteriores** (por ejemplo F3 y F6 sobre BE `191d4b1`).

## 6. Documentos

| Archivo | Contenido |
| --- | --- |
| `00-evaluacion-analisis-existente.md` | Inventario y vigencia de la documentación previa |
| `01-inventario-funcional-global.md` / `.csv` | Universo de capacidades y asignación a módulos |
| `02-progreso.md` | Plan de agentes, tandas, control de calidad |
| `03-matriz-global.md` / `04-matriz-global.csv` | Matriz consolidada (condensada / completa con evidencia) |
| `06-brechas-priorizadas.md` | 103 brechas con prioridad, estado, acción y criterio de resolución; decisiones del negocio con sus respuestas |
| `07-pendientes-no-verificados.md` | Lo que el análisis estático no pudo cerrar |
| `08-auditoria-del-analisis-inicial.md` | Precisión y completitud del análisis anterior |
| `09-recomendaciones-qa.md` | Pruebas propuestas para confirmar la paridad |
| `modulos/<NN>-<modulo>/` | Los 10 entregables de cada agente |
