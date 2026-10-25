# Fase 8 — Flujos E2E entre módulos

> Lee antes `00-plan-maestro.md`. Usa **datos nuevos** (prefijo `QAE`) para que cada flujo empiece limpio: placas `QAE001…`, cartas porte `QAE-CP-001…`.
> Cada flujo se ejecuta con el rol real de cada paso (cambiando de sesión), no con Admin.

## 1. Objetivo

Recorrer los procesos reales del negocio de principio a fin, cambiando de rol en cada paso, y verificar en cada punto de control que los datos que deja un módulo son los que recibe el siguiente: stock, pesos, estados, consecutivos, facturas y notificaciones.

## 2. Criterios de entrada

1. Fases 1 a 7 aprobadas, sin BLOCKER ni CRITICAL abiertos en los pasos de los flujos (o aceptados por el usuario, anotando qué flujo afecta).
2. Dataset maestro intacto (terceros, convenios, tarifas).
3. Ambiente local para los flujos con palancas de tiempo (E2E-12, E2E-13).

## 3. Cómo registrar un flujo

Para cada flujo, el informe incluye una tabla de puntos de control:

| Paso | Rol | Acción | Dato verificado | Esperado | Observado | Estado |
|---|---|---|---|---|---|---|

Un flujo `PASA` solo si todos sus puntos de control pasan. Si un paso falla, el flujo se marca `FALLA` en ese paso y se continúa solo si el fallo no invalida lo que sigue.

## 4. Flujos

### E2E-01 · Importación completa, un camión, salida total (P0)

| # | Rol | Acción | Punto de control |
|---|---|---|---|
| 1 | Vigilancia | Ingreso `QAE001`, Descargue importación. | En la cola de báscula «Sin iniciar». |
| 2 | Báscula | Ingreso con depósito IMP `QAE-CP-001`, `QA Cebolla` 100 bultos, manifiesto; cobro inmediato a `QA Cliente Uno`; bruto 35.000. | Depósito `2026BA…` Draft; stock 100 (`DeclaredEntry`); factura BASCULA Paid; tiquete `2026T…`; CE recibe aviso de depósito nuevo. |
| 3 | Báscula | Tara 15.000. | Neto 20.000; ciclo Complete; tiquete impreso. |
| 4 | Bodega | Recepción contando 100, ubicación, firma. | Recepción Completed; stock sigue 100; sin aviso de diferencia. |
| 5 | CE | Completar datos (cliente, fecha, importador, agencia, USD 30.000, manifiesto) y confirmar; cerrar ingreso de camiones. | Confirmed; período y factura de almacenamiento Draft; TRM DIAN o pendiente; etiqueta SIN NACIONALIZAR. |
| 6 | Facturación | Revisar la factura de almacenamiento; registrar TRM si está pendiente; asignar N.º SIIGO; aprobar. | Importe = fórmula del convenio (hoja de cálculo); Approved. |
| 7 | CE | Levante 100; reimprimir etiqueta. | Nacionalizado; etiqueta NACIONALIZADA. |
| 8 | Vigilancia | Salida de `QAE001`. Ingreso `QAE002` con Cargue importación. | `QAE001` fuera de planta; `QAE002` en cola. |
| 9 | CE | OC por 100 para `QAE002`. | OC `2026OC…` Pending; reservado 100; disponible 0. |
| 10 | Báscula | Salida de mercancía con la OC; cobro; tara 14.000. | Ciclo de salida; factura BASCULA. |
| 11 | CE | Guía de salida antes del cargue (DEC-056: el conductor la pide en CE); cobro inmediato. | Guía `2026S…`; saldos: entrada 100, anterior 100, despachado 100, nuevo 0; factura GUIA_SALIDA. |
| 12 | Bodega | Ejecutar cargue 100: el diálogo muestra «Guía de salida 2026S… vigente». | OC Loaded; stock 0; reserva liberada; depósito **Closed**; períodos cerrados; sin aviso «Guía de salida requerida». |
| 13 | Báscula | Repesaje bruto 34.000. | Neto 20.000; OC Dispatched; servicio Completed. |
| 14 | Vigilancia | Salida `QAE002`. | Fuera de planta. |
| 15 | Admin | Trazabilidad, movimientos por depósito, facturación por CPI. | Etapas finales; kardex IN 100 / OUT 100; facturas del depósito listadas. |

