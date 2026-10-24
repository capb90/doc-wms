# 06-facturacion — Resultado del agente AG-06

> 2026-10-23 · Auditoría estática: sin Git, sin builds, sin pruebas, sin APIs ni bases de datos; no se abrieron secretos ni `db_legacy/`. Código según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`.
> **Prefijos:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`.

## 1. Cobertura

| Concepto | Cantidad |
| --- | ---: |
| Capacidades legacy asignadas | 22 (`CF-L017…020`, `065…072`, `201…207`, `234`, `249`, `251`) |
| Capacidades legacy auditadas | 22 + 1 no catalogada (`CF-LX06-01`, alerta de TRM) = 23 |
| Desgloses por operación | 9 (`CF-L202.a…e`, `CF-L234.a…d`) |
| Candidatas `SOLO_V2` asignadas / confirmadas | 8 / 8 (`CF-V060…067`) |
| `SOLO_V2` nuevas | 4 (`CF-V068` tablero, `CF-V069` sobrescritura de línea, `CF-V06A` factura consolidada, `CF-V06B` PDF interno) |
| Filas de la matriz | 44 |
| Archivos legacy leídos | `mod_facturacion` (9 PHP), `mod_convenios` (7), `mod_tarifas` (4), `mod_tasascambio` (5), `cron.php`, `menus/evaluatasacambio.php`, `inicial.php`, `menus/menuizquierda.php`, y los consumidores de tarifas en `mod_bascula` |
| Backend leído | `BillingController` (27 acciones), `BillingCyclesController`, `BillingPreviewController`, `BillingReportsController`, `InvoiceReissueController`, `FormulaTypeController`, `ServiceController`, `ForkliftRateController`, `SystemController`, agreements de `StakeholderController`; `Wms.Application/Billing` (servicios, resolutor, calculadoras, comandos, consultas, jobs); los 4 jobs de facturación |
| Frontend leído | `pages/billing/*` (8 páginas), `pages/admin/services/*`, `pages/admin/forklift-rates`, `pages/admin/stakeholders/[id].vue`, `features/billing`, `features/agreements`, `features/services` |

## 2. Conteos por dimensión

Cada celda da tres cifras: filas legacy (23) · desgloses (9) · `SOLO_V2` (12).

| Dimensión | COMPLETO_CODIGO | PARCIAL | NO_IMPLEMENTADO | NO_APLICA | Otros |
| --- | --- | --- | --- | --- | --- |
| Frontend | 11 · 3 · 9 | 8 · 1 · 0 | 0 · 1 · 0 | 4 · 4 · 3 | — |
| Backend | 16 · 6 · 8 | 6 · 3 · 4 | 0 | 1 · 0 · 0 | — |
| Integración | CONECTADO 20 · 5 · 12 | 0 | — | 2 · 3 · 0 | SIN_INTEGRACION 1 · 1 · 0 |
| Reglas de negocio | 14 · 5 · 7 | 8 · 4 · 5 | 0 | 1 · 0 · 0 | — |
| **Paridad integral** | **0 · 4 · —** | **14 · 4 · —** | 0 | — · — · 12 | DIFERENCIA_INTENCIONAL **9 · 1 · —** |

Ninguna capacidad legacy del módulo tiene paridad `COMPLETO_CODIGO` como fila principal: o es reemplazo documentado (9) o tiene alguna brecha (14). Las brechas son en su mayoría de detalle; el flujo central (períodos con la regla legacy, cálculo por motor, N.º SIIGO, anular y refacturar, TRM) está implementado y conectado.

## 3. Brechas por criticidad

| Criticidad | Cantidad | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 2 | BR-06-001, BR-06-004 |
| MEDIA | 5 | BR-06-002, BR-06-003, BR-06-005, BR-06-006, BR-06-007 |
| BAJA | 7 | BR-06-008 … BR-06-014 |

Las más graves:
1. **BR-06-004 (ALTA):** un servicio complementario sin tarifa hace lanzar la apertura: la confirmación del depósito se revierte y el job reintenta y avisa cada 5 minutos (contra DEC-020).
2. **BR-06-001 (ALTA):** un convenio «Programado» nunca se activa (no hay ejecutor de `ScheduledActivationDate`) y el convenio no tiene vigencia final: la tarifa pactada no se aplica, sin aviso.
3. **BR-06-003 (MEDIA):** «Depósitos pendientes» solo lista depósitos con período abierto; un depósito agotado con factura sin N.º o anulada sin refacturar desaparece de la lista de trabajo (R-FAC-10).
4. **BR-06-005 (MEDIA):** la renovación cobra el stock del día en que corre (fin + 4), no el del inicio del período como el detalle legacy; afecta fórmulas por cantidad.
5. **BR-06-006 (MEDIA):** no hay fecha de factura; los informes anual y por CPI usan la creación del borrador.

