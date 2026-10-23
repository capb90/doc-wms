# Inventario de P1 pendientes de Báscula, Comercio Exterior y Facturación — F11-S5 (Parte B)

> Generado el 2026-10-06 (hora Colombia) · Build FE `bd729e5` / BE `00d6ac3` · Ejecutor: Claude (agente QA, Opus 5.5).
> Fuente de los casos: `docs/qa/fase-03-bascula.md`, `fase-05-comercio-exterior.md` y `fase-06-facturacion.md` (columna P = P1).
> Cruce: el mismo método de S4 (§4.3 DIR, conteo por ID en los informes, las evidencias de S0 a S4, el registro de datos, las filas F11 de las fichas y los casos de origen de la suite REG). Los 94 P1 ya ejecutados en S0–S4 no se repiten.

## Conteo

| Módulo | P1 en la fase | Ejecutados por ID en S0–S4 | Pendientes (este inventario) |
|---|---|---|---|
| Báscula | 72 | 25 | 47 |
| Comercio Exterior | 47 | 11 | 36 |
| Facturación | 50 | 16 | 34 |
| **Total** | **169** | **52** | **117** |

**Diferencia con la cuenta esperada (unos 170):** la cifra de 170 del informe final (§7, condición 4) es el total de P1 de los tres módulos (72 + 47 + 50 = 169). Los pendientes son 117 porque 52 de esos P1 ya se habían ejecutado por ID en S0–S4 (F3: 25, F5: 11, F6: 16). La diferencia supera el 10 % solo por esa razón; el resto de los 94 P1 ya ejecutados (42) son de otros módulos.

## Resultado de la ejecución en S5

| Estado | Báscula | Comercio Exterior | Facturación | Total |
|---|---|---|---|---|
| PASA | 43 | 34 | 33 | 110 |
| FALLA | 2 | 0 | 0 | 2 |
| No aplica | 0 | 2 | 1 | 3 |
| Diferido a staging | 2 | 0 | 0 | 2 |
| **Total** | 47 | 36 | 34 | **117** |

«No aplica»: el caso se ejecutó por ID, pero su precondición ya no puede darse en el sistema. Las razones están en la nota de cada caso. «Diferido a staging»: los dos cronometrajes del operario, que van con PRF-002 (§8 del informe final).

## Báscula

| ID | Título | Estado | Evidencia |
|---|---|---|---|
| F3-COL-002 | Filtro por estado | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-COL-003 | Refresco | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CAM-001 | Precarga del vehículo | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CAM-002 | Vehículo sin datos | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CAM-004 | Conductor existente | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CAM-005 | Conductor nuevo | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CAM-007 | Precarga asíncrona | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CAM-008 | Memoria del turno | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REG-006 | Documento obligatorio | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REG-010 | Producto repetido | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REG-011 | Línea libre | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REG-017 | Fecha de ingreso del depósito (WMS-33) | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REG-018 | Primer pesaje Tara | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REG-024 | Tiempo del registro | Diferido a staging | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-COB-006 | Consumidor final | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-COB-014 | Error de cobro recuperable | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-PES-005 | Tipo de peso permitido | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-PES-006 | Peso inválido | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-PES-009 | Fecha del pesaje | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-PES-015 | Tiempo hasta primer peso | Diferido a staging | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-TIQ-004 | Fecha y hora | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-TIQ-005 | Reimprimir | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-TIQ-007 | Finalizar | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REI-002 | Aviso al salir con borradores | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REC-001 | Badge y lista | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REC-003 | Retomar con primer peso | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-REC-005 | Descartar con ciclo | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-MCA-003 | Datos de CE en solo lectura | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-MCA-004 | Producto nuevo en el segundo camión | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-MCA-006 | Ambigüedad | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UCA-002 | Sin unidades | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UCA-003 | Placa repetida | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UCA-004 | Placa ya en el depósito | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UCA-005 | Modo distinto en el segundo camión | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UCA-008 | Tanquero y contenedor de bodega | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-SAL-002 | Buscar por placa | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-SAL-004 | Orden externa | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-SAL-007 | Repesaje antes del cargue | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-SBA-002 | Cliente obligatorio | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-SBA-003 | Dos pesajes | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-HIS-003 | Totales | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-HIS-004 | Exportar Excel | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-CIC-001 | Detalle del ciclo | FALLA → [DEF-F11-019](defectos/DEF-F11-019.md) | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-RPT-001 | Reporte diario | FALLA → [DEF-F11-018](defectos/DEF-F11-018.md) | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-INT-001 | Vigilancia → báscula | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UX-001 | Enter por paso | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |
| F3-UX-005 | Mensajes de error del backend | PASA | `S5-B-F3-api.txt` / `S5-B-F3-pantalla.txt` |

