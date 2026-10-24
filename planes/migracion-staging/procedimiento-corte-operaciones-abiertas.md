# Procedimiento del corte: congelamiento y operaciones abiertas

> **Para qué sirve:** cerrar o rehacer lo que está abierto en el legacy el día del corte real, para que la migración no deje camiones, órdenes, guías ni facturas a medias. Es el paso «0. Congelamiento y conteo» de `plan-migracion-legacy-staging.md` §3, regla 4.
> **Origen:** brecha BR-08-004 de la auditoría de paridad (`analisis/auditoria-paridad-integral-2026-10-23/06-brechas-priorizadas.md`) y decisiones D30 y D31 de `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md` (§15.1). Respuesta del usuario del 2026-10-23.
> **Fecha:** 2026-10-24. Backend `develop` `560f558`, frontend `develop` `e2e11e6`.
> **Estado:** procedimiento escrito, **sin ensayar**. Se ensaya con el volcado nuevo del legacy (`DEC-040`: el corte real exige un volcado nuevo y repetir las fases 1 y 3 de la migración).
> **Sin datos de personas** (`DEC-007`): los conteos y el informe llevan códigos, números de depósito y cifras. Las consultas las corre el usuario en la MariaDB de trabajo (`db_legacy/trabajo/`, fuera de git); este documento solo las describe.

## 1. Ventana y responsables

| Qué | Cómo |
| --- | --- |
| **T0** | Al cierre de la jornada, sin camiones en planta. Es la hora del volcado que se migra |
| **T−1** | La jornada anterior, a la misma hora. Sirve de ensayo de los conteos |
| **Desde T0 en el legacy** | Solo se consulta y se cobra cartera. No se registran ingresos, pesajes, depósitos, órdenes, salidas ni guías (D31) |
| **Quién opera cada paso** | Usuario: corre los conteos y decide cada excepción. Operarios de cada área: terminan o anulan lo suyo antes de T0. Comercio Exterior y Facturación: rehacen en V2 lo que se anuló. Agente: describe, concilia con la herramienta del producto y redacta el informe |
| **Qué se congela** | La operación del legacy durante la ventana. V2 recibe la migración y arranca con los depósitos vivos (corte simulado: `DEC-040`) |

Todo lo abierto se **termina antes de T0** o se **rehace en V2 después de migrar**. No se migran operaciones a medias.

## 2. Conteos en el legacy (T−1 y T0)

Los conteos usan los mismos filtros de F6-03 (`planes/paridad-legacy/plan-backend-paridad-legacy.md`): sin registros `eliminado` y sin el importador 70 (Colmotores). Cada conteo se entrega por **modalidad** y como número, más la lista de números de depósito, de orden o de factura afectados (sin nombres).

> **Advertencia:** las tablas y columnas citadas salen de `bodegas-legacy/bodegas_schema.sql` y de las consultas de F6-03. **Se validan contra el volcado nuevo** antes de usarlas: el esquema puede haber cambiado desde el volcado de 2024. Si una columna no existe, se ajusta la consulta y se documenta la diferencia en el informe (`db_legacy/trabajo/consultas/`).

| Conteo | Qué mide | Dónde mirar en el legacy |
| --- | --- | --- |
| **C1. Camiones en planta** | Pesajes de entrada activos que aún no tienen su repesaje o su salida, por modalidad | `pesaje` con `pesaje_origen IS NULL` y `estado <> 'eliminado'`, sin otra fila `pesaje` cuyo `pesaje_origen` apunte a él (criterio de `modulos/mod_bascula/listarentradasbascula.php`); `pesaje` de salida sin cierre. Agrupar por `id_modalidad` |
| **C2. Ingresos pesados sin depósito** | Ingresos con pesaje cuyo depósito no se creó | `ingreso` activo con `pesaje.id_ingreso` y sin fila en `deposito` (`deposito.id_ingreso`) |
| **C3. Órdenes de cargue abiertas** | Órdenes sin terminar de cargar | `ordencargue` con `fechahora_fin IS NULL` y `estado <> 'eliminado'` (une a `salida` por `id_salida`) |
| **C4. Salidas sin guía y guías sin salida de portería** | Salidas cargadas sin guía de salida, y guías cuya salida no registró portería | `salida` activa sin `guiadesalida.id_salida`; `guiadesalida` sin `salidapuerta.id_salida` |
| **C5. Cobros de báscula pendientes** | Operaciones de báscula por cobrar | Criterio de `modulos/mod_bascula/cobrarcartera.php`: `pesaje` (origen, no eliminado) con `detallefactura` y `factura.total_factura > 0 AND factura.pago = 0` |
| **C6. Períodos de almacenamiento no facturados** | Depósitos vivos con períodos vencidos sin factura | Para los depósitos vivos de la consulta de F6-03, los períodos entre `MAX(facturaciigo.fechafin_periodo)` con `estado = 'facturada'` (o `fecha_deposito`) y T0 |
| **C7. Depósitos vivos con prórroga** | Depósitos que migran con la prórroga registrada | `deposito.prorroga = 1` entre los vivos (BR-08-003; columna 22 del CSV) |
| **C8. Números de depósito repetidos entre vivos** | Depósitos vivos que comparten número en años distintos | `deposito.nro_deposito` repetido entre vivos, con el año de `fecha_deposito` (BR-08-005; columna `anio_deposito` del CSV de levantes) |
| **C9. Depósitos vivos y filas del CSV** | Cuadre entre el legacy y los archivos que se cargan | Depósitos vivos de la consulta de F6-03 contra las filas de cada CSV (depósitos y levantes) |

