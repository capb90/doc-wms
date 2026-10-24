# 02-bascula — Resultado del agente AG-02

> 2026-10-23 · Auditoría estática (sin Git, sin builds, sin pruebas, sin llamadas a APIs ni a bases de datos). Código en disco; según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`.

## 1. Cobertura

- **Asignadas:** 22 capacidades legacy (CF-L102…121, CF-L235, CF-L255) y 6 candidatas V2 (CF-V020…025).
- **Auditadas:** las 22 + 1 no catalogada (**CF-LX02-01**, atajos Alt+N/Alt+K de `bodegas-legacy/entrada.php`), con 10 desgloses por operación (CF-L103.a/b/c, CF-L116.a…e, CF-L121.a/b); 6 candidatas V2 + 4 nuevas (**CF-V026…029**). Total: 43 filas en la matriz.
- **Archivos leídos:** los 42 scripts de `bodegas-legacy/modulos/mod_bascula/` (los formularios largos por sus bloques PHP, JS y HTML relevantes), `peso.php`, `consultapesa.php`, `entrada.php`, `menus/menuizquierda.php`, `verificapermisos.php`; los 7 controladores de báscula (51 acciones), los handlers y servicios de `Wms.Application/Weighbridge/` que implementan cada regla, `WmsPolicyRoles.cs`, `PaymentContractsTests.cs`; las 8 páginas de `pages/operations/weighbridge/`, los componentes y composables principales de `features/weighbridge/` y el servicio HTTP completo (51 funciones).

## 2. Conteos

**Paridad integral (23 capacidades legacy principales):** COMPLETO_CODIGO 5 · PARCIAL 13 · DIFERENCIA_INTENCIONAL 5 · NO_IMPLEMENTADO 0 · NO_VERIFICADO 0 · NO_APLICA 0.
Desgloses (10): COMPLETO_CODIGO 3 · PARCIAL 4 · DIFERENCIA_INTENCIONAL 2 · NO_IMPLEMENTADO 1 (CF-L116.d, otros servicios).

**Por dimensión (43 filas):**

| Dimensión | COMPLETO / CONECTADO | PARCIAL | NO_IMPLEMENTADO / SIN_INTEGRACION | NO_APLICA | DIFERENCIA_INTENCIONAL |
| --- | ---: | ---: | ---: | ---: | ---: |
| Frontend | 30 | 8 | 1 | 4 | — |
| Backend | 26 | 12 | 1 | 4 | — |
| Integración | 38 | 1 | 1 | 3 | — |
| Reglas de negocio | 13 | 17 | 1 | 12 | — |

Reglas regla a regla (`03-reglas-negocio.md`, 31 reglas): COMPLETO_CODIGO 15 · PARCIAL 8 · NO_IMPLEMENTADO 2 · NO_APLICA 6 (las diferencias decididas citan su decisión).

## 3. Brechas (18): CRÍTICA 0 · ALTA 1 · MEDIA 5 · BAJA 12

Las más graves:
1. **BR-02-006 (ALTA)** — En un ciclo con 3 o más pesajes, corregir cualquier pesaje que no sea el primero modifica siempre el segundo y recalcula el neto solo del primer depósito (`ModifyWeighingDialog.vue:123-131`, `ModifySecondWeightHandler.cs:62-84`); riesgo R-BAS-09 del plan de QA, caso F3-COR-006 nunca ejecutado.
2. **BR-02-005 (MEDIA)** — El tiquete imprime «Numeración autorizada y/o habilitada por la DIAN» sobre el consecutivo interno `2026T…` (`WeighbridgeTicketPdfService.cs:414`).
3. **BR-02-013 (MEDIA)** — Un camión con varios documentos exige un pesaje intermedio por depósito; el legacy usaba un solo pesaje (`RecordWeighingHandler.cs:133-140` vs `registrarentradavariascp.php:79-133`).
4. **BR-02-001 (MEDIA)** — La salida exige una orden de cargue previa; el legacy registraba la salida y CE la completaba (`InitiateOutputWeighingValidator.cs:13-15` vs `registrarsalida.php:104-105`).
5. **BR-02-002 / BR-02-010 (MEDIA)** — Solo báscula exige cliente registrado; báscula ya no puede corregir el registro guardado (documento, mercancía, cantidad, destinatario, valor).

Ninguna tiene ficha `DEF-*`; varias son diferencias sin decisión que piden confirmación del negocio (categoría REGLAS_NEGOCIO).

## 4. `SOLO_V2`

Confirmadas: CF-V020 (cola), CF-V021 (recuperar), CF-V022 (por repesar / en proceso, absorbidas por la cola), CF-V023 (tablero), CF-V025 en su parte de **flujo perecedero** (cierra sin guía persistida: `GenerateGlobalDispatchGuideHandler.cs:71`), y nuevas CF-V026 (reporte diario de facturación), CF-V027 (documentos de envío), CF-V028 (alta rápida de terceros y transportadoras), CF-V029 (observación del tiquete).
Reasignadas: CF-V024 (corrección de pesajes) es en buena parte el «modificar» legacy (CF-L104/L108/L112); el **depósito adicional** de CF-V025 equivale a «Vehículo con varios Doc.» (CF-L103.c).

## 5. Contraste con el análisis anterior

### 5.1 Estados de `MIGRATION_MATRIX.md` (22 capacidades)

| Clasificación | Cantidad | Capacidades |
| --- | ---: | --- |
| CONFIRMADA_EN_CODIGO | 9 | CF-L102, L104, L106, L108, L110, L112, L117, L118, L255 |
| INCOMPLETA | 7 | CF-L103 (no ve la diferencia de varios documentos), L107 (orden previa), L111 (cliente obligatorio), L114 (repesajes múltiples), L115 (leyenda DIAN, impresiones), L116 (otros servicios, cobro sin tarifa), L235 (cita el lookup como uso; aviso de vehículo repetido) |
| OBSOLETA | 6 | CF-L105, L109, L113 (COMPORTAMIENTO DIFERENTE → la anulación F3-09 existe), L119, L120 (NO ENCONTRADA → F4-07 y F4-08 existen), L121 (su motivo, «sin informe por modalidad», se resolvió con F5-09) |
| CONTRADICHA_POR_CODIGO | 0 | — |
| NO_VERIFICADA | 0 | — |

### 5.2 Afirmaciones de los planes y documentos del módulo (40)

| Afirmación | Clasificación | Evidencia |
| --- | --- | --- |
| Plan backend F1-01 (opcionales en báscula) | CONFIRMADA_EN_CODIGO | `InitiateStorageWeighingValidator.cs:56-131` |
| F1-02 / P1 (documento sin fecha, 409 ambiguo) | CONFIRMADA_EN_CODIGO | `StorageDocumentLookup.cs:59-60`; `InitiateStorageWeighingHandler.cs:272` |
| F1-03 (exportador en báscula) | CONFIRMADA_EN_CODIGO | validador `:78-86`; `RegisterStorageEntryRequest` `ExporterId` |
| F1-04 (CE completa fecha y manifiesto) | NO_VERIFICADA | Pertenece al módulo 04 |
| F1-05 / P2 (requisitos de confirmación) | CONFIRMADA_EN_CODIGO | `DepositConfirmationRequirements.cs:49-59` (detalle en módulo 04) |
| F1-06 / P3 (producto libre) | CONFIRMADA_EN_CODIGO | `WeighbridgeProductResolver.cs:103` |
| F1-07 (CE cambia el producto) | NO_VERIFICADA | Módulo 04 (`ChangeDepositLineProduct/` existe) |
| F1-08 / P5 (unidades sin desglose) | CONFIRMADA_EN_CODIGO | `CargoUnitDeclaration.cs:14-113`; `InitiateStorageWeighingHandler.cs:1360` |
| F1-09 / P4 / BAS-05 (efectivo y cambio) | OBSOLETA | Retirado por §10 (2026-10-02); `PaymentContractsTests.cs` |
| Contrato C-F1-12 | OBSOLETA | Ídem |
| Contrato C-F1-01, C-F1-02, C-F1-03 | CONFIRMADA_EN_CODIGO | DTO y TS coinciden (`05-analisis-v2.md` §3) |
| F3-09 / C-F3-10 / C-F3-11 (anular pesaje) | CONFIRMADA_EN_CODIGO | `VoidWeighingCommandHandler.cs`; `WeighbridgeHistoryDto.cs:34-36` |
| F4-07 / C-F4-18 / P10 (pesaje compartido) | CONFIRMADA_EN_CODIGO | `WeighbridgeOutputSharingController.cs:31`; `AddAdditionalOrdersCommand.cs` |
| F4-08 / C-F4-19 / P10 / P16 (salida con tiquete, sin lote) | CONFIRMADA_EN_CODIGO | `ExitWithEntryTicketCommand.cs:9`; `LoadingOrderExitController.cs` |
| F5-09 / C-F5-11 (filtros, pesos, totales, no impresos) | CONFIRMADA_EN_CODIGO | `GetWeighbridgeHistoryQuery.cs`; `WeighbridgeController.cs:723`; columnas `cashReceived`/`changeGiven`: OBSOLETA (§10) |
| P16 (no se construye la salida en lote) | CONFIRMADA_EN_CODIGO | Sin código de selección múltiple |
| GAP-018 / §A.3 (lookup sin uso) | CONFIRMADA_EN_CODIGO | `useWeighbridgeLookup.ts` sin consumidores |
| Captura automática retirada | CONFIRMADA_EN_CODIGO | Sin restos (búsqueda en `03-reglas-negocio.md` R-30) |
| Plan frontend F1-01 (sin «Validar documento», panel plegado) | CONFIRMADA_EN_CODIGO | `StorageServiceForm.vue:8-9,518,1102` |
| F1-02 / DF16 (líneas en línea, unidad en línea libre) | CONFIRMADA_EN_CODIGO | `TruckGoodsLines.vue:63` |
| F1-03 / DF15 (tipo de carga visible; interruptor del operario) | INCOMPLETA | Selector visible (`:1057`); el interruptor «Detallar mercancía por unidad» no es del operario: lo decide el backend (`:247`, `CargoUnitsEditor.vue:43-46`) |
| F1-04 (efectivo en el cobro) | OBSOLETA | §10 |
| F1-05 / DF5 / DF9 (pasos en línea, destinatario) | CONFIRMADA_EN_CODIGO | `index.vue:1024-1146` |
| F1-06 / DF6 / DF8 (teclado, sin modal de confirmación, motivo) | CONFIRMADA_EN_CODIGO | `index.vue:528,1374-1403`; `StorageServiceForm.vue:8-9` |
| DF7, DF10, DF11 | CONFIRMADA_EN_CODIGO | `StorageServiceForm.vue:518,823-824,1102` |
| F1-09 / DF2 (cronometraje) | NO_VERIFICADA | PRF-002 pendiente (`estado.md` §4) |
| F3-01 frontend (anular, rol Admin/Scale, ocultar acciones) | CONFIRMADA_EN_CODIGO | `history.vue:146-154`; `cycles/[id].vue:100` |
| F4-05, F4-06 frontend | CONFIRMADA_EN_CODIGO | `AdditionalOrdersDialog.vue`; `EntryTicketExitPanel.vue`; `ExitWithEntryTicketDialog.vue` |
| F5-09 frontend (filtros, totales, Excel) | CONFIRMADA_EN_CODIGO | `history.vue:84-117`; «# Impr.» como Sí/No |
| §A.5 ganancias de V2 (cola, memoria, borradores, camiones previos, neto en servidor, mora, recuperar, atajos, alta rápida, fecha editable, depósito adicional, por facturar) | CONFIRMADA_EN_CODIGO | `05-analisis-v2.md`; salvo «efectivo y cambio solo con pago inmediato»: OBSOLETA |
| `BASCULA_PARITY.md` §3.2 («siete campos obligatorios se movieron a báscula») | OBSOLETA | Hoy son opcionales (F1-01) |
| `BASCULA_PARITY.md` BAS-01…04, BAS-06, BAS-07 | CONFIRMADA_EN_CODIGO | Ver filas anteriores |
| `BASCULA_PARITY.md` BAS-08 / BAS-09 | CONFIRMADA_EN_CODIGO | Con la lectura de P10 |
| `BASCULA_PARITY.md` §6 (rol de Vigilancia a báscula, sin desarrollo) | NO_VERIFICADA | Es configuración de usuarios, no código |
| DEC-010 (≤ 30 s) | NO_VERIFICADA | PRF-002 |
| DEC-012 (consecutivo `2026T00001`, año de la fecha de ingreso) | CONFIRMADA_EN_CODIGO | `WeighbridgeService.cs:105-106`; `RecordWeighingHandler.cs:92` |
| DEC-016 (WMS-10, un peso de manifiesto) | CONFIRMADA_EN_CODIGO | `InitiateStorageWeighingHandler.cs:415-417` (pesos por producto en null) |
| DEC-017 (conductor por documento) | CONFIRMADA_EN_CODIGO | `RegisterStorageEntryRequest` sin `DriverId`; `EntryDriverRules.cs` |
| DEC-019 (D-1, D-2, repesar 409) | CONFIRMADA_EN_CODIGO | `ExitLoadingRules.cs:25-38`; sin «Cambiar modo de pago» en báscula |
| `estado.md` §1 («toda la funcionalidad planeada está implementada») para báscula | INCOMPLETA | Implementado salvo lo que §10 retiró; quedan diferencias sin decisión (§3) |

Totales: CONFIRMADA_EN_CODIGO 29 · INCOMPLETA 2 · OBSOLETA 4 · NO_VERIFICADA 5 · CONTRADICHA_POR_CODIGO 0.

## 6. Incertidumbres

- Uso real en producción de las variantes legacy (`registrarentrada.php`, «Vehículo con varios Doc.», repesajes múltiples, otros servicios): el catálogo es del checkout y `db_legacy/` no se abrió.
- La validación QA de F3 corrió sobre FE `a5289ce` / BE `191d4b1` (2026-10-02); el código actual tiene correcciones posteriores (fase 11, selector de conductor del 2026-10-08).
- `ModifyFirstWeightHandler` también calcula el neto con los dos primeros pesajes; el efecto exacto de BR-02-006 en cada caso multidepósito no se probó (estático).

## 7. Sin analizar y por qué

- Pantallas de Comercio Exterior que completan el depósito (F1-04, F1-07, reparto de unidades): módulo 04.
- Cargue y guía de las salidas (F3-07, CHG-33): módulo 05. Facturación (N.º SIIGO, pagos, anulación manual): módulo 06.
- `reportes/bascula/*.html|pdf`: salidas generadas, posiblemente con datos personales; no se abrieron.
- Medición de tiempos (PRF-002): requiere ejecución con un operario.