## Comercio Exterior

| ID | Título | Estado | Evidencia |
|---|---|---|---|
| F5-TAB-001 | Tarjetas | PASA | `S5-B-F5-api.txt` |
| F5-LIS-002 | Filtros de importación | PASA | `S5-B-F5-api.txt` |
| F5-CNF-005 | Asignar cliente sin rol | PASA | `S5-B-F5-api.txt` |
| F5-CNF-006 | Propagación del cliente | No aplica | `S5-B-F5-api.txt` |
| F5-CNF-012 | Confirmar con unidades de carga | PASA | `S5-B-F5-api.txt` |
| F5-PRD-003 | Eliminar producto con dependencias | PASA | `S5-B-F5-api.txt` |
| F5-PRD-005 | Editar en Confirmed | PASA | `S5-B-F5-api.txt` |
| F5-COR-001 | Devolver para corrección | PASA | `S5-B-F5-api.txt` |
| F5-COR-006 | Guía con depósito en Borrador | No aplica | `S5-B-F5-api.txt` |
| F5-ANU-002 | Motivo obligatorio | PASA | `S5-B-F5-api.txt` |
| F5-ANU-003 | Anular Confirmed con OC Pending | PASA | `S5-B-F5-api.txt` |
| F5-ANU-005 | Con salida ejecutada | PASA | `S5-B-F5-api.txt` |
| F5-AJU-002 | Observación obligatoria | PASA | `S5-B-F5-api.txt` |
| F5-FEC-001 | Corregir fecha de ingreso | PASA | `S5-B-F5-api.txt` |
| F5-ETI-003 | EXP e INSP | PASA | `S5-B-F5-api.txt` |
| F5-IMP-001 | Manifiesto DIAN | PASA | `S5-B-F5-api.txt` |
| F5-LEV-004 | Número duplicado en otro depósito | PASA | `S5-B-F5-api.txt` |
| F5-LEV-007 | Editar levante | PASA | `S5-B-F5-api.txt` |
| F5-LEV-008 | Reducir por debajo de lo usado | PASA | `S5-B-F5-api.txt` |
| F5-LEV-009 | Retirar levante | PASA | `S5-B-F5-api.txt` |
| F5-LEV-010 | Retirar con uso | PASA | `S5-B-F5-api.txt` |
| F5-OC-002 | Selector de depósitos | PASA | `S5-B-F5-api.txt` |
| F5-OC-003 | Depósito en Borrador (API) | PASA | `S5-B-F5-api.txt` |
| F5-OC-008 | Orden externa | PASA | `S5-B-F5-api.txt` |
| F5-OC-013 | Multi-depósito | PASA | `S5-B-F5-api.txt` |
| F5-OC-014 | Multi-cliente (CE-12) | PASA | `S5-B-F5-api.txt` |
| F5-OC-015 | Modificar ítems | PASA | `S5-B-F5-api.txt` |
| F5-OC-018 | Revertir con guía vigente | PASA | `S5-B-F5-api.txt` |
| F5-GUI-004 | Saldos tras cambios posteriores | PASA | `S5-B-F5-api.txt` |
| F5-GUI-005 | Segunda guía de la misma OC | PASA | `S5-B-F5-api.txt` |
| F5-GUI-016 | Consecutivo | PASA | `S5-B-F5-api.txt` |
| F5-ABA-001 | Listado | PASA | `S5-B-F5-api.txt` |
| F5-ABA-002 | Cálculo del plazo | PASA | `S5-B-F5-api.txt` |
| F5-ABA-003 | Registrar prórroga | PASA | `S5-B-F5-api.txt` |
| F5-INT-002 | Camión tardío | PASA | `S5-B-F5-api.txt` |
| F5-INT-003 | Diferencia de recepción | PASA | `S5-B-F5-api.txt` |

