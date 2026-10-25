# Registro de datos QA-PRE — ronda de preproducción (2026-10-25)

> Base `wms_qa_preprod` (copia de `wms_migracion`). Informe: `qa/resultados/PRE-informe-2026-10-25.md`. Sin contraseñas.
> Todo lo creado lleva el prefijo `QA-PRE` (o `QA PRE` en los nombres de usuario y `QP…` en las placas).

## Cuentas

| Usuario | Roles | Uso |
| --- | --- | --- |
| `qa.pre.boot` | Admin | Admin de arranque (`Bootstrap`), solo para crear las demás |
| `qa.pre.admin` | Admin | Administración y pantallas de Admin |
| `qa.pre.comext` | Comercio exterior | CE |
| `qa.pre.vigilancia` | Operario vigilancia | Vigilancia |
| `qa.pre.bascula` | Operario báscula | Báscula |
| `qa.pre.bodega` | Operario bodega | Bodega |
| `qa.pre.facturacion` | Facturación | Facturación |
| `qa.pre.multi1` | Facturación + Comercio exterior | Multirol |
| `qa.pre.multi2` | Báscula + Comercio exterior | Multirol |

## Maestros

| Clave | Dato | Id / valor |
| --- | --- | --- |
| C1 | `QA-PRE Cliente Uno SAS` (NIT 900100001), cliente e importador | `e8cd3c42-8d6a-4f7d-9a37-7508848e3902` |
| C2 | `QA-PRE Cliente Dos SAS` (900100002), cliente e importador | `2717f51d-b5a3-48b2-99bc-55b0d41fc5d6` |
| CM | `QA-PRE Cliente Mora SAS` (900100003), cliente e importador | `f68b8b19-0962-40db-955a-3910f87faeb6` |
| CS | `QA-PRE Cliente Sin Salidas SAS` (900100004), cliente e importador | `9da8bfa0-d66a-4d4a-9d88-a0be5971b727` |
| EX | `QA-PRE Exportador SAS` (900100005), cliente y exportador | `6fd9933a-0dc6-488b-b968-1f8de3433243` |
| AG | `QA-PRE Agencia SIA SAS` (900100006), agencia de aduanas | `69297f3a-eaad-4d40-a146-e23aa2c74530` |
| TR | `QA-PRE Transportes SAS` (900100007), transportadora | `8e7b573f-1340-410a-89a5-a5bc67efb5b0` |
| Ciudad | `QA-PRE Destino Abandono` (COL, 2 días, destino de abandono) | creada por `POST administration/cities` |
| Convenio | `QA-PRE-CONV-EX` de EX: ALMACENAMIENTO `FIXED` EXP001 $150.000 + IVA, activo | creado por `qa.pre.facturacion` |
| Productos migrados usados | P1 `CEBOLLA FRESCA ROJA`, P2 `ACEITE DE PALMA`, P3 `LLANTAS VARIAS REF` | sin modificar |
| Ciudades migradas usadas | Pasto, Quito | sin modificar |
| Ubicación / cuadrilla migradas usadas | `Bodega 2 BA-[1][1]` · `CBA - Bodegas Asociadas` | sin modificar |
| Conductores | `QA-PRE Conductor N` (documentos `99000…`), creados en los registros de báscula o por CE | — |
| Configuración | Tarifas de montacargas de DEC-041; `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` = `qa.pre.ajustes@local.test` | — |

## Operación (B2)