### E2E-02 · Importación con dos camiones y salida parcial (P0)

| # | Rol | Acción | Punto de control |
|---|---|---|---|
| 1 | Vigilancia + Báscula | Camiones `QAE003` (60) y `QAE004` (40) con `QAE-CP-002`. | Un depósito; dos entradas; stock 100; «Camiones ingresados: 2». |
| 2 | Bodega | Recepción de `QAE003` contando 58. | Aviso de diferencia a CE; stock 100. |
| 3 | CE | CE-7 a 98; confirmar; cerrar ingreso. | Cantidad 98; correo de ajuste; factura con 98. |
| 4 | CE | Levante 50; OC 50; guía (DEC-056); Bodega carga 50. | Saldos de la guía: entrada 98, anterior 98, despachado 50, nuevo 48. Etiqueta reimpresa con 48. |
| 5 | CE | Levante 48; segunda OC 48; segunda guía; cargue. | Saldos: anterior 48, despachado 48, nuevo 0. La primera guía no cambió. Depósito Closed. |

### E2E-03 · Camión tardío en depósito confirmado (P0)

| # | Rol | Acción | Punto de control |
|---|---|---|---|
| 1 | — | Depósito `QAE-CP-003` confirmado con 1 camión (100), factura aprobada con N.º. | Estado inicial. |
| 2 | Vigilancia + Báscula | Segundo camión `QAE006` con 20 al mismo documento. | Se asocia; stock 120. |
| 3 | CE / Facturación | Revisar avisos y la factura. | CE: reimprimir etiqueta (y manifiesto si falta); factura aprobada recalculada conservando N.º; notificación con total anterior y nuevo. |
| 4 | CE | Cerrar ingreso; intentar tercer camión. | 409 con quién y cuándo cerró. |

### E2E-04 · Exportación con descargue (P0)

Vigilancia (Descargue exportación) → Báscula (EXP, exportador, 2 pesajes) → Bodega (recepción) → CE (confirmar con exportador) → etiqueta «PARA EXPORTACION» → Vigilancia (Cargue exportación) → CE OC → Báscula salida → Bodega carga → **guía de exportación automática sin cargo** → repesaje → depósito Closed → factura de almacenamiento según tarifa EXP (`FIXED`).

### E2E-05 · Exportación sin descargue / unidad de carga (P1)

Camión con contenedor (unidades de carga) → Báscula registra la unidad → Bodega recibe la unidad completa sin contar (R-BOD-02) → CE confirma con la mercancía por unidad → OC por la unidad → cargue de la unidad completa → guía automática. Verificar fórmula `PER_CARGO_UNIT` si está configurada.

### E2E-06 · Inspección (P1)

Vigilancia → Báscula INSP (un solo pesaje bruto forzado) → Bodega → CE confirma (sin importador ni agencia) → etiqueta «INSPECCION ADUANERA» → factura por la tarifa o el mínimo de INSP.

### E2E-07 · Solo báscula (P0)

Vigilancia (Solo báscula) → Báscula: cliente, cobro inmediato, un pesaje → tiquete → Vigilancia salida. Sin depósito ni stock. Repetir con dos pesajes y cobro por facturar → Facturación numera y aprueba la factura → registra el pago.

### E2E-08 · Solo bodega — recepción sin báscula (P1)

Vigilancia (Solo bodega) → no aparece en báscula → Bodega recepción directa (crea depósito, stock declarado, período) → CE confirma → factura de almacenamiento. (Depende de R-BOD-01.) Verificar que no queden dos ingresos abiertos (R-BOD-04).

### E2E-09 · Montacargas en descargue (P1)

En E2E-01 paso 4: Bodega inicia montacargas (Tractomula, horómetro 100) antes de que CE asigne cliente; finaliza (102) con «Agregar IVA» → factura MONTACARGAS con IVA; si el cliente se asigna después, verificar el destinatario.

### E2E-10 · Orden multi-depósito y multi-cliente (P1)

Dos depósitos IMP confirmados y nacionalizados de `QA Cliente Uno` y `QA Multirol` → una OC con ambos → báscula salida → guía (anotar el firmante y el destinatario, R-CE-08) → cargue parcial en uno: aviso «Guía con cantidades distintas a lo cargado» (DEC-052) → anular y emitir la guía de nuevo → ZIP por depósito → saldos por línea correctos en cada depósito.

