# 04 — Resultado del agente AG-04 (Comercio Exterior: ingresos y depósitos)

> Auditoría estática del 2026-10-23. No se ejecutaron builds, pruebas, APIs ni consultas a bases de datos, ni comandos Git. Código según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b` (código en disco ese día).

## 1. Cobertura

| Concepto | Cantidad |
| --- | ---: |
| Capacidades legacy asignadas (`CF-L122…142`, `CF-L237`, `CF-L259`, `CF-L260`) | 24 |
| Capacidades legacy no catalogadas añadidas (`CF-LX04-01`, alerta de abandono) | 1 |
| Filas de desglose (`CF-L140.a/.b`, `CF-L141.a/.b`) | 4 |
| Candidatas V2 asignadas (`CF-V040…045`, `CF-V084`) | 7 |
| Capacidades V2 nuevas (`CF-V046…048`) | 3 |
| Filas de la matriz | 39 |

Las 25 capacidades legacy y las 10 V2 tienen las cinco dimensiones evaluadas con evidencia de código. Excluidas por decisión (Colmotores): `CF-L237`, `CF-L259` → `NO_APLICA`, sin restos en V2 (búsqueda `vin`, `vines`, `serial`).

## 2. Paridad integral (25 capacidades legacy, filas padre)

| Estado | N.º | Capacidades |
| --- | ---: | --- |
| COMPLETO_CODIGO | 4 | CF-L123, CF-L125, CF-L129, CF-L137 |
| DIFERENCIA_INTENCIONAL | 6 | CF-L126, CF-L127, CF-L128 (DEC-010); CF-L132 (P11); CF-L135 (DEC-010/012/013, P2); CF-L142 (GAP-012) |
| PARCIAL | 12 | CF-L122, CF-L124, CF-L130, CF-L131, CF-L133, CF-L134, CF-L136, CF-L138, CF-L140, CF-L141, CF-L260, CF-LX04-01 |
| NO_IMPLEMENTADO | 1 | CF-L139 |
| NO_APLICA | 2 | CF-L237, CF-L259 |

### Por dimensión (25 legacy)

| Dimensión | Estados |
| --- | --- |
| Frontend | COMPLETO_CODIGO 17 · PARCIAL 1 · NO_IMPLEMENTADO 1 · NO_APLICA 6 |
| Backend | COMPLETO_CODIGO 19 · PARCIAL 2 · NO_IMPLEMENTADO 1 · NO_APLICA 3 |
| Integración | CONECTADO_CODIGO 20 · NO_APLICA 5 |
| Reglas de negocio | COMPLETO_CODIGO 11 · PARCIAL 9 · NO_IMPLEMENTADO 2 · NO_APLICA 3 |

**Validación por ejecución:** 17 de las 25 filas legacy citan casos de QA ejecutados (`docs/qa/resultados/F5-informe-2026-10-02.md`, `F11-informe-S5-2026-10-06.md`); sin ejecución: CF-L123 (cubierta por QA de báscula, módulo 02), CF-L132 (sin caso de asociación de listas), CF-L138, CF-L139, CF-L142, CF-L260 (caso previsto F3-MCA-009) y las dos excluidas.

## 3. Brechas

| Criticidad | N.º | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 0 | — |
| MEDIA | 3 | BR-04-001, BR-04-002, BR-04-012 |
| BAJA | 9 | BR-04-003…011 |

Las más relevantes:

1. **BR-04-001 (MEDIA)** — Un camión tardío a un depósito ya cerrado por agotamiento (sin cierre del ingreso de camiones) crea **otro depósito** en vez de reactivarlo (CF-L260, RN-023, DEC-013).
2. **BR-04-002 (MEDIA)** — La fecha de ingreso solo se corrige dentro de la estadía del primer camión; `DEC-012` dice «sin límite hacia atrás». QA validó el comportamiento del código.
3. **BR-04-012 (MEDIA)** — No existe la etiqueta por vehículo (`adhesivovehiculo.php`), útil en depósitos de varios camiones.
4. **BR-04-011 (BAJA)** — El filtro «Manifiesto» busca el del camión, no el DIAN; EXP/INSP sin filtro por placa (ya en backlog de QA).
5. **BR-04-007/008 (BAJA)** — La validación del depósito contra la plantilla no tiene botón en la UI y la interfaz TS del detalle declara 9 campos inexistentes.

No se duplicó el pendiente FOB/CIF del valor de la mercancía (`estado.md` §4 n.º 8): se cita en CF-L124.

## 4. SOLO_V2

| ID | Resultado |
| --- | --- |
| CF-V040 Unidades de carga en el depósito | Confirmada (DEC-014, P5). |
| CF-V041 Inspecciones INSP | Confirmada (el legacy solo tenía el prefijo `OT`). |
| CF-V042 Cierre explícito del ingreso de camiones | Confirmada (DEC-013). |
| CF-V043 Fecha de ingreso editable | Confirmada; límite inferior en BR-04-002. |
| CF-V044 Ajuste CE-7 con kárdex | Confirmada (DEC-019). |
| CF-V045 Exportaciones EXP | **Reasignada** a CF-L134/CF-L135 (el legacy tenía depósitos de exportación). |
| CF-V084 Alerta diaria de abandono (job) | Confirmada; diferencias en BR-04-010. |
| CF-V046 Confirmación con requisitos y devolución a corrección | Nueva, confirmada (P2, P5). |
| CF-V047 Validación contra plantilla | Nueva; backend completo, UI sin disparador (`SOLO_MAQUETADO` / `SIN_INTEGRACION`, BR-04-007). |
| CF-V048 Manifiesto por camión y cambio de producto de la línea | Nueva, confirmada (F1-04, F1-07). |

## 5. Contraste con el análisis anterior

### 5.1 Estados de `bodegas-legacy/docs/legacy_analysis/MIGRATION_MATRIX.md` (24 filas)

| Clasificación | N.º | Detalle |
| --- | ---: | --- |
| CONFIRMADA_EN_CODIGO | 12 | L123, L126, L127, L128, L135, L136, L137 (anulación lógica), L138 (sin seriales), L139 (no existe), L142 (no construir), L237, L259 |
| OBSOLETA | 8 | L122 (las columnas de saldo y los filtros ya existen; el saldo amparado no aplica por DEC-010), L125 (ya libera reservas, cierra períodos y anula facturas: F3-08), L129–L132 (listas de empaque construidas: F4-05/06), L140 (prórroga y abandono construidos: F2-08/09), L141 (ya registra impresiones: F4-09) |
| INCOMPLETA | 4 | L124 («solo en Borrador»: hoy también manifiesto por camión, fecha de ingreso y planilla en Confirmado), L133 y L134 («CUBIERTA»: filtros de manifiesto y placa, BR-04-011), L260 («Confirmado hasta stock 0»: omite el cierre automático y el camión tardío, BR-04-001) |
| CONTRADICHA_POR_CODIGO | 0 | — |

### 5.2 Afirmaciones de planes y decisiones

| Afirmación | Clasificación | Evidencia |
| --- | --- | --- |
| Plan backend F1-04 (fecha del documento y manifiesto por camión) | CONFIRMADA_EN_CODIGO | `ForeignTradeController.cs:440-459`; `DepositCompletionController.cs:36` |
| F1-05 (requisitos al confirmar, P2/P5) | CONFIRMADA_EN_CODIGO | `DepositConfirmationRequirements.cs:64-124` |
| F1-06 (producto libre en báscula) | NO_VERIFICADA | Módulo 02 |
| F1-07 (cambio de producto de la línea) | CONFIRMADA_EN_CODIGO | `DepositCompletionController.cs:78` |
| F1-08 (unidades sin desglose, reparto) | CONFIRMADA_EN_CODIGO (parte CE) | `DepositCompletionController.cs:104`; la parte de báscula es del módulo 02 |
| F2-08 (prórroga) | CONFIRMADA_EN_CODIGO | `RegisterStorageExtensionCommandHandler.cs` |
| F2-09 (listado, resumen, job) | CONFIRMADA_EN_CODIGO | `AbandonmentCalculator.cs`, `AbandonmentReader.cs`, `AbandonmentAlertService.cs`, `Program.cs:81` |
| F2-10 (reportes de abandono) | NO_VERIFICADA | Módulo 07 (existen controlador y consumidores) |
| F3-08 (anular con efectos) | CONFIRMADA_EN_CODIGO | `WarehouseStorageCancellationService.cs` |
| F4-05 / F4-06 (listas de empaque) | CONFIRMADA_EN_CODIGO | `PackingListsController.cs`; detalles menores en BR-04-006 |
| F4-09 (registro de impresiones) | CONFIRMADA_EN_CODIGO | `ForeignTradeController.cs:287-290`, `LabelPrintsController.cs` |
| Plan frontend F1-07, F1-08, F2-07, F3-06 (DF14), F4-04, F5-02, F5-03, F7-01 | CONFIRMADA_EN_CODIGO | Páginas y componentes de `05-analisis-v2.md` §1 |
| GAP-003, GAP-011, GAP-013 construidos; GAP-012 no construido | CONFIRMADA_EN_CODIGO | Matriz |
| P6 (b) días desde el ingreso, (c) marca de destino | CONFIRMADA_EN_CODIGO | `AbandonmentReader.cs:53`; `City.cs:26` |
| P6 (a) reporte con prórroga desde 60 días | NO_VERIFICADA | Módulo 07 |
| P11 | CONFIRMADA_EN_CODIGO | `ImportPackingListCommandHandler.cs:41-70`; asociación en Borrador |
| DEC-010, DEC-014, DEC-016, DEC-019 (CE-7) | CONFIRMADA_EN_CODIGO | Matriz |
| DEC-012: consecutivos y año por fecha de ingreso | CONFIRMADA_EN_CODIGO | `WeighbridgeService.cs:34-39` |
| DEC-012: corrección «sin límite hacia atrás» | CONTRADICHA_POR_CODIGO | `WarehouseStorage.cs:212-213` (BR-04-002) |
| DEC-013: cierre explícito sin reapertura | CONFIRMADA_EN_CODIGO | `ServiceRecord.cs:330-342` |
| DEC-013: el camión tardío entra al stock del depósito | INCOMPLETA | No si el depósito se cerró por agotamiento (BR-04-001) |
| `00-plan-maestro.md` §10: etiqueta NACIONALIZADA con levante parcial | CONFIRMADA_EN_CODIGO | `LabelGenerationService.cs:85-87` |
| `estado.md` §1: «toda la funcionalidad planeada está implementada» (para este módulo) | INCOMPLETA | Implementado salvo detalles; CF-V047 sin UI |

## 6. Incertidumbres

- **Uso real** de seriales por unidad (CF-L138/L139), volumen y condiciones (CF-L124) y etiqueta por vehículo (CF-L141.a): el código no dice si se usaban fuera de Colmotores; por eso las brechas piden confirmación.
- **Año del consecutivo tras corregir la fecha de ingreso**: el número no se recalcula si la corrección cruza de año (`CorrectEntryDate` no toca `WarehouseStorageNumber`). DEC-012 no cubre el caso; no se registró como brecha.
- **Alerta legacy por exportaciones**: `evaluaabandonos.php` no filtraba modalidad; V2 solo cuenta importación. Se interpreta como anomalía legacy corregida.
- La modalidad de exportación se compara exacta con `EXP001` en listados y detalle (`GetExportDepositsHandler.cs:17`): si se crea otra modalidad EXP no aparecería. No se registró como brecha (no hay otra en el código).

## 7. Lo que quedó sin analizar

- La creación del depósito en báscula y el producto por descripción libre (F1-06, CF-V025): módulo 02.
- Levantes, órdenes de cargue, guías y la salida a destino de abandono: módulo 05. Reportes `abandonment-*`, kárdex y PDF comunes: módulo 07. Recálculo de la factura del período y TRM: módulo 06.
- Los HTML/PDF de `bodegas-legacy/reportes/depositos/` (artefactos con datos) y `bodegas-legacy/leerexcel/` (librería de ejemplo sin uso en el módulo).
- No se ejecutaron las pruebas unitarias citadas (`Wms.Tests/ForeignTrade/*`).