| Flujo | Placas | Documento | Depósito | Tiquetes / órdenes / guías | Facturas | Estado final |
| --- | --- | --- | --- | --- | --- | --- |
| E2E-01 | QPA001, QPA002 | QA-PRE-CP-001 | `2026BA00002` (C1) | `2026T00003`, `2026T00004`; `2026OC00002`; `2026S00002` | `QA-PRE-FE-0001` (almacenamiento, Aprobada); báscula y guía pagadas | Cerrado, OC Despachada |
| E2E-02 | QPA003–QPA006 | QA-PRE-CP-002 | `2026BA00003` (C2) | `2026OC00003`, `2026OC00004`; `2026S00003`, `2026S00004` | almacenamiento Borrador | Cerrado |
| E2E-03 | QPA007–QPA009 | QA-PRE-CP-003 | `2026BA00004` (C1) | — | `QA-PRE-FE-0003` (Aprobada, actualizada por el camión tardío) | Confirmado, ingreso cerrado; QPA009 rechazado (409) |
| E2E-04 | QPA010, QPA011 | QA-PRE-CP-004 | `2026EXP00001` (EX) | `2026OC00005`; `2026S00005` (exportación, automática) | almacenamiento $178.500 Borrador | Cerrado |
| E2E-05 | QPD001, QPD002 | QA-PRE-CP-D01 | `2026EXP00002` (EX), contenedor `QPCU0001` | `2026OC00016`; `2026S00010` (automática) | almacenamiento Borrador | Cerrado |
| E2E-06 | QPA019 | QA-PRE-CP-006 | `2026INSP00002` (C1) | — | mínimo $0 Borrador | Confirmado |
| E2E-07 | QPA012–QPA015 | — | — | tiquetes `2026T00011…14` | `QA-PRE-FE-0007` Pagada; cobros inmediato, a no registrado y a consumidor final | — |
| E2E-08 | QPA020 | QA-PRE-CP-008 | `2026BA00008` (C1) | — | mínimo $50.000 Borrador | Confirmado |
| E2E-09 | QPA021 | QA-PRE-CP-009 | `2026BA00009` (C2) | montacargas Tractomula | $261.800 Pagada | Cerrado (E2E-10) |
| E2E-10 | QPA022 | — | `2026BA00004` + `2026BA00009` | `2026OC00007`; `2026S00007` | dos facturas de guía Borrador | Despachada |
| E2E-11 | QPA016–QPA018 | QA-PRE-CP-011A/B | `2026BA00005`, `2026BA00006`, `2026BA00007` | `2026OC00006` revertida; `2026S00006` anulada | refacturada y anulada | Anulados |
| E2E-12 | QPC020–QPC024 | QA-PRE-CP-C21/C23/C24 | `2026BA00025`, `2026BA00026`, `2026BA00029` (CM) | `2026OC00012`; `2026S00009` | `QA-PRE-FE-MORA1` Pagada | CM `Active` |
| E2E-13 | QPC015, QPC016 | QA-PRE-CP-C15 | `2026BA00024` (C2) | OC de 100 | dos períodos cerrados | Cerrado |
| E2E-14 | QPC030 | QA-PRE-CP-C30 | `2026BA00028` (C2), TRM manual 3.950 | — | `QA-PRE-FE-TRM1` Aprobada | Confirmado |
| E2E-15 | QPD003 | QA-PRE-CP-D03 | `2026BA00030` (C1), ingreso del 24/10 | — | Borrador | Confirmado |
| E2E-16 | QPD094 → QPD004 | QA-PRE-CP-D04 | `2026BA00031` (descartado) | — | — | Anulado |
| E2E-17 | QPD005 | QA-PRE-CP-D05 | `2026BA00032` (C1) | `2026OC00017`; `2026S00011` | — | Cerrado |

## Operación (B3, B4, B5, B7)

| Uso | Datos |
| --- | --- |
| Sin salidas (F1-TER-019, F5-OC-023, F5-GUI-018) | QPA023/QPA024, `2026BA00010` (CS), `2026OC00008`, `2026S00008` |
| Un pesaje para dos documentos (F3-MUL-005, F3-COR-011) | QPA025, `2026BA00011` (C1) y `2026BA00012` (C2), ciclo `d13cf892-…` |
| Modo intermedio (F3-MUL-001…004, F3-COR-001/006/010) | QPD006, `2026BA00033` (C1) y `2026BA00034` (C2) |
| Solo báscula Tara primero (F3-SBA-003) | QPD007, tiquete `2026T00046` |
| Convenio de C2 `QA-PRE-CONV-C2` | Almacenamiento IMP 0,25 % (mín. $45.000 con IVA); P3 IMP PER_UOM $1.000; P1 perecedero PER_UOM $2.000; montacargas `FIXED` $100.000 |
| Convenios de C1 | `QA-PRE-CONV-C1-A` (0,20 %, archivado), `QA-PRE-CONV-C1-B` (0,22 %, programado para el 25/10 y activado por el job), `QA-PRE-CONV-C1-TAR008` (Borrador, rechazó 150 %) |
| Convenio de CS `QA-PRE-CONV-CS` | Almacenamiento IMP 0,30 % con complementario PAPELERIA (F6-ALM-014, `2026BA00035`) |
| Tarifas (F6-TAR-*) | `2026BA00013` (P1, 0,25 %), `2026BA00014` (P3, PER_UOM), `2026BA00015` (P1 perecedero), `2026BA00016` (EX con importador C1, tarifa base), `2026BA00017` (montacargas de C2) |
| Recálculo (F6-REC-*) | `2026BA00018` (`QA-PRE-FE-0106`, pagos y CE-7), `2026BA00019` (factura anulada), `2026BA00020` (dos camiones; pesaje de QPB009 anulado) |
| Palancas (F6-ALM-009/017/019) | `2026BA00014`, `2026BA00021`, `2026BA00022`, `2026BA00023` (ver §3 del informe) |
| Órdenes F5 | `2026OC00018` (cancelada), `2026OC00019` (ganadora de la concurrencia, guía `2026S00012`), `2026OC00021` y guía `2026S00014` (doble envío) |
| Precio programado (F1-SRV-021) | GUIA_SALIDA: $18.000 programados, $16.000, $18.000 y de nuevo $15.000 vigente desde el 25/10 |
| Migración por CSV (FA-MIG-*) | Clientes legacy `990000001`, `990000002`; producto `990000101`; depósitos `990001` (2023 y 2025) → `2023BA00021`, `2025BA00001`; `990002` → `2025BA00002` (prórroga); `990003` → `2025EXP00001`; `990004`, `990005` → `2025BA00003`, `2025BA00004`; levantes `QA-PRE-LEVM1/2` |
| Salida de un migrado (PRE-B5-09) | QPD010, `2024BA00005`, `2026OC00020`, `2026S00013` (por facturar al cliente del depósito) |
| Respaldos | Destinos «QA-PRE local» (scratchpad del ejecutor) y «QA-PRE s3mock» (bucket `wms-qa-pre`), los dos inactivos al terminar |
| Mora | Configuración de facturación de CM: mensual, plazo 0, límite $1.000 |