## Facturación

| ID | Título | Estado | Evidencia |
|---|---|---|---|
| F6-DSH-001 | KPIs | PASA | `S5-B-F6-api.txt` |
| F6-DSH-002 | Coherencia | PASA | `S5-B-F6-api.txt` |
| F6-INV-003 | Filtros | PASA | `S5-B-F6-api.txt` |
| F6-INV-006 | PDF de la factura | PASA | `S5-B-F6-api.txt` |
| F6-ACC-010 | Enviar | PASA | `S5-B-F6-api.txt` |
| F6-ACC-012 | Motivo corto | PASA | `S5-B-F6-api.txt` |
| F6-ACC-015 | Anular almacenamiento | PASA | `S5-B-F6-api.txt` |
| F6-OVR-001 | Override disponible solo en Draft | PASA | `S5-B-F6-api.txt` |
| F6-OVR-007 | Override descartado por recálculo | PASA | `S5-B-F6-api.txt` |
| F6-TAR-005 | Convenio inactivo | PASA | `S5-B-F6-api.txt` |
| F6-TAR-006 | Escalera: producto + modalidad | PASA | `S5-B-F6-api.txt` |
| F6-FOR-002 | `FIXED` IVA incluido | PASA | `S5-B-F6-api.txt` |
| F6-FOR-006 | `PERCENTAGE_OF_VALUE_PRORATED` | PASA | `S5-B-F6-api.txt` |
| F6-FOR-007 | `PER_VEHICLE` | PASA | `S5-B-F6-api.txt` |
| F6-FOR-008 | `PER_CARGO_UNIT` | PASA | `S5-B-F6-api.txt` |
| F6-FOR-011 | `PER_VEHICLE_TYPE` en montacargas | PASA | `S5-B-F6-api.txt` |
| F6-ALM-003 | Sin configuración del cliente | PASA | `S5-B-F6-api.txt` |
| F6-ALM-004 | Ciclo quincenal y semanal | PASA | `S5-B-F6-api.txt` |
| F6-ALM-007 | Consolidated | PASA | `S5-B-F6-api.txt` |
| F6-ALM-011 | Sin stock no factura | PASA | `S5-B-F6-api.txt` |
| F6-ALM-013 | Reapertura por reversa | PASA | `S5-B-F6-api.txt` |
| F6-ALM-014 | Servicio complementario sin tarifa | No aplica | `S5-B-F6-api.txt` |
| F6-ALM-015 | Renovación automática por job | PASA | `S5-B-F6-api.txt` |
| F6-TRM-007 | Factura aprobada | PASA | `S5-B-F6-api.txt` |
| F6-REC-003 | Factura Draft | PASA | `S5-B-F6-api.txt` |
| F6-REC-005 | Factura con pagos | PASA | `S5-B-F6-api.txt` |
| F6-REC-006 | Factura anulada | PASA | `S5-B-F6-api.txt` |
| F6-REC-007 | Otros disparadores | PASA | `S5-B-F6-api.txt` |
| F6-REF-001 | Refacturar anulada | PASA | `S5-B-F6-api.txt` |
| F6-PAG-004 | Monto 0 | PASA | `S5-B-F6-api.txt` |
| F6-PAG-005 | Factura pagada o anulada | PASA | `S5-B-F6-api.txt` |
| F6-CFG-005 | Validaciones | PASA | `S5-B-F6-api.txt` |
| F6-CAR-004 | OverdueWarning | PASA | `S5-B-F6-api.txt` |
| F6-JOB-001 | Arranque de jobs | PASA | `S5-B-F6-api.txt` |

El detalle de cada caso (datos, mensajes y cifras) está en `F11-informe-S5-2026-10-06.md` §4 y en las evidencias `evidencias/F11/S5-B-*`.