### E2E-11 · Correcciones y reversas encadenadas (P0)

| # | Acción | Punto de control |
|---|---|---|
| 1 | Báscula registra un ingreso y lo descarta en Recuperar. | Depósito Cancelled; el camión se puede volver a registrar (R-BAS-02). |
| 2 | Báscula completa una operación y la anula (Anular pesaje). | Ciclo Canceled; efecto en depósito/stock/factura documentado. |
| 3 | CE devuelve un depósito confirmado a Borrador, corrige un producto o el valor de la mercancía, reconfirma. | Sin factura duplicada; importe recalculado con lo corregido (DEF-F11-030). |
| 4 | CE crea OC, CE emite guía, Bodega carga, CE anula la guía, CE revierte la salida. | Guía ANULADA (número no reutilizado); factura de la guía anulada o marcada para revisión; stock devuelto; depósito reabierto; período reabierto. |
| 5 | Facturación anula la factura de almacenamiento y refactura. | Nueva factura Draft enlazada; períodos re-enlazados. |
| 6 | CE anula el depósito. | Stock fuera; períodos cerrados; facturas según política; avisos a Bodega y Facturación. |

### E2E-12 · Cliente en mora bloquea la operación (P0, local)

Factura vencida de `QA Cliente Mora` (palanca de tiempo) → job → `Blocked` → intentar: cobro de báscula, cierre de montacargas, recepción sin báscula, OC, guía (los cinco bloqueados) → Facturación registra el pago → job → `Active` → las cinco operaciones vuelven a permitirse.

### E2E-13 · Renovación de almacenamiento y cierre por agotamiento (P1, local)

Depósito confirmado con stock 100 → renovación (cierre manual o job) → segunda factura sobre el saldo → despacho total a mitad del segundo período → período cerrado conservando lo cobrado → depósito Closed → ninguna renovación posterior.

### E2E-14 · TRM pendiente a factura aprobada (P1, local)

Depósito USD confirmado sin acceso a la DIAN → factura al mínimo con «TRM PENDIENTE» → Facturación no puede numerar ni aprobar → registra TRM manual → factura recalculada con la tarifa real → numera y aprueba → la DIAN, ya disponible, no reemplaza la TRM manual.

### E2E-15 · Fechas operativas (WMS-33) (P1)

Camión que entra un día y se procesa al siguiente (o con fecha corregida hacia atrás): fecha de ingreso del depósito = la de Vigilancia → pesajes con fecha del día anterior → etiqueta, abandono y período con esa fecha → consecutivo del año de esa fecha.

### E2E-16 · Corrección en Vigilancia con operación posterior (P2)

Ingreso con placa errada → báscula registra → Vigilancia intenta corregir el motivo (bloqueado) y corrige la placa (permitido) → el depósito refleja la placa corregida en sus entradas.

### E2E-17 · Salida con el tiquete de ingreso (P2)

Camión entra con mercancía de un depósito ya confirmado y nacionalizado y sale con otra mercancía usando el mismo tiquete (F3-SAL-011 / F5-OC-021) → CE emite la guía (DEC-056) → la OC se despacha al cargar sin segundo pesaje.

### E2E-18 · Concurrencia en báscula (P2)

Dos operarios (`bascula` y `f_chosi`) abren el mismo camión a la vez: ambos intentan guardar o cobrar → solo una operación válida; la otra recibe el error de servicio/ciclo ya existente; ningún dato duplicado.

### E2E-19 · Consecutivos sin saltos en un día de operación (P1)

Tras los flujos anteriores, listar tiquetes, depósitos por modalidad, OC y guías del día: consecutivos de 5 dígitos, sin saltos ni repetidos (incluidas las operaciones descartadas o anuladas: anotar si generan saltos).

### E2E-20 · Cierre del día de facturación (P1)

Al final de los flujos: reporte diario de báscula = suma de facturas BASCULA del día; facturación anual del mes = suma de facturas con número; cartera del dashboard = suma de pendientes; inventario general = suma de stocks.

## 5. Criterios de salida específicos

- Flujos P0 (E2E-01, 02, 03, 04, 07, 11, 12) `PASA` o con defectos informados al usuario.
- ≥ 80 % de los P1 ejecutados.
- Cada flujo con su tabla de puntos de control.

## 6. Entregables

Informe con una sección por flujo, defectos y registro de datos. Detenerse.