## Estado final

- 43 depósitos creados en la ronda: 37 de 2026 (`2026BA00002…00035`, `2026EXP00001…00002`, `2026INSP00002`) y 6 por CSV (`2023BA00021`, `2025BA00001…00004`, `2025EXP00001`). Órdenes `2026OC00002…00023`, guías `2026S00002…00014` (`2026S00006` anulada), tiquetes hasta `2026T00048`.
- Facturas con número QA-PRE: `QA-PRE-FE-0001`, `QA-PRE-FE-0003` y `QA-PRE-FE-TRM1` aprobadas; `QA-PRE-FE-0007`, `QA-PRE-FE-0106` y `QA-PRE-FE-MORA1` pagadas; `QA-PRE-FE-0018` anulada.
- DEF-F11-034: `QPE001` (salida iniciada en báscula, `2026OC00022` cargada sin guía) sigue en planta porque la salida responde 409; `QPE002` (`2026OC00023`, cargada sin báscula) salió sin guía.
- Todos los demás camiones `QP…` tienen la salida registrada.

## Re-test de DEF-F11-030 y DEF-F11-034 (2026-10-25)

Datos creados en `wms_qa_preprod` por el re-test (informe PRE, §11). Prefijo `QA-PRE-RT-`.

| Dato | Uso |
|---|---|
| `2026BA00036` (C1, USD 10.000 → 20.000 → 15.000; factura `QA-PRE-FE-RT01` aprobada) | F5-COR-007 valor y factura aprobada; F5-COR-008 bloqueo |
| `2026BA00037` (C1 → C2, COP → USD 30.000; factura anulada y refacturada a C2) | F5-COR-007 moneda y agencia; F5-COR-008 anulada |
| `2026BA00038` (C1 → C2, 30 unidades, levante 30) | F5-COR-008 Borrador; origen de `2026OC00024` |
| `2026BA00039` (C1, 100 unidades, factura `QA-PRE-FE-RT20` aprobada; `Closed`) | E2E-01 |
| `2026BA00040` (C1, 10 unidades, tiquete `2026T00055`) | E2E-17 |
| `2026EXP00003` (C1, 20 unidades) | F4-CAR-017 exportación |
| `2026OC00024` (`Loaded`, guía `2026S00015`), `2026OC00025` (`Dispatched`, `2026S00016`), `2026OC00026` (cancelada; guía `2026S00017` anulada), `2026OC00027` (`Dispatched`, `2026S00018`), `2026OC00028` (`Dispatched`, guía de exportación `2026S00019`) | F4-CAR-016/017, PRE-B2-SAL-01, E2E-01, E2E-17 |
| Camiones `QPR001`–`QPR003`, `QPR010`, `QPR020`, `QPR021`, `QPR030`, `QPR040`, `QPR041`; conductores `QA-PRE Conductor 9nn` | Ingresos del re-test |

Quedan en planta: `QPR001`–`QPR003` y `QPR030` (camiones de ingreso de los depósitos) y `QPR041`. `QPR010`, `QPR020`, `QPR021` y `QPR040` salieron.