## 3. Tratamiento por tipo

| Conteos | Tratamiento | Criterio de cierre |
| --- | --- | --- |
| **C1, C2** | Se terminan en el legacy antes de T0, o se rehacen en V2 desde Vigilancia, después de migrar | Llegar a 0 |
| **C3, C4** | Se terminan en el legacy, o se anulan allí y se crea la orden en V2 sobre el depósito migrado. V2 exige la orden de cargue antes de la salida (`DEC-050`) | Llegar a 0 |
| **C5** | Se cobran en el legacy o en SIIGO. Se entrega la lista a Facturación. V2 **no** crea facturas a mano (`DEC-021`) | Lista entregada |
| **C6** | Se facturan o se anulan en el legacy antes de exportar | Llegar a 0 |
| **Levantes registrados después de T0** | Se registran en V2 | — |
| **C7, C8** | Se cotejan con el lote migrado: C7 con los depósitos que quedan con prórroga y plazo de 60 días; C8 con los depósitos creados por número y año | Coinciden con el lote |
| **C9** | Se cotejan con la conciliación (`POST administration/legacy-import/reconciliation`) | Todo `Ok` |

Reglas del tratamiento:

- Lo que se rehace en V2 lleva la **fecha real** de la operación original, no la del día de la migración (`DEC-010` §4: fechas editables).
- Una factura de báscula pendiente (C5) no migra ni se recrea: la cartera sigue en el legacy o en SIIGO hasta que se cobre.
- Un depósito con prórroga (C7) migra con ella: V2 no admite una segunda prórroga.

## 4. Conciliación y cierre

1. **Informe del corte.** Una tabla por tipo (C1 a C9) con: conteo en T−1, conteo en T0, cuántos se cerraron, cuántos se recrearon en V2 y la **diferencia**, que debe ser **0**.
2. **Conciliación de depósitos:** `administration/legacy-import/reconciliation` con el CSV del corte: todo en `Ok` (`summary.differences = 0` y `summary.notMigrated = 0`).
3. **Apertura de la facturación:** `administration/legacy-import/open-billing` con todos los depósitos en `Opened`; los `Skipped` y `Failed` se explican uno por uno.
4. **Orden de carga:** el de `plan-migracion-legacy-staging.md` §3, regla 4, empezando por el paso «0. Congelamiento y conteo».
5. **Después de migrar:** copia de seguridad de V2 («listo para operarios») y recién entonces se abre V2 a la operación.

## 5. Reversa

- Si un conteo no llega a 0 en T0, **se posterga el corte**: se vuelve a abrir el legacy, se termina lo pendiente y se repite el congelamiento.
- Si el usuario decide aceptar una excepción, se documenta en el informe: conteo, números afectados, quién la aceptó y cómo se rehace en V2.
- Mientras el corte no se complete, el legacy sigue siendo el sistema de registro: V2 no se abre a la operación real.

## 6. Plantilla del informe del corte

```text
# Informe del corte — T0 = <fecha y hora de Colombia>

Backend <hash> · Frontend <hash> · Volcado <nombre y hash SHA-256>

| Conteo | T−1 | T0 | Cerrados en el legacy | Recreados en V2 | Diferencia |
| --- | ---: | ---: | ---: | ---: | ---: |
| C1 Camiones en planta | | | | | 0 |
| C2 Ingresos pesados sin depósito | | | | | 0 |
| C3 Órdenes de cargue abiertas | | | | | 0 |
| C4 Salidas sin guía / guías sin salida | | | | | 0 |
| C5 Cobros de báscula pendientes | | | n/a | n/a | lista entregada |
| C6 Períodos no facturados | | | | | 0 |
| C7 Depósitos con prórroga | | | n/a | n/a | cotejado |
| C8 Números repetidos entre vivos | | | n/a | n/a | cotejado |
| C9 Depósitos vivos / filas del CSV | | | n/a | n/a | cuadra |

Conciliación: ok = <n>, differences = <n>, notMigrated = <n>
Apertura de facturación: Opened = <n>, Skipped = <n>, Failed = <n>
Excepciones aceptadas: <ninguna | lista con número, motivo y responsable>
Veredicto: CORTE COMPLETO / POSTERGADO
```

> Sin nombres, documentos, teléfonos ni direcciones de personas naturales (`DEC-007`).