Ninguna duplica una ficha `DEF-*`; se citan DEF-F6-002, 005, 006, 008, 013, 018, 021, DEF-F7-007, DEF-F8-006 y DEF-F11-017 como verificadas, y MAF-07, MAF-08 y MAF-14 del análisis del motor.

## 4. `SOLO_V2` confirmadas

`CF-V060` motor de acuerdos (4 niveles, 8 fórmulas + precio base y respaldo), `CF-V061` ciclos configurables (8; `OnDemand` retirado por §10), `CF-V062` pagos y conciliación diaria, `CF-V063` mora y bloqueo, `CF-V064` aviso de vencimiento, `CF-V065` refacturación, `CF-V066` TRM de la DIAN al abrir el período, `CF-V067` cierre y renovación automáticos; nuevas `CF-V068` tablero, `CF-V069` sobrescritura de línea, `CF-V06A` consolidada por cliente, `CF-V06B` PDF interno.

**`BillingPreviewController`:** no es resto de la creación manual retirada por DEC-021. `POST billing/preview` alimenta el total del cobro en línea (`F/features/billing/components/BillingCollectForm.vue:270`) y `POST billing/formula-preview` la vista previa de convenios (`F/features/agreements/services/formula-type-service.ts:24-30`). Lo retirado (`create.vue`, `BillingPreviewPanel.vue`, `GetStorageInvoiceDraft`, `POST billing/invoices`) no existe y `B/Wms.Tests/Api/BillingControllerSurfaceTests.cs` lo vigila.

## 5. Contraste con el análisis anterior

### 5.1 Estados de `MIGRATION_MATRIX.md` (22 capacidades)

| ID | Estado previo | Clasificación | Motivo |
| --- | --- | --- | --- |
| CF-L017 | REEMPLAZADA | CONFIRMADA_EN_CODIGO | Convenio por cliente con fórmulas (§2.A.3) |
| CF-L018 | REEMPLAZADA | INCOMPLETA | El reemplazo existe, pero la vigencia ofrecida (Programado) no funciona y no hay fecha fin (BR-06-001) |
| CF-L019 | REEMPLAZADA | INCOMPLETA | Ídem |
| CF-L020 | REEMPLAZADA | CONFIRMADA_EN_CODIGO | Archivar |
| CF-L065 | REEMPLAZADA | INCOMPLETA | El API existe; la UI de tarifas base es solo Admin, contra §10 (BR-06-002) |
| CF-L066 | REEMPLAZADA | INCOMPLETA | Ídem; IVA por `ServiceTax` confirmado |
| CF-L067 | REEMPLAZADA | INCOMPLETA | Ídem |
| CF-L068 | REEMPLAZADA | INCOMPLETA | Ídem |
| CF-L069 | REEMPLAZADA | CONFIRMADA_EN_CODIGO | TRM DIAN o manual por depósito; COP y USD |
| CF-L070 | REEMPLAZADA | CONFIRMADA_EN_CODIGO | `PUT billing/warehouse-storages/{id}/trm` |
| CF-L071 | REEMPLAZADA | CONFIRMADA_EN_CODIGO | Solo la manual, antes de aprobar |
| CF-L072 | REEMPLAZADA | CONFIRMADA_EN_CODIGO | Sin catálogo |
| CF-L201 | PARCIAL | OBSOLETA | Los ciclos legacy y la regla de períodos ya existen (F3-05, F3-06); quedan BR-06-003 y BR-06-014 |
| CF-L202 | PARCIAL | OBSOLETA | Motor + N.º SIIGO implementados; quedan BR-06-004…007 |
| CF-L203 | CUBIERTA | INCOMPLETA | Sin filtros por depósito ni CPI (BR-06-008) |
| CF-L204 | CUBIERTA | INCOMPLETA | Sin fecha de factura ni cambio de destinatario en UI (BR-06-006, 007) |
| CF-L205 | COMPORTAMIENTO DIFERENTE | OBSOLETA | Anular + refacturar (F3-10, P9) |
| CF-L206 | PARCIAL | OBSOLETA | Informe anual con Excel (F5-08); queda BR-06-006 |
| CF-L207 | PARCIAL | OBSOLETA | Informe por depósito (F5-08); queda BR-06-009 |
| CF-L234 | PARCIAL | OBSOLETA | Regla legacy en el calculador y el job; quedan BR-06-005, 010 |
| CF-L249 | REEMPLAZADA | INCOMPLETA | El endpoint que cita (`GET system/dian-trm/today`) no tiene consumidor; el reemplazo real es la consulta en el servidor |
| CF-L251 | CUBIERTA | INCOMPLETA | Sin búsqueda por CPI ni autocompletar (BR-06-009) |

Conteo: CONFIRMADA_EN_CODIGO 6 · INCOMPLETA 10 · OBSOLETA 6 · CONTRADICHA_POR_CODIGO 0 · NO_VERIFICADA 0.

### 5.2 Afirmaciones de planes y decisiones

| Afirmación | Clasificación | Evidencia |
| --- | --- | --- |
| F3-05: unión de ciclos, catálogo, ventana consolidada | CONFIRMADA_EN_CODIGO | `BillingCycleCatalog.cs:24-62`; son 8 y no 9 porque §10 retiró `OnDemand` (DEF-F6-008) |
| F3-06: regla legacy, `LimitDate`, job por fecha límite, P8 | CONFIRMADA_EN_CODIGO | `StoragePeriodCalculator.cs`; `BillingJobService.cs:154-282`; `ApproveInvoiceHandler.cs:24-29` |
| F3-10: anular y refacturar | CONFIRMADA_EN_CODIGO | `CancelInvoiceHandler.cs`; `ReissueInvoiceCommandHandler.cs`. Evolución: la nueva nace sin vencimiento (CHG-12), no «ahora + plazo» como decía el ítem |
| F5-08: informe anual y por CPI | CONFIRMADA_EN_CODIGO | `BillingReportsController.cs`; handlers |
| DEC-020 la factura siempre se genera | INCOMPLETA | Falla con servicio complementario sin tarifa (BR-06-004) |
| DEC-021 sin creación manual | CONFIRMADA_EN_CODIGO | §4 de este documento |
| DEC-022 recálculo único | CONFIRMADA_EN_CODIGO | `RecalculateCoreAsync`; `Invoice.ReplaceStorageLines` |
| DEC-023 TRM fuera de báscula | CONFIRMADA_EN_CODIGO | `EnsureTrmAsync`; guardas de N.º y aprobación; `AssignDianTrm`/`AssignManualTrm` |
| DEC-024 N.º SIIGO | CONFIRMADA_EN_CODIGO | `Invoice.AssignInvoiceNumber`, `IsNonFiscal` |
| DEC-025 dos fórmulas de porcentaje | CONFIRMADA_EN_CODIGO | Calculadoras; la decisión del cliente sigue abierta (`estado.md` §6) |
| DEC-026, DEC-027, DEC-028 | CONFIRMADA_EN_CODIGO | `StorageBillingService.cs:156-235`; `BillingResolver.cs:46-50`; `StorageBillableQuantity` |
| DEC-041 tarifas T1–T4 | NO_VERIFICADA | Son datos de configuración (P13: tarifas a mano), no código |
| `DECISIONES_REVISION.md` §1.3, §1.4, §2.A.3, §2.B.6, §2.B.7 | CONFIRMADA_EN_CODIGO | Ver `03-reglas-negocio.md` |
| GAP-007, GAP-008 (construir), GAP-020 (aceptado) | CONFIRMADA_EN_CODIGO | Ídem |
| `pending-deposits` conserva su criterio (plan F3-10, desviación 11) | CONFIRMADA_EN_CODIGO | Es la causa de BR-06-003 |
| Manual `manual-modulo-facturacion.md` | OBSOLETA | Su propio aviso (`docs/manuales/manual-modulo-facturacion.md:3-6`); describe la creación manual (§3.2) |
| MAF-07, MAF-08, MAF-14 (`analisis-motor-acuerdos-facturacion-2026-09-17.md`) | CONFIRMADA_EN_CODIGO | Siguen presentes: BR-06-004, BR-06-001, BR-06-005 |
| `estado.md` §1 «toda la funcionalidad planeada está implementada» (para este módulo) | INCOMPLETA | Implementada con 14 brechas, 2 ALTA |

## 6. Incertidumbres

- **Horario real del cron legacy:** no hay crontab en el repositorio; ejecutado sin sesión, dos de sus `INSERT` usan `$_SESSION['usuario_id']` vacío y fallarían. En la práctica la regeneración ocurría al abrir «Depósitos x Facturar».
- **BR-06-004** se dedujo del código: QA no logró reproducir la configuración (F6-ALM-014 «NO APLICA»). Confianza MEDIA.
- **Quién usaba convenios, tarifas y tasas en el legacy:** depende de la tabla `permisos` (datos reales, no consultados).
- **FOB/CIF:** la base de cobro del almacenamiento depende de una equivalencia no validada (`estado.md` §4 n.º 8).
- La fase F6 de QA corrió sobre BE `191d4b1` (2026-10-02); los defectos se re-probaron en F11, pero no hubo una corrida completa de F6 sobre el corte auditado.

## 7. Sin analizar y por qué

- Las páginas de informes como pantallas (PDF, impresión, columnas) y los Excel: módulo 07. Aquí solo el cálculo.
- Los cobros de báscula, montacargas y guía (CF-L116…118, montacargas, guía): módulos 02, 03 y 05; se usaron como consumidores del motor.
- La importación de depósitos y la apertura de facturación de migrados (`OpenMigratedBillingCommand`): módulo 08 (CF-V081).
- `InvoicePdfService` en detalle y el contenido del correo de los avisos.
- Concurrencia entre instancias del job (MAF-09): requiere ejecución.
