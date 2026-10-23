# Registro de datos QA — Fase 11 (re-test, regresión y cierre)

> Lo actualiza cada sesión de la fase 11 (S0 a S4). Sirve para que la sesión siguiente reutilice datos sin adivinarlos. **Sin contraseñas ni tokens.**
> Ambiente: Local (`localhost:3000` / `localhost:5281/api/v1`, Postgres Docker `wms-postgres-db` puerto 5433, base `wmsdb`) · Base recreada durante la implementación del plan de corrección (9 migraciones, solo datos sembrados) · Datos creados en S0 el 2026-10-05 entre las 16:56 y las 17:13 (hora Colombia).
> Builds: frontend `develop` `0a6267b` (código en `4074c63`; `0a6267b` solo toca documentación) · backend `develop` `09b0baf`.
> El registro de la campaña anterior (`registro-datos-qa.md`) es referencia: **sus datos no existen en esta base**.
> **Método de S0:** datos creados por el API con el usuario del rol que corresponde (`capb90` en Administración, `vigilancia`, `bascula`, `bodega`, `c_exterior`, `facturacion`), con los mismos contratos que envía la pantalla. Las contraseñas se leen del README en tiempo de ejecución y no se copian.

## Usuarios
| Usuario | Roles | Activo | Creado en fase | Nota |
|---|---|---|---|---|
| admin | Admin | Sí | (bootstrap) | Sigue con «debe cambiar contraseña»; no se usó salvo para crear `capb90`. Su contraseña la define el usuario. |
| capb90 | Admin | Sí | F11-S0 | Administrador de trabajo del QA |
| vigilancia | Receiving | Sí | F11-S0 | |
| bascula | Scale | Sí | F11-S0 | |
| facturacion | Billing | Sí | F11-S0 | |
| bodega | Warehouse | Sí | F11-S0 | |
| c_exterior | ForeignTrade | Sí | F11-S0 | |
| v_montenegro | Billing + Admin | Sí | F11-S0 | Multi-rol |
| j_coral | Billing + ForeignTrade | Sí | F11-S0 | Multi-rol |
| f_chosi | Scale + ForeignTrade | Sí | F11-S0 | Multi-rol |
| qa_inactivo | Warehouse | **No** | F11-S0 | Desactivado sin fecha de bloqueo (F1-USR-013). Login responde «Usuario inactivo. Comuníquese con el administrador.» |

> Las 10 cuentas QA se crearon con la contraseña temporal del README y pasaron por el cambio obligatorio a la contraseña del README. Correo `<usuario>@bodegas-qa.test`, teléfono `+570000000000`, identificaciones 100000001–100000010.

## Estado inicial de catálogos (antes de S0)

| Catálogo | Estado |
|---|---|
| Productos, terceros, vehículos, conductores, ciudades, cuadrillas, embalajes | 0 |
| Servicios | 5 sembrados (ALMACENAMIENTO con IVA; BASCULA sin precio ni IVA) |
| Mínimos de almacenamiento | IMP, EXP e INSP en $0, «incluye IVA» = No |
| Tarifas de montacargas | 5 tipos sin monto |
| Ciclos de facturación | Sin `OnDemand` (CHG-60); 8 ciclos |
| Parámetros | `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` vacío; `COMPANY_*` sembrados con el pie del legacy (CHG-84) |
| Ubicaciones 20 · Unidades de medida 10 · Tipos de unidad de carga 3 · Motivos 7 · Roles con `NormalizedName` corregido (`FOREIGNTRADE`, CHG-04) | |

## Terceros
| Nombre | Identificación | Roles de negocio | Config. facturación | Estado financiero | ID |
|---|---|---|---|---|---|
| QA Cliente Uno SAS | NIT 900100001 | CUSTOMER | Mensual · 30 días · PerService · sin límite | Active | `e329015c-1131-456e-8351-5dd40420f26b` (contacto Ana QA 3001000001; cuenta Bancolombia Ahorros; convenio QA-CONV-001) |
| QA Cliente Mora SAS | NIT 900100002 | CUSTOMER | Mensual · 30 · PerService · límite 1.000 | **Blocked** (S0, palanca) | `9aa003ad-f17d-4352-aa77-d08ca167532b` |
| QA Cliente Consolidado SAS | NIT 900100003 | CUSTOMER | Quincenal (Biweekly) · 15 · Consolidated · límite 10.000.000 | Active | `1dcfd0c3-a69d-4d6d-af25-09efdac483cf` |
| QA Importación Andina Ltda | NIT 900100004 | IMPORTER | — | Active | `f9e96dbb-e562-4a4c-90cf-ba381a3e43c7` |
| QA Exportador SAS | NIT 900100005 | EXPORTER | — | Active | `e162f840-9b6f-4a7c-b262-863183b0d24d` |
| QA Agencia SIA Aduanas | NIT 900100006 | CUSTOMS_AGENCY | — | Active | `9b5b78a8-57f5-486c-b046-f2f8e3d762cd` |
| QA Transportes SAS | NIT 900100007 | TRANSPORT_COMPANY | — | Active | `0f89cd64-8519-4f50-b024-5c3a81a57437` (contacto Tomas QA 3001000007) |
| QA Importadora Quito Cía | RUC 1790000000001 | IMPORTER, CUSTOMER | Days15 · 5 · PerService · sin límite | Active | `f1936f25-44e4-44d5-96eb-1a87d71df639` (contacto en Ecuador) |
| QA Multirol Comercial | NIT 900100008 | CUSTOMER, IMPORTER | Semanal · 10 · PerService · límite 0 | Active (factura parcial aprobada, ver Facturas) | `1f15afc0-04bf-42bc-832a-28365b770ae0` |
| QA Compañía Ñandú Transportes | NIT 900100092 | TRANSPORT_COMPANY | — | Active | `257bbe60-0f15-4eaa-ab31-cc3fd45aac48` (para PDF con ñ) |

## Catálogos y tarifas
| Tipo | Código / nombre | Valor relevante | ID | Fase |
|---|---|---|---|---|
| Convenio | QA-CONV-001 (QA Cliente Uno), Active | ALMACENAMIENTO IMP `PERCENTAGE_OF_VALUE` 0,255 % / mínimo 184.000 / umbral 72.156.863 · BASCULA `FIXED` 25.000 · MONTACARGAS `PER_VEHICLE_TYPE` 90/70/50/45/30 mil · GUIA_SALIDA `FIXED` 30.000 | `ba770f5f-b251-4896-8d1c-1e1b11aba0ae` | S0 |
| Precio base | BASCULA | 24.000 vigente desde 2026-10-05 | `9ee6290c-…` | S0 |
| Precio base | GUIA_SALIDA | 35.000 vigente desde 2026-10-05 | `8b45bcb0-…` | S0 |
| Impuesto | BASCULA | IVA 19 % asignado (§10 · IVA en báscula). ALMACENAMIENTO trae IVA sembrado. | | S0 |
| Tarifa base | ALMACENAMIENTO IMP · QA Cebolla | `PER_UOM` 1.500 por BULTO | `3fcbee77-6353-4d2b-b90d-70bba69e9c85` | S0 |
| Tarifa base | ALMACENAMIENTO EXP (genérica) | `FIXED` 150.000 | `5f9bc257-ad43-4696-b1d8-20c58378a28d` | S0 |
| Mínimo | ALMACENAMIENTO | IMP 184.000 **neto** («incluye IVA» = No); EXP 0; INSP 0 | IMP `e8f9a0b1-c2d3-4678-a9b0-c1d2e3f4a5b6` | S0 |
| Tarifas montacargas | Tractomula 80.000 · DobleTroque 65.000 · Sencillo 45.000 · Turbo 40.000 · GuacalEstiba 25.000 | | | S0 |
| Producto | QA Cebolla | BULTO, embalaje QA-CAJA, SKU QA-SKU-CEBOLLA | `e6f76b4c-6768-463c-9765-e21354693ff5` | S0 |
| Producto | QA Aceite | LITRO, SKU QA-SKU-ACEITE | `df772dda-b9bc-4c57-a5b2-1eb63590decc` | S0 |
| Producto | QA Repuestos | UNIDAD, SKU QA-SKU-REPUESTOS | `e770c353-2127-4879-82bd-5e88f9da2981` | S0 |
| Embalaje | QA-CAJA | QA Caja de cartón | `ed24312f-ae75-4153-b41b-24ea44c1cb45` | S0 |
| Tipo de unidad de carga | QA_ISOTANQUE | QA Isotanque | `73f9dcc7-8a7f-4310-a9f3-12b7b735ca19` | S0 |
| Ciudad | QA Quito | ECU, PICHINCHA, 3 días | `abbe7076-c61e-46c2-822f-62cac532a9c4` | S0 |
| Ciudad | QA Bogota | COL, DC, 0 días, destino de abandono | `317cbd1e-f747-4660-b939-42293f9c20d4` | S0 |
| Cuadrilla | QA Cuadrilla 1 | activa | `89190a8d-7462-4f2a-a2cf-48665e41887e` | S0 |
| Parámetro | INVENTORY_ADJUSTMENT_ADMIN_EMAIL | qa-ajustes@bodegas-qa.test | | S0 |
| Parámetros | COMPANY_NAME / NIT / ADDRESS / PHONE / EMAIL / CITY | Sembrados (pie del legacy), sin cambios | | (migración) |

> No creados en S0 (los crea el caso que los prueba): convenios del Consolidado con fórmulas `PERCENTAGE_OF_VALUE_PRORATED`, `PER_VEHICLE`, `WEIGHT_THRESHOLD`, `PER_CARGO_UNIT`; reglas para perecederos; motivo `QA Motivo pesaje`; ubicación no disponible; unidad de medida inactiva.

## Vehículos y conductores
| Placa / documento | Tipo | Transportadora / país | ID | Fase |
|---|---|---|---|---|
| QAA101 | Tractomula | QA Transportes SAS / Colombia (Admin) | `33274f52-46e4-479e-83ea-2053f61b0311` | S0 |
| QAA102 | Sencillo | QA Transportes SAS / Colombia (Admin) | `68c9c115-92a4-4dfe-9cb5-1dc7e794a798` | S0 |
| QAA103 | Turbo | QA Transportes SAS / Ecuador (Admin) | `f432cc2b-072d-4fca-90a1-5fbd889a033a` | S0 |
| QAB201, QAB202, QAB205 | Tractomula | QA Transportes SAS / Colombia (creados por `vigilancia`) | | S0 |
| QAB203, QAB204 | Sencillo | QA Transportes SAS / Colombia (`vigilancia`) | | S0 |
| QAC401–QAC406 | Sencillo | QA Transportes SAS / Colombia (`vigilancia`) | | S0 |
| CC 1000000001 | Conductor Pedro QA Conductor Colombia, tel. 3002000001 | Colombia | `28c2adbd-cffc-4698-b368-5988b2706751` | S0 |
| Pasaporte 1700000001 | Conductor Jorge QA Conductor Ecuador, tel. 0992000001 | Ecuador | `00dfc212-6b92-4970-96d9-ded59c18f906` | S0 |

## Ingresos (Vigilancia)
| Placa | Motivo | Hora ingreso (CO) | Salida | EntryLog ID | Fase | Usado en |
|---|---|---|---|---|---|---|
| QAA101 | Descargue mercancía importación | 17:03 | 17:08 | `478091b6-3d8a-4c9b-8890-880577037905` | S0 | BA00001 camión 1 |
| QAB201 | Descargue mercancía importación | 17:03 | 17:08 | `84d65954-ff52-406f-a3dc-fdd2d7fc8e88` | S0 | BA00001 camión 2 |
| QAA102 | Descargue mercancía exportación | 17:03 | 17:08 | `739cb56e-85fd-47a1-8b23-b414e0f6ab95` | S0 | EXP00001 |
| QAB203 | Descargue mercancía importación | 17:03 | 17:08 | `bfd81073-cfe5-45b1-b0eb-bbea47cd1667` | S0 | INSP00001 (modalidad elegida en báscula) |
| QAB202 | Descargue mercancía importación | 17:03 | **abierto** | `473f23a2-3c0a-4792-b563-ce0d9dcaa48a` | S0 | BA00002 tanquero, ciclo con primer peso |
| QAA103 | Solo báscula | 17:03 | 17:08 | `e2126c57-6aa7-41fd-8386-cd5bc9a37c06` | S0 | Solo báscula T00006 |
| QAB204 | Solo bodega | 17:03 | **abierto** | `f6abfaba-33c4-4540-a6ff-4576e1ab02b1` | S0 | Recepción sin báscula (re-test DEF-F4-002/005, DEF-F8-005) |
| QAB205 | Cargue mercancía importación | 17:07 | 17:08 | `fae3e8ae-50d3-4449-88df-f18610640d66` | S0 | Salida 2026OC00001 |
| QAC401, QAC402, QAC403 | Solo báscula | 17:09 | 17:09 | | S0 | Operaciones **descartadas** (ver nota) |
| QAC404 | Solo báscula | 17:09 | 17:10 | `7c7b3afb-2a46-49fe-a1a2-8dd01e893a9b` | S0 | Cobro por facturar a QA Cliente Mora |
| QAC405 | Solo báscula | 17:09 | 17:10 | `8c036b33-d0a4-4ad3-a129-d74540fd1d4b` | S0 | Cobro por facturar a QA Multirol |
| QAC406 | Solo báscula | 17:09 | 17:10 | `bb8f5d05-7733-49c7-80c6-86f41ee4b05b` | S0 | Cobro por facturar a QA Cliente Consolidado (factura anulada) |

> **Nota QAC401–QAC403:** el script de preparación envió el cobro «por facturar» con total 0 (400 «El total a pagar debe ser mayor a cero.») y siguió con la salida; los tres camiones salieron con su operación de Solo báscula registrada y sin cobro. Se descartaron por `DELETE weighbridge/incomplete/{id}`: los tres `ServiceRecord` quedaron `Discarded` y sin vínculo con el ingreso (comportamiento de CHG-06). Sirven como datos de trazabilidad de operaciones descartadas (DEF-F7-002).

## Operaciones de báscula
| Tiquete | Placa | Tipo operación | Documento / OC | Estado ciclo | Factura | Fase |
|---|---|---|---|---|---|---|
| 2026T00001 | QAA101 | Ingreso IMP | QA-CP-F11-001 | Complete (35.000 bruto / 15.000 tara) | `4a5fd48c` Paid 29.750 efectivo, QA Cliente Uno (sin N.º) | S0 |
| 2026T00002 | QAB201 | Ingreso IMP 2.º camión | QA-CP-F11-001 | Complete (30.000 / 12.000) | `6a33e723` **QA-SIIGO-F11-0003** Paid 29.750 (cobro por facturar, luego pagado) | S0 |
| 2026T00003 | QAA102 | Ingreso EXP | QA-CP-F11-002 | Complete (28.000 / 13.000) | `04aa23fb` Paid 29.750 transferencia QA-TRF-F11-001 | S0 |
| 2026T00004 | QAB203 | Ingreso INSP (pesaje único) | QA-CP-F11-003 | Complete (21.000 bruto) | `13253985` Paid 28.560 al conductor (persona no registrada) | S0 |
| 2026T00005 | QAB202 | Ingreso IMP tanquero QAT001 | QA-CP-F11-005 | **FirstWeightCaptured** (45.000 bruto), sin llegada a Bodega | `b43fa7f6` Paid 29.750 transferencia QA-TRF-F11-002 | S0 |
| 2026T00006 | QAA103 | Solo báscula (un pesaje, tara) | — | Complete (18.000) | `ed95aa99` Paid 28.560 Consumidor final | S0 |
| 2026T00007 | QAB205 | Salida con 2026OC00001 | 2026OC00001 | Complete (14.000 tara / 30.000 bruto) | `541677fa` Paid 29.750 QA Cliente Uno | S0 |
| 2026T00008 | QAC404 | Solo báscula por facturar | — | Complete (12.000) | `6634765c` QA-SIIGO-F11-0010 **Overdue** (Mora) | S0 |
| 2026T00009 | QAC405 | Solo báscula por facturar | — | Complete (12.000) | `06ad4f0b` QA-SIIGO-F11-0011 PartiallyPaid (Multirol) | S0 |
| 2026T00010 | QAC406 | Solo báscula por facturar | — | Complete (12.000) | `5e30ddfa` QA-SIIGO-F11-0012 **Cancelled** (Consolidado) | S0 |

> Tarifa de báscula observada: con QA Cliente Uno (convenio) 25.000 + IVA = 29.750; sin cliente con convenio (conductor, consumidor final, Mora, Multirol, Consolidado) precio base 24.000 + IVA = 28.560.

## Depósitos
| Número | Modalidad | Carta porte | Camiones | Estado | Cliente / terceros | Nacionalización | Fase |
|---|---|---|---|---|---|---|---|
| 2026BA00001 | IMP | QA-CP-F11-001 | QAA101 (100, manifiesto QA-MAN-F11-001A, 20.000 kg) + QAB201 (60, QA-MAN-F11-001B, 18.000 kg) | **Confirmed**, ingreso de camiones **cerrado** (2 camiones), TRM DIAN 3.273,49 | QA Cliente Uno · Importador QA Importación Andina · Agencia QA Agencia SIA · Transportadora QA Transportes · USD 50.000 · manifiesto DIAN QA-DIAN-F11-001 | **Nacionalizado** con QA-LEV-F11-001 (100 de 160, parcial) | S0 |
| 2026BA00002 | IMP · unidades de carga | QA-CP-F11-005 | QAB202 con tanquero **QAT001** (30.000 L QA Aceite) | **Draft**, ingreso abierto | QA Cliente Uno · Andina · SIA · USD 50.000 | Sin nacionalizar | S0 |
| 2026EXP00001 | EXP | QA-CP-F11-002 | QAA102 (50 QA Cebolla) | **Confirmed**, ingreso cerrado | QA Cliente Uno · Exportador QA Exportador SAS · COP 50.000.000 | — | S0 |
| 2026INSP00001 | INSP | QA-CP-F11-003 | QAB203 (40 QA Repuestos) | **Draft** con recepción completada | QA Cliente Uno · USD 50.000 | — | S0 |

| Depósito | ID | Producto del depósito (ID) | Stock al cierre de S0 |
|---|---|---|---|
| 2026BA00001 | `7cfba83d-79fe-44fb-bfa5-78c1fd93aaa3` (importación `a5747e47-9c1c-4336-bc83-f095ec9ee343`) | QA Cebolla `607f1e25-1ed0-4897-b99f-faa9b10341ed` | recibido 160 · stock 80 · reservado 0 |
| 2026BA00002 | `8d48b994-5ca6-41ab-bde0-3428ed0d32b9` (importación `d7bcbcbb-c90b-45be-af49-655da819d82b`) | QA Aceite `fc532ef0-a60d-4ca8-9228-3838aacd0ce4` | 30.000 L |
| 2026EXP00001 | `a1d3634d-fcc1-4da9-9cde-ede9e97151ae` | QA Cebolla `28350a91-ed30-4420-ae6c-abc86c917fcd` | 50 |
| 2026INSP00001 | `f0ecb041-128b-4cf3-a3dd-cad280510208` | QA Repuestos `3bd02cbd-37dc-4d41-b7b2-3f2117a98d8a` | 40 |

## Recepciones y montacargas
| ID | Depósito / placa | Estado | Diferencia | Factura | Fase |
|---|---|---|---|---|---|
| Recepción `361b15af` | 2026BA00001 / QAA101 | Completed (llegada + cierre; 1 foto, firma, QA Cuadrilla 1, A01-R01-N01), recibió `bodega` | 100 = 100 | — | S0 |
| Recepción `f6e70dae` | 2026BA00001 / QAB201 | Completed (A01-R01-N02), `bodega` | 60 = 60 | — | S0 |
| Recepción `a49925c4` | 2026EXP00001 / QAA102 | Completed (A01-R01-N03), `bodega` | 50 = 50 | — | S0 |
| Recepción `765460c8` | 2026INSP00001 / QAB203 | Completed (A01-R02-N01), `bodega` | 40 = 40 | — | S0 |
| Montacargas `8d0f7e8a` | BA00001 (servicio del ingreso) · Tractomula · 100 → 102 h | Complete, pago inmediato, sin IVA | — | `852f27f5` Paid 90.000 (tarifa del convenio para Tractomula; valor digitado 90.000 por 2 h) | S0 |
| Montacargas `6a7e5288` | BA00001 · GuacalEstiba · 200 → 203,5 h | Complete, por facturar, **con IVA** | — | `9457d5fe` Draft 35.700 (30.000 + IVA) | S0 |

## Levantes, órdenes de cargue y guías
| Tipo | Número | Depósito(s) | Estado | Factura | Fase |
|---|---|---|---|---|---|
| Levante | QA-LEV-F11-001 (aceptación QA-ACE-F11-001, 100 QA Cebolla, 20.000 kg, FOB USD 30.000) | 2026BA00001 | Vigente | — | S0 |
| Orden de cargue | 2026OC00001 (externa QA-OE-F11-001, emisor QA Agencia SIA, 80 QA Cebolla, QAB205, conductor Pedro QA, QA Quito, QA Cuadrilla 1) · ID `d2fc2d0e-2d85-4522-a1b5-9b3aecb1beb0` | 2026BA00001 | **Dispatched** (Pending → InProgress al iniciar la salida en báscula → Loaded al cargar → Dispatched al repesar con guía) | — | S0 |
| Guía de salida | 2026S00001 (Import, firmante Importador, vence 2026-10-08) · ID `28bf2753-6235-4fa5-89d7-3831dfd980d6` | 2026BA00001 / OC00001 | Vigente | `ce6be5e2` GUIA_SALIDA Paid 30.000 (convenio, sin IVA) | S0 |

## Facturas y pagos
| N.º interno / SIIGO | Servicio | Cliente / destinatario | Estado | Total | Pagado | Fase |
|---|---|---|---|---|---|---|
| `ebb447cc` / **QA-SIIGO-F11-0001** | ALMACENAMIENTO BA00001 (0,255 % × USD 50.000 × 3.273,49) | QA Cliente Uno | **PartiallyPaid** (aprobada, enviada; vence 2026-11-04) | 496.670,28 | 250.000 (P1 200.000 transferencia QA-PAG-F11-001 + P2 50.000 cheque QA-PAG-F11-002, ambos Verified) | S0 |
| `526302c5` / **QA-SIIGO-F11-0002** | ALMACENAMIENTO EXP00001 (tarifa base EXP FIXED 150.000) | QA Cliente Uno | **Approved** (vence 2026-11-04) | 178.500 | 0 | S0 |
| `6a33e723` / **QA-SIIGO-F11-0003** | BASCULA T00002 (por facturar) | QA Cliente Uno | **Paid** | 29.750 | 29.750 (P3 efectivo, Verified) | S0 |
| `6634765c` / **QA-SIIGO-F11-0010** | BASCULA T00008 | QA Cliente Mora | **Overdue** (palanca) → cliente **Blocked** | 28.560 | 0 | S0 |
| `06ad4f0b` / **QA-SIIGO-F11-0011** | BASCULA T00009 | QA Multirol Comercial | **PartiallyPaid** (aprobada, vence 2026-10-15) | 28.560 | 10.000 (P4, Verified) | S0 |
| `5e30ddfa` / **QA-SIIGO-F11-0012** | BASCULA T00010 | QA Cliente Consolidado | **Cancelled** («QA F11 S0: anulación de prueba del dataset») | 28.560 | 0 | S0 |
| `9457d5fe` (sin N.º) | MONTACARGAS por facturar | QA Cliente Uno | **Draft** | 35.700 | 0 | S0 |
| `4a5fd48c`, `04aa23fb`, `b43fa7f6`, `541677fa` (sin N.º) | BASCULA contado | QA Cliente Uno | Paid | 29.750 c/u | 29.750 | S0 |
| `13253985` (sin N.º) | BASCULA contado | Pedro QA Conductor Colombia (no registrado) | Paid | 28.560 | 28.560 | S0 |
| `ed95aa99` (sin N.º) | BASCULA contado | Consumidor final | Paid | 28.560 | 28.560 | S0 |
| `852f27f5` (sin N.º) | MONTACARGAS contado | QA Cliente Uno | Paid | 90.000 | 90.000 | S0 |
| `ce6be5e2` (sin N.º) | GUIA_SALIDA S00001 | QA Cliente Uno | Paid | 30.000 | 30.000 | S0 |

> Estados que S0 no deja: **PendingApproval** (ningún flujo del API la produce al asignar el N.º; la factura sigue en Draft hasta aprobar) y **Sent** distinto de PartiallyPaid (QA-SIIGO-F11-0001 pasó por Sent antes del pago). Pagos **Pending/Received/Rejected**: el API registra los pagos directamente como `Verified`, así que «Verificar» y «Rechazar» responden «Solo se pueden verificar pagos recibidos.» y «No se puede rechazar un pago ya verificado.»; se revisa en S2 con DEF-F6-009 (R-FAC-06).

## Períodos de almacenamiento
| Depósito | Estado | Período | Límite | Fórmula | Factura |
|---|---|---|---|---|---|
| 2026BA00001 | Open | 2026-10-05 → 2026-11-05 | 2026-11-08 | PERCENTAGE_OF_VALUE (417.369,98 neto) | QA-SIIGO-F11-0001 |
| 2026EXP00001 | Open | 2026-10-05 → 2026-11-05 | 2026-11-08 | FIXED (150.000 neto) | QA-SIIGO-F11-0002 |

## Palancas y ambiente
| Dato | Detalle |
|---|---|
| Palanca | `f11_palanca_mora_s0.sql` (patrón de `f8_palanca_mora.sql`): `due_date = now() - 2 días` en QA-SIIGO-F11-0010. Solo base local. Tras reiniciar el API, `OverdueDetectionJob` marcó 1 factura vencida y pasó a QA Cliente Mora de Active a Blocked en la primera corrida. |
| API | Pestaña del panel de terminal «wms-api (QA F11)» (`dotnet run --project Wms.Api --launch-profile http`); reiniciado una vez (17:12) para la corrida de los jobs. Log en el scratchpad de la sesión. |
| Frontend | Vista previa `wms-dev` (`localhost:3000`). Sesión del navegador abierta con `c_exterior`. |
| Avisos (tabla `notifications`) | `c_exterior`, `j_coral` y `f_chosi`: 2 «Nuevo depósito de importación» y 1 «Guía de salida requerida» cada uno; `admin`, `capb90` y `v_montenegro`: 1 «Cargue completado». |

## Equivalencias con la campaña anterior (para los casos detectores)

| Ficha(s) | Dato de la campaña anterior | Dato equivalente en esta base | Nota para el re-test |
|---|---|---|---|
| DEF-F1-005, DEF-F3-016 | `QAA101` y el duplicado inactivo `qaa101` | `QAA101` (Tractomula) | Crear `qaa101` y `QA A-1#` en el re-test: deben rechazarse (CHG-05). |
| DEF-F2-001, DEF-F2-002 | `QAA102`, `AA102`, `QAB201`… | `QAA102`, `QAB201`, `QAB202`, `QAB205` existen | Buscar `AA102` en Vigilancia no debe tomar `QAA102`. |
| DEF-F2-004, DEF-F7-002 | `QAA102`, `QAC304`, `QAF701` con salida; `QAC402` descartado | Ingresos con salida: QAA101, QAB201, QAA102, QAB203, QAA103, QAB205, QAC404–406 · descartados: QAC401–403 · ciclo en curso: QAB202 | Ver la trazabilidad de cada uno. |
| DEF-F3-001 | Avisos a CE | Avisos ya recibidos por `c_exterior`, `j_coral`, `f_chosi` (tabla de ambiente) | En S1 verificar en la interfaz y en tiempo real con un depósito nuevo. |
| DEF-F3-004 | `QAC402` / 2026BA00003 descartado | QAC401–QAC403 (descartados en S0, sin vínculo) | El re-test descarta una operación nueva y comprueba la cola y el cobro. |
| DEF-F3-005 | `QAC406` salida con ciclo abierto | `QAB202` (ciclo `FirstWeightCaptured`) | Intentar la salida en Vigilancia: debe rechazarse (CHG-30). **No** registrar la salida de QAB202. |
| DEF-F3-008 | `QAA103` (Solo báscula), `QAB205` (Salida) | T00006 (QAA103, conductor Jorge QA, Turbo, Ecuador) y T00007 (QAB205, Pedro QA) | Verificar que el conductor y el vehículo quedaron guardados. |
| DEF-F3-010 | `QA-CP-0001` con ingreso cerrado | `QA-CP-F11-001` (2026BA00001, ingreso cerrado por `c_exterior`) | Buscar el documento en báscula. |
| DEF-F3-012, DEF-F5-014 | `2026OC00001` (despachada), `2026OC00003` | `2026OC00001` (Dispatched con guía S00001) | F3-SAL-008 con OC00001; F3-SAL-009 y la salida sin guía necesitan una OC nueva sobre BA00001 (stock 80, nacionalizado). |
| DEF-F3-015, DEF-F8-009 | `QAA103`, `QAB203`, INSP00004 / T00024–25 | T00004 (INSP pesaje único 21.000) y T00006 (Solo báscula 18.000) | Historial, tablero y reporte diario de báscula del 05/10. |
| DEF-F4-001, DEF-F6-007 | 2026BA00005 tanquero `QAT001` | **2026BA00002** tanquero QAT001 (QAB202, sin llegada) | Registrar llegada y recepción de la unidad completa. |
| DEF-F4-002, DEF-F4-005, DEF-F8-005 | `QAB204` / INSP00002–03 | `QAB204` con ingreso «Solo bodega» abierto | Recepción sin báscula desde la interfaz: debe usar este ingreso y dejar el depósito en Borrador. |
| DEF-F4-003 | `QAA101/QAB201` segundo pesaje sin llegada | `QAB202` (T00005) sin llegada | Intentar el segundo pesaje antes de la llegada: debe rechazarse (CHG-36). |
| DEF-F4-014 | 2026OC00006 cargada | 2026OC00001 (Dispatched) | Reejecutar el cargue: mensaje de negocio, no 404 de reserva. |
| DEF-F4-018 | 2026INSP00001 en Borrador con mercancía recibida | **2026INSP00001** (Draft, recibido 40) | Inventario de Bodega. |
| DEF-F5-001 | 2026BA00002 en Borrador | **2026BA00002** (Draft) | Editar fecha del documento, moneda y valor. |
| DEF-F5-002, DEF-F5-003, DEF-F8-006 | 2026BA00001, BA00008, INSP00001, BA00027 | 2026BA00001 (Confirmed) e INSP00001 (Draft) | CE-7 y corrección de productos con kárdex; detalle de la factura con la cantidad ajustada. |
| DEF-F5-004 | **2026BA00004** (levante 20, recibido llevado a 15) | **2026BA00001** (levante QA-LEV-F11-001 de 100; recibido 160) | CE-7 a 90 (< 100 levantado) debe rechazarse. |
| DEF-F5-005 | 2026BA00011 anulado con levante | Ninguno | El re-test anula un depósito nuevo y prueba el levante. |
| DEF-F5-008 | 2026BA00001 con 2 camiones | **2026BA00001** (QAA101 + QAB201) | «Validar depósito» compara con los dos camiones. |
| DEF-F5-009 | OC00011 / OC00014 sobre BA00002 (QA-CP-0401) | 2026OC00001 (BA00001, QA-CP-F11-001, importador Andina, manifiesto QA-DIAN-F11-001) | Filtros de órdenes por documento, importador y manifiesto. |
| DEF-F5-010, DEF-F5-012 | 2026BA00002 / S00002 / S00006 | 2026BA00001 / **2026S00001** | Guía, factura y etiqueta; responsable de la recepción = `bodega`. |
| DEF-F6-001, DEF-F6-004 | EXP00001, INSP00001–04 | 2026EXP00001 (factura 178.500 con la tarifa base EXP) · INSP00001 (Draft; al confirmarse no debe tomar el convenio IMP) | Para el override se necesita una factura de almacenamiento en Borrador (la crea el re-test). |
| DEF-F6-002 | BA00002, BA00013, BA00017, BA00028 | Períodos abiertos de BA00001 y EXP00001 | Cierre manual de períodos. |
| DEF-F6-006 | QA-SIIGO-0011 (pago parcial) y QAE-SIIGO-003 | **QA-SIIGO-F11-0010** (sin pagos; ya Overdue y Mora Blocked en una corrida) y **QA-SIIGO-F11-0011** (pago parcial, Approved) | S1 aplica la palanca a F11-0011 y verifica Overdue + bloqueo de Multirol en una corrida. |
| DEF-F6-008 | BA00024 OnDemand | Ninguno | `PUT billing/configurations` con `OnDemand` ya responde 400 «El ciclo de facturación no es válido.» (visto en S0). |
| DEF-F6-018 | QA-SIIGO-0018 | QA-SIIGO-F11-0002 (Approved) | El re-test acerca el vencimiento con una palanca. |
| DEF-F6-021 | BA00005, BA00019 | BA00002 (tanquero) o un depósito nuevo | Mínimo IMP configurado como neto (184.000). |
| DEF-F7-003 | OC00017 sin guía, S00001 | Ninguno | El re-test crea una salida EXP o INSP. |
| DEF-F7-007 | 2026BA00004 refacturada | 2026BA00001 (QA-SIIGO-F11-0001) o EXP00001 (QA-SIIGO-F11-0002) | Anular y refacturar en el re-test. |
| DEF-F7-009 | 2026BA00001 kárdex | **2026BA00001** (declarado, cargue de 80) | |
| DEF-F7-010 | `QAA101` | `QAA101` | Buscar `qaa101` en la trazabilidad. |
| DEF-F7-011 | 2026T00001 | **2026T00001** (QAA101) | PDF del tiquete: contacto de la transportadora. |
| DEF-F8-002 | BA00004 + BA00017 (dos clientes) / OC00025 / S00011 | Ninguno | El re-test necesita un depósito de otro cliente (p. ej. Consolidado) además de BA00001. |
| DEF-F8-003 | **QAE026** / BA00036 / OC00029 (salida con el tiquete de ingreso) | Ninguno | El re-test crea un depósito y una OC y saca el mismo camión con su tiquete de ingreso. |
| DEF-F8-004 | BA00027 / OC00021–22 / **2026S00007**–00008 | **2026S00001** (levante QA-LEV-F11-001) | El re-test registra un segundo levante, emite otra guía y reimprime S00001: debe conservar QA-LEV-F11-001. |
| DEF-F8-008 | OC00020 | 2026OC00001 | Ya pasó a InProgress al iniciar la salida (visto en S0). |
| DEF-F10-001, DEF-F10-002 | QAE-SIIGO-001 (pago parcial) | **QA-SIIGO-F11-0001** (pendiente 246.670,28) | Doble envío y fallo del pago. |
| DEF-F10-003 | QAE-SIIGO-003 | QA-SIIGO-F11-0003 (Paid) | Un pago sobre una factura pagada da un error de negocio. |
| DEF-F9-003 | INSP00008 / QAF901 | Ninguno | El re-test crea su ingreso y recepción. |

---

## Sesión S1 (2026-10-05, 17:40–18:25 hora Colombia) — datos creados o modificados

> Build: FE `ae36cb4` (código `4074c63`) · BE `c56cc86` (incluye la corrección de DEF-F11-001; el API se reinició a las 17:40 sobre ese commit). API en la pestaña de terminal «wms-api (QA F11 S1)». Método igual que S0 (API con el rol dueño de cada paso) más pantalla para Vigilancia, Bodega (recepción directa), Báscula (reingreso), Facturación (override) y navegación por rol.

### Usuarios, terceros, convenios y catálogos
| Dato | Detalle | Para |
|---|---|---|
| Usuario `qa_cambio` | Warehouse, activo, contraseña restablecida por Admin y nombre «QA Cambio Auditoria Editado» | DEF-F7-001 |
| QA F11 Tercero CE SAS | NIT 900100111, CUSTOMER, creado por `c_exterior` · `440518a6-b261-42b8-956c-81389cf5ad0b` | DEF-F9-001 |
| Convenio QA-F11-FAC | De QA F11 Tercero CE SAS, **Draft**, creado por `facturacion`; servicios BASCULA FIXED 20.000 (desactivado) y ALMACENAMIENTO IMP PERCENTAGE_OF_VALUE 0,3 % / mín. 150.000 / umbral 50.000.000 | DEF-F9-001, REG-004 |
| QA Cliente REG F11 SAS | NIT 900100121, CUSTOMER, con contacto «Rita QA» y cuenta Bancolombia · `b776f377-d22f-4c7f-9d5f-44d0260d728c` | REG-003 |
| Motivo «QA Motivo pesaje F11» | requiere pesaje, creado por Admin · `4a3345f2-57cd-47c5-b413-021033719ff1` | DEF-F9-001 |
| Precio BASCULA | Nuevo precio 24.000 vigente desde 2026-10-05 (el anterior quedó inactivo; mismo valor) | REG-004 |
| Vehículos | AA102 y QAB20 (creados por Vigilancia desde la pantalla), QAZ902 (**inactivo**), QAZ903 (creado por CE), QAE101, QAE102, QAD101, QAM101–QAM103, QAF101–QAF103, QAS101, QAR101 | |
| Conductor | Carlos QA Conductor CE, CC 1000000903 (creado por CE) | DEF-F9-001 |

### Depósitos, órdenes y guías
| Número | Modalidad · cliente | Estado final | Uso |
|---|---|---|---|
| 2026BA00003 | IMP · Uno · COP 200.000.000 · QA-CP-F11-S1-B · 3 camiones (QAB201 60→58 contado, QAA101 40, QAA102 20 tardío) | Confirmed, ingreso **cerrado**, stock 120, sin levante; factura `23dac727` Draft **595.000** (override desde la pantalla) | DEF-F3-001, CHG-09 crit. 3, REG-011, REG-014, DEF-F6-004 |
| 2026BA00004 | IMP · Uno · QA-CP-F11-S1-DESC (QAA103) | **Cancelled** (operación descartada) | DEF-F3-004 |
| 2026BA00005 | IMP · Uno · USD 30.000 · QA-CP-F11-S1-A (QAE101) | **Closed** (despachado 100 con 2026OC00002 / **2026S00002**) | E2E-01 (REG-029) |
| 2026BA00006 | IMP · Multirol · PER_UOM 110 bultos · semanal | Confirmed, stock 110; períodos 05/10–12/10 (Closed, factura `9233bb32` Draft **8.000** por override) y 13/10–20/10 (Open, factura `ca7ab3b4` Draft 196.350) | DEF-F6-002, DEF-F6-003, REG-021 |
| 2026BA00007 | IMP · Mora · QA-CP-F11-S1-M (QAM101) | **Closed** (cargado 50 con 2026OC00003); factura **QA-SIIGO-F11-S1-0002** Overdue 89.250 | REG-025 |
| 2026BA00008 | IMP · Uno · QA-CP-F11-S1-R (QAR101) | Draft, recibido 30 | REG-010 |
| 2026INSP00002 | INSP · Mora · COP 5.000.000 (QAM102) | Confirmed; factura `e894f3ef` Draft **$0** sin N.º | DEF-F6-001 crit. 2, DEF-F11-003 |
| 2026INSP00003 | INSP · Mora · recepción sin báscula de QAF101 | Draft, stock 5 | REG-025 (operación re-habilitada) |
| 2026INSP00004 | INSP · Uno · recepción directa **desde la pantalla** de QAB204 | Confirmed (CE completó fecha, valor y manifiesto); factura $0 | DEF-F4-002 |
| 2026INSP00001 (S0) | INSP · Uno | **Confirmed** en S1; factura `eeb133f1` Draft $0 con N.º **QA-SIIGO-F11-S1-ZERO** (asignado: es el defecto DEF-F11-003) | DEF-F6-001 |
| 2026BA00001 (S0) | | Período 05/10–05/11 **Closed** por cierre manual; nuevo 06/11–06/12 (factura `f6db57ba` Draft **95.000** por override) | DEF-F6-002, DEF-F6-004 |
| 2026BA00002 (S0) | tanquero QAT001 | Recepción **Completed**, QAT001 InWarehouse, ciclo Complete; QAB202 salió | DEF-F4-001 |
| 2026OC00002 | BA00005 · QAE102 | Dispatched; guía **2026S00002** (Import, saldos 100/100/100/0) | E2E-01 |
| 2026OC00003 | BA00007 · Mora · QAM101 | **Loaded**, sin guía (Mora Blocked); QAM101 con ciclo de salida **FirstWeightCaptured** (2026T00022) e ingreso **abierto** | REG-025 bloqueo de guía; dato para DEF-F5-014 / CHG-33 en S2 (no registrar su salida) |

### Báscula
- Tiquetes 2026T00011 a 2026T00022 (sin saltos desde T00001).
- Solo báscula: QAA103 (T00014, un pesaje, Paid), QAS101 (T00015, dos pesajes, por facturar → **QA-SIIGO-F11-S1-0003** Paid), QAM103 (T00021, Mora tras el desbloqueo).
- Montacargas: Tractomula 90.000 sin IVA y 100.001 + IVA 19.000,19 (servicio de QAE101); Sencillo 45.000 a Mora (tarifa base, tras el desbloqueo).

### Facturas y pagos
| N.º | Estado | Nota |
|---|---|---|
| QA-SIIGO-F11-S1-0001 | Paid 298.002,17 | Almacenamiento BA00005; pagos 100.000 + 198.002,17 |
| QA-SIIGO-F11-S1-0002 | **Overdue** 89.250 | Almacenamiento BA00007 (Mora), vencida por la palanca → Mora **Blocked** |
| QA-SIIGO-F11-S1-0003 | Paid 28.560 | BASCULA por facturar (Consolidado), aprobada 05/10 → vence 20/10 |
| QA-SIIGO-F11-0010 (S0) | **Paid** | Pago total 28.560 en S1 (desbloqueó a Mora en la misma operación) |
| QA-SIIGO-F11-0011 (S0) | **Overdue** (saldo 18.560) | Palanca S1 → Multirol **Blocked** |
| QA-SIIGO-F11-0001 (S0) | **Overdue** (saldo 246.670,28) | Palanca S1 → Uno **OverdueWarning** |

### Estado financiero al cierre de S1
QA Cliente Mora **Blocked** (89.250) · QA Multirol **Blocked** (18.560) · QA Cliente Uno **OverdueWarning** (246.670,28; sin límite, nunca se bloquea) · los demás Active.

### Ingresos abiertos al cierre de S1
- **QAF103** «Solo bodega» (sin recepción): para re-tests de S2 (p. ej. DEF-F9-003, recepción con autor del cuerpo).
- **QAM101** «Cargue importación» con ciclo de salida abierto, esperando la guía de 2026OC00003: **no registrar su salida** antes del re-test de DEF-F5-014 / CHG-33.

### Palancas y reinicios
| Hora | Acción |
|---|---|
| 17:40 | Reinicio del API sobre BE `c56cc86` (el proceso de S0 era anterior a ese commit). |
| 18:00 | Palanca `resultados/f11_palanca_s1.sql` (solo base local): vencimiento −2 días en QA-SIIGO-F11-0011, QA-SIIGO-F11-0001 y QA-SIIGO-F11-S1-0002, y en los Borradores `568d8ac9` (BASCULA por facturar, Consolidado) y `9457d5fe` (MONTACARGAS por facturar, Uno). Reinicio del API → una corrida de los jobs. |
| 18:19 | API detenido y reiniciado a propósito para la prueba de CHG-86 (franja «Sin conexión…»). |

### Equivalencias usadas en S1
| Ficha | Dato de la campaña anterior | Dato usado |
|---|---|---|
| DEF-F2-001 | QAA102/AA102, QAB201/QAB20 | Mismos (AA102 y QAB20 creados en S1) |
| DEF-F3-004 | QAC402 / 2026BA00003 | QAA103 / 2026BA00004 |
| DEF-F4-001 | QAB202 / 2026BA00005 / QAT001 | QAB202 / **2026BA00002** / QAT001 |
| DEF-F4-002 | QAB204 / INSP00002–03 | QAB204 / **2026INSP00004** |
| DEF-F6-002 | BA00002 (mensual), BA00013, BA00028 (PER_UOM 110) | BA00001 (mensual) y **BA00006** (semanal, PER_UOM 110) |
| DEF-F6-003 | BA00013 cantidad 6 | BA00006 cantidad 110 |
| DEF-F6-004 | EXP00001 184.000 | BA00003 606.900 (pantalla) y BA00001 renovación (API, cantidad 1) |
| DEF-F6-005 | Borrador por facturar del Consolidado 57.120 | QAS101 por facturar al Consolidado 28.560 |
| DEF-F6-006 | QA-SIIGO-0011 (Uno, parcial), Mora 17.850 | QA-SIIGO-F11-0001 (Uno, parcial), QA-SIIGO-F11-0011 (Multirol, parcial), QA-SIIGO-F11-S1-0002 (Mora, sin pagos) |
| DEF-F7-001 | `qa_cambio` | `qa_cambio` (creado en S1) |

---

## Sesión S2 (2026-10-05, 20:15–21:05 hora Colombia) — datos creados o modificados

> Build: FE `15a5028` (código `5bab469`) · BE `214f5f6`. API reiniciado al empezar sobre BE `214f5f6` (pestaña de terminal «wms-api (QA F11 S2)», `dotnet run --launch-profile http`) y frontend en la vista previa `wms-dev`. Método: API con el rol dueño de cada paso más pantalla para Báscula, Bodega (recepción directa y cargue), Comercio Exterior, Facturación y navegación por rol. SQL solo de lectura; no se ejecutó ninguna palanca.

### Usuarios, terceros, catálogos y tarifas
| Dato | Detalle | Para |
|---|---|---|
| `qa_cambio` | Contraseña restablecida por Admin y cambiada a la del README (dos veces) | DEF-F1-002, DEF-F11-001 |
| `qa_inactivo` | Reactivado y desactivado dos veces; queda **inactivo** | DEF-F1-009 |
| `j_coral` | Se le quitó y devolvió el rol Facturación; queda Billing + ForeignTrade | DEF-F1-009 |
| Conductor Pedro QA (`28c2adbd…`) | **Reescrito por báscula** a «Luis QA Nuevo Ecuador» y luego a «Mario QA Salida Nuevo» (DEF-F11-008); **restaurado por Admin** con `PATCH drivers/{id}` a «Pedro QA Conductor Colombia · CC 1000000001 · 3002000001» | DEF-F3-008, DEF-F11-008 |
| Tercero «QA F11 Tipo NIT Mayusculas» | NIT 900199904, CUSTOMER, `2851c3c1…` (creado con `idType` «NIT») | DEF-F11-002 |
| Producto «QA F11 Producto S2» | SKU QA-SKU-F11-S2, unidad Kilogramo (creado con Saco), `a25d5f85…` | DEF-F1-001 |
| Tarifa base ALMACENAMIENTO · QA Cebolla · IMP · perecedero | PER_UOM 1.900, `126b8a07…`, **desactivada** | DEF-F1-003 |
| QA-CONV-001 · ALMACENAMIENTO · QA Cebolla · IMP · perecedero | PER_UOM 1.650, `123fe077…`, **desactivado** | DEF-F6-012 |
| QA-CONV-001 · ALMACENAMIENTO · QA Aceite · IMP · PER_CARGO_UNIT | rate 70.000, TANQUERO, mínimo por unidad 100.000 (IVA incluido), `2b9283a8…`, **activo** | DEF-F6-007 |
| QA-F11-FAC · ALMACENAMIENTO · QA Repuestos · IMP · PERCENTAGE_OF_VALUE 100 % | `5841bf82…`, **desactivado**; el servicio genérico volvió a 0,3 % | DEF-F1-004 |
| Mínimo IMP de ALMACENAMIENTO | 184.000; pasó a «IVA incluido» y volvió a **Neto** | DEF-F6-021 |

### Vehículos e ingresos nuevos (todos con salida salvo los indicados)
QAG201, QAG202 (Sencillo → DobleTroque · Ecuador · QA Compañía Ñandú), QAG601 (Turbo · Ñandú), QAG602 (salió sin servicio), QAG701, QAG703 (**sin salida**, Solo báscula descartado), QAG801, QAG802, QAG901 y QAG902 (**sin salida**, ciclo completo), QAH101, QAH102. QAF103 (S1) quedó **sin salida** tras su recepción directa.

### Depósitos, órdenes y guías
| Número | Modalidad · cliente | Estado final | Uso |
|---|---|---|---|
| 2026BA00009 | IMP · Uno · QA-CP-F11-S2-IDEM · QAG201 (6) | Draft, recibido 6 | DEF-F3-002, DEF-F4-003, DEF-F3-005 |
| 2026BA00010 | IMP · Consolidado · QA-CP-F11-S2-ETQ · QAG801 (40) | Confirmed, ingreso cerrado, levante QA-LEV-F11-S2-ETQ (40), stock 10 | DEF-F8-003, DEF-F8-002 |
| 2026BA00011 / BA00012 | IMP · Consolidado · QA Repuestos 10 · COP 10.000.000 (QAG901 / QAG902) | Confirmed; líneas de mínimo en la factura consolidada de Consolidado (`15428832…`, Draft) | DEF-F6-021 |
| 2026BA00013 / BA00014 | IMP · Uno · QA-CP-F11-S2-UI (QAH101, 6) y QA-CP-F11-S2-MUL (adicional, 4; cliente asignado por CE) | Draft, recibidos | DEF-F3-006/007/003/011, DEF-F11-009 |
| 2026BA00002 (S0) | tanquero QAT001 | **Confirmed** en S2; factura `20451d53` Draft 100.000 (mínimo por unidad) | DEF-F6-007 |
| 2026BA00008 (S1) | IMP · Uno | Draft; QA Cebolla 31 (corrección CE), valor USD 25.000 | DEF-F5-002, DEF-F5-001 |
| 2026BA00001 (S0) | | Levante QA-LEV-F11-S2-002 (30); stock 50 | DEF-F8-004, DEF-F5-004 |
| 2026EXP00001 (S0) | | **Closed** (despachado 50 con 2026OC00005 / 2026S00004) | DEF-F4-006 |
| 2026INSP00001 (S0) | | Ajuste CE-7 40 → 39 | DEF-F5-002 |
| 2026INSP00005 | INSP · Uno · recepción directa de QAF103 desde la pantalla (QA Repuestos 8) | Draft, sin período ni factura | DEF-F11-005, DEF-F10-001, DEF-F8-005 |
| 2026OC00004 | BA00001 · 20 · QAG601 | Dispatched, guía **2026S00003** (Importador) | cadena A |
| 2026OC00005 | EXP00001 · 50 · QAG701 | Dispatched, guía **2026S00004** (Export) | cadena B |
| 2026OC00006 | INSP00004 · 2 · QAG702 | **Cancelled** | DEF-F3-012 |
| 2026OC00007 | BA00010 · 20 · QAG801 (salida con tiquete de ingreso) | Dispatched, guía **2026S00005** | DEF-F8-003 |
| 2026OC00008 | BA00001 10 + BA00010 10 · QAG802 | Dispatched, guía **2026S00006** (multicliente, firma Conductor) | DEF-F8-002 |
| 2026OC00009 | BA00010 · 5 · QAA103 (creada desde la pantalla) | **Cancelled** | DEF-F10-001 |

### Báscula
Tiquetes 2026T00024 a 2026T00033. Ciclo multidepósito de QAH101: bruto 18.000 → intermedio 16.000 → tara 12.000 (T00032 y T00033). Ciclo 2026T00023 (S1, QAR101): pesaje 1 corregido de 25.000 a 25.500; la tara volvió a 16.000 tras las pruebas (neto 9.500).

### Facturas y pagos
| N.º / id | Estado | Nota |
|---|---|---|
| QA-SIIGO-F11-S2-0001 (`23dac727`, BA00003) | **PartiallyPaid** 595.000 · pagado 7.000 | Tres pagos Verified: 5.000 (autor desde el token), 1.000 con comprobante PDF por API y 1.000 con comprobante desde la pantalla (doble clic) |
| QA-SIIGO-F11-S2-0002 (`f6db57ba`, BA00001 renovación) | Draft con N.º | Enter doble |
| QA-SIIGO-F11-S2-0100 (`4a5fd48c`, BASCULA contado T00001) | Paid con N.º | DEF-F6-022 |
| `e894f3ef` (INSP00002, $0) | **Approved** sin N.º | DEF-F11-003 |
| `9457d5fe` (MONTACARGAS, Uno) | **Cancelled** | anulación sin pagos |
| GUIA_SALIDA | 30.000 (S00003), 35.000 (S00005), 30.000 + 35.000 (S00006) | contado |

### Estado financiero al cierre de S2
Sin cambios frente a S1: Mora **Blocked**, Multirol **Blocked**, Uno **OverdueWarning**. QAM101/2026OC00003 (Mora) sigue con la salida abierta y sin guía.

---

## Sesión S3 (2026-10-05 23:03 – 2026-10-06 00:05 hora Colombia) — datos creados o modificados

> Build: FE `d9783af` (código `20bb089`) · BE `44bd80a` (incluye `fce70d5` y la migración `AddEntryLogServiceDiscardedAt`). Primera parte (REG-024 y SMTP caído) con el API arrancado por QA con `DianTrm__BaseUrl=http://127.0.0.1:9`, `Email__SmtpHost=127.0.0.1` y `Email__SmtpPort=9` (variables del proceso, sin tocar archivos); el usuario detuvo esa instancia y el resto de la sesión corrió con el API normal (pestañas de terminal «wms-api (QA F11 S3)»). Método: API con el rol dueño de cada paso y pantalla (vista previa `wms-dev`) para báscula, Bodega, Comercio Exterior, Facturación, Admin y navegación por rol.

### Palanca y reinicios
| Hora | Acción |
|---|---|
| 23:03 | API sin DIAN ni SMTP (REG-024, DEF-F5-003). |
| 23:11 | API normal (pedido del usuario). |
| 23:28 | Palanca `resultados/f11_palanca_s3.sql` (solo base local): vencimiento a 2 días en QA-SIIGO-F11-S3-TRM y QA-SIIGO-F11-0002 (DEF-F6-018). Reinicios del API a las 23:28 y 23:30 para dos corridas más del job de vencimientos. |
| 23:52–23:56 | API detenido y reiniciado a propósito (CHG-86, DEF-F10-004). |

### Conductores y vehículos
| Dato | Detalle |
|---|---|
| Conductor «Luis QA Nuevo S3 Corregido», Pasaporte 1700000931 | Creado por báscula en el Solo báscula de QAJ202 (DEF-F11-008); su apellido y teléfono se corrigieron con el mismo documento (QAJ203). |
| Conductor «Mario QA Salida S3», CC 1000000941 | Creado por báscula en la salida de QAJ302. |
| Pedro QA y Jorge QA | **Sin cambios** (el ingreso de QAJ201 quedó con Jorge QA). |
| Vehículos nuevos | QAJ101, QAJ201–QAJ204, QAJ301, QAJ302, QAJ401, QAJ402, QAJ501, QAJ601, QAJ701, QAJ801, QAJ901–QAJ903 (Tractomula, QA Transportes SAS). |

### Ingresos
Con salida: QAJ302, QAJ501, QAJ701. **Sin salida**: QAJ101 (ingreso del 03/10 09:30, 2026BA00015), QAJ201 (2026BA00016 registrado, sin cobro), QAJ202/QAJ203/QAJ204 (Solo báscula iniciados, sin cobro; QAJ204 descartado y vuelto a registrar para R-TRZ), QAJ301, QAJ401, QAJ402, QAJ601 (ciclo con primer peso, recepción completada), QAJ801 (salida descartada), QAJ901 («Solo bodega»), QAJ902 (sin registro), QAJ903 («Solo báscula», sin iniciar).

### Depósitos, órdenes y guías
| Número | Detalle | Estado final |
|---|---|---|
| 2026BA00015 | IMP · Uno · USD 40.000 · QAJ101 (ingreso 03/10) · TRM **manual** 4.100 (primero 4.000) | Confirmed; factura `08470a76` **QA-SIIGO-F11-S3-TRM** PartiallyPaid 497.658 (pago 1.000 por API) |
| 2026BA00016 | IMP · Uno · USD 50.000 · QAJ201 (conductor Jorge QA) | Confirmed; factura **QA-SIIGO-F11-S3-0016** Cancelled → refacturada `7f48699a` Draft 496.670,28 |
| 2026BA00017 | IMP · Uno · QAJ401 · 8 QA Cebolla | Draft, ciclo 2026T00037 completo (tara corregida 18.000 → 17.500) |
| 2026BA00018 / 2026BA00019 | Multidepósito de QAJ402: principal (Uno, MULB, 8) y adicional **sin cliente** (MULX, 44) | Draft; tiquetes 2026T00038/39; factura en cero `1a4a21a0` a Consumidor final |
| 2026BA00020 | IMP · Uno · QAJ601 · QA Cebolla 2 + QA Aceite 7 · sin valor ni moneda · recepción con QA Aceite sin contar | Draft |
| 2026EXP00002 | EXP · Uno · COP 10.000.000 · QAJ301 · 20 QA Cebolla | **Closed** (despachado con 2026OC00010 / **2026S00007**) |
| 2026BA00013 (S2) | CE-7 6 → 5 y confirmado; luego **anulado** «Prueba QA S3» | Cancelled; factura `86f2dad7` Cancelled |
| 2026BA00001 (S0) | Validado (plantilla 38.000/160); período 06/11–06/12 cerrado a mano → nuevo 07/12–07/01 (factura `9947b037` Draft) | Confirmed |
| 2026BA00002 (S0) | Factura `20451d53` anulada y refacturada → `a5894ced` Draft 100.000 | Confirmed |
| 2026INSP00001 (S0) | CE-7 39 → 38 con SMTP caído; 2 QA Repuestos despachados con 2026OC00011 | Confirmed, stock 36 |
| 2026OC00010 | EXP · QAJ302 · 20 | Dispatched (R-EXP) |
| 2026OC00011 | INSP · QAJ701 · 2 | Dispatched sin guía |
| 2026OC00012 | IMP · BA00001 · QAJ801 · 5 | **Reverted** (cargue de prueba revertido) |

### Báscula
Tiquetes 2026T00035 a 2026T00041. Montacargas de QAJ601: Tractomula 100 → 105 h, $ 90.000 sin IVA, pago inmediato (factura `ae62e96e`).

### Configuración y catálogos (todos restaurados)
QA Cliente Mora: límite quitado (API y pantalla) y restaurado a 1.000 (Blocked). QA Cliente Consolidado: preferencia PerWeighbridgeCycle por API y restaurada a Consolidated. Embalaje QA-CAJA, unidad «Saco», tarifa Turbo y COMPANY_EMAIL cambiados y restaurados. Rol Facturación asignado y retirado a qa_cambio. Servicio PER_CARGO_UNIT de QA-CONV-001: rate 71.000 y restaurado a 70.000. Levante QA-LEV-F11-001: observación «QA F11 S3 PATCH sin fobUsd». Manifiesto de 2026BA00004 (anulado) escrito por el defecto DEF-F11-012 y vuelto a vacío.

### Estado financiero al cierre de S3
Mora **Blocked**, Multirol **Blocked**, Uno **OverdueWarning**, Consolidado Active.

### Equivalencias usadas en S3
| Ficha | Dato de la campaña anterior | Dato usado |
|---|---|---|
| DEF-F3-010 | 2026BA00012 | QA-CP-F11-001 (2026BA00001, ingreso cerrado en S0) con QAJ902 |
| DEF-F4-010 | Cebolla 2 + Aceite 7 | QAJ601 / 2026BA00020 |
| DEF-F4-013, 016, 017 | QAB204 | QAJ601 (servicio activo) |
| DEF-F5-008 | 2026BA00012 | 2026BA00001 (dos camiones) |
| DEF-F7-003 | 2026OC00017 | 2026OC00011 (inspección, QAJ701) |
| DEF-F7-007 | 2026BA00004 refacturada | 2026BA00002 y 2026BA00016 |
| DEF-F8-006 | 2026BA00027 | 2026BA00013 (6 → 5) |
| DEF-F8-007 | 2026BA00031 | 2026BA00013 |
| DEF-F8-008 | 2026OC00020 | 2026OC00012 |

## Sesión S4 (2026-10-06 08:58 – 10:00 hora Colombia) — datos creados o modificados

> Build: FE `e41decf` · BE `ea14548`, sin migraciones nuevas. Al empezar no había API ni frontend corriendo: QA los arrancó sobre estos commits (pestaña de terminal «wms-api (QA F11 S4)», `dotnet run --launch-profile http`; vista previa `wms-dev`). Método: API con el rol dueño de cada paso y pantalla para lo que el caso pide ver. **Sin palancas.** SQL solo de lectura. Bloque STG diferido a staging (decisión del usuario, 2026-10-06).

### Vehículos e ingresos (todos con Pedro QA, salvo QAK701 sin conductor)
| Dato | Detalle |
|---|---|
| Vehículos nuevos | QAK402, QAK501–QAK504, QAK592 (creado por la corrección de placa de QAK502, que quedó inactivo), QAK601–QAK612 y QAK701 (creado desde la pantalla de Vigilancia, sin tipo ni transportadora). |
| Con salida | QAK501 (F2-SAL-003). |
| Sin salida | QAK402, QAK503, QAK592, QAK601–QAK612, QAK701 (Registered) y **QAK504 (Completed y fuera de la cola: DEF-F11-016)**. |

### Depósitos, órdenes y guías
| Número | Detalle | Estado final |
|---|---|---|
| 2026BA00021 / 2026BA00022 | Multidepósito de QAK402: principal (Uno, QA-CP-F11-S4-MULB, 8 QA Cebolla) y adicional sin cliente (QA-CP-F11-S4-MULX, 4) con factura en cero a Consumidor final; tiquetes 2026T00042/43; recepciones completadas (BA00022 con diferencia 4/3) | BA00021 **Confirmed** (USD 30.000, TRM DIAN 3.209,78, levante QA-LEV-S4-01 de 8, factura `537ef935` Draft 292.202,32); BA00022 Draft |
| 2026BA00023 | IMP sin cliente, QA-CP-F11-S4-REI: QAK601 (5) y QAK607 (10), stock 15; cobro de QAK601 al conductor por 30.000; tiquete 2026T00044 (primer peso corregido 25.000 → 26.000); montacargas Tractomula 100 → 101,5 (80.000, persona no registrada) | Draft |
| 2026BA00024 | IMP QA-CP-F11-S4-UCA, unidades de carga: Tanquero QAT601, QA Aceite 30.000 (QAK606) | Draft |
| 2026BA00025 | IMP QA-CP-F11-S4-DESC (QAK602), descartado desde «Recuperar operaciones» | Cancelled (servicio Discarded; stock 0 sin movimiento de salida: observación) |
| 2026BA00026 | Recepción directa de QAK612 («Solo bodega»), QA-CP-F11-S4-RSB, 20 QA Cebolla | Draft |
| 2026EXP00003 | EXP QA-CP-F11-S4-EXP (QAK603), COP 20.000.000; 10 QA Cebolla despachados con 2026OC00014 (6, QAK609) y 2026OC00015 (4, QAK610) | **Closed**; factura de almacenamiento 178.500 **anulada** en F6-ACC-011 |
| 2026EXP00004 | EXP sin exportador (QAK608) para F5-CNF-003 | Cancelled (StorageCancellation) |
| 2026INSP00006 | INSP QA-CP-F11-S4-INSP (QAK604), USD 40.000, un solo pesaje (2026T00045), confirmado sin recepción | Confirmed (TRM DIAN 3.209,78; factura $0) |
| 2026OC00013 | EXP · QAK609 · 10 | Cancelled (F5-OC-016) |
| 2026OC00014 / 2026OC00015 | EXP · QAK609 (6 de 10) / QAK610 (4) | Dispatched; guías automáticas **2026S00008** y **2026S00009**; tiquetes 2026T00047 y 2026T00048 |
| 2026OC00016 | IMP · BA00021 · QAK611 · 2 | **Reverted**; guía **2026S00010** anulada (factura GUIA_SALIDA `3aeb6ade` Paid 35.700 queda para revisión); ciclo de salida 2026T00049 anulado |

### Báscula
- Solo báscula de QAK605 (2026T00046, QA Cliente Uno, 29.750) **anulado** en F3-COR-007; la factura sigue Paid.
- Tiquetes de S4: 2026T00042 a 2026T00049.

### Facturas, pagos y estado financiero
| Dato | Detalle |
|---|---|
| Factura consolidada `15428832` (QA Cliente Consolidado: 2026BA00010/11/12) | N.º **QA-SIIGO-F11-S4-0010**, **Approved**. Tras dos CE-7 en 2026BA00010 (40 → 41 → 40) quedó en 420.810: la línea de BA00010 cobra 10 en vez de 40 (**DEF-F11-017**). |
| Pago con comprobante (REG-023) | 1.000 por transferencia a QA-SIIGO-F11-S2-0001 (2026BA00003); pagado 7.000 → 8.000. |
| Pago de la deuda de QA Cliente Mora | 89.250 a QA-SIIGO-F11-S1-0002 → **QA Cliente Mora pasa a Active** (F6-CAR-008). Para volver a probar la mora hace falta otra factura vencida y la palanca. |
| Comprobantes sueltos | Dos PDF de 72 KB en `uploads/payment-vouchers` (DEF-F11-015 y REG-023); el primero sin pago asociado. |
| Estado financiero al cierre | QA Cliente Uno OverdueWarning 246.670,28 · QA Cliente Mora Active 0 · QA Cliente Consolidado Active 0. |

### Restaurado tras las pruebas
- Cantidades de 2026BA00020 (QA Aceite 7, QA Cebolla 2).
- Manifiesto de 2026BA00003 (vacío).
- Exportador de 2026EXP00003: el PUT de terceros agregó también QA Transportes SAS como transportadora documental.
- Recibido de 2026BA00010 en 40. La factura no se restauró: ver DEF-F11-017.

### Equivalencias usadas en S4
| Caso pedido | Dato usado |
|---|---|
| DEF-F11-010 (F3-MUL-002) | QAK402 → 2026BA00021 + 2026BA00022 (en S3: QAJ402 → 2026BA00018/19) |
| DEF-F11-012 | 2026BA00004 y 2026BA00013 (anulados), control 2026BA00003 |
| DEF-F11-013 | 2026EXP00001, 2026INSP00001 y 2026INSP00005 (Borrador) |
| DEF-F11-014 | 2026BA00020 (QA Cebolla contada 2; QA Aceite declarada y no contada) |

## Sesión S5 (2026-10-06 10:50 – 11:57 hora Colombia) — datos creados o modificados

> Build: FE `bd729e5` · BE `00d6ac3`, sin migraciones nuevas. Al empezar no había API ni frontend corriendo. QA los arrancó con autorización del usuario (pestaña de terminal «wms-api (QA F11 S5)», `dotnet run --launch-profile http`, y vista previa `wms-dev`). El API se reinició una vez, a las 11:51, también con autorización, para correr los jobs. Método: API con el rol dueño de cada paso y pantalla para lo que el caso pide ver. Palanca `f11_palanca_s5.sql`, solo base local.

### Vehículos, conductores, productos y catálogos
| Dato | Detalle |
|---|---|
| Vehículos nuevos | QAL101–QAL108, QAL131–QAL139, QAL141, QAL151–QAL155, QAL162–QAL167, QAL171–QAL172, QAL181–QAL182, QAL191–QAL196 y QAL201, este último corregido a **QAL291** en la prueba de DEF-F11-016. QAL151 fue creado por Vigilancia con tipo y transportadora. QAL152–QAL154 se crearon por API sin datos; QAL152 quedó con QA Compañía Ñandú · Ecuador · Sencillo y QAL153 con Turbo. |
| Conductor nuevo | Rosa · QA Nueva S5 · CC 1000000951 · Colombia (creado desde la pantalla de Báscula, F3-CAM-005) |
| Producto nuevo | «QA MERCANCÍA VARIA» (SKU BAS-7C80E8BD), creado por la línea libre de báscula (F3-REG-011) |
| Convenio | **QA-CONV-REG-S5** de QA Cliente REG F11 SAS (activo) con BASCULA FIXED 25.000 IVA incluido, ALMACENAMIENTO IMP · QA Repuestos · PERCENTAGE_OF_VALUE_PRORATED 1 % y ALMACENAMIENTO IMP · QA Aceite · PER_VEHICLE 50.000. **Los tres servicios quedaron desactivados.** |
| QA-CONV-001 | Servicio MONTACARGAS desactivado y reactivado (F6-TAR-005). |

### Ingresos abiertos al cierre de S5
QAL131–QAL138, QAL151–QAL155, QAL162, QAL171, QAL172, QAL191, QAL193–QAL195.
- QAL101, QAL102–QAL108, QAL139, QAL141, QAL163, QAL181, QAL182, QAL192, QAL196 y QAL291 tienen salida.
- **QAK504** sigue sin salida y aparece en la cola (DEF-F11-016 verificado).

### Depósitos, órdenes y guías
| Número | Detalle | Estado final |
|---|---|---|
| 2026BA00027 | REG F11 · QA-CP-F11-S5-R17 · QAL101 (40) + QAL103 tardío (5) · tarifa base PER_UOM | **Closed** (2026OC00017 por 30 con QAL102 · guía 2026S00011; 2026OC00018 por 15 con QAL104 · 2026S00012); factura **QA-SIIGO-F11-S5-0001** Sent 80.325 (45 bultos) |
| 2026BA00028 | REG F11 · QA Cebolla 20 + QA Repuestos 10 (QAL105) | Confirmed; Cebolla agotada (2026OC00019 · 2026S00013); renovado a mano: período 07/11–07/12 solo de Repuestos (factura Draft 218.960) |
| 2026BA00029 | Uno · COP 100.000.000 · QA Cebolla 50 (QAL107) · levantes R21 (20) + R21B (10) · manifiesto DIAN QA-DIAN-F11-S5-29 | Confirmed, stock 23 (2026OC00020 20 · 2026S00014; 2026OC00021 5 · 2026S00015; 2026OC00023 3 · 2026S00017); factura Draft 303.450 |
| 2026BA00030 | Uno · QA-CP-F11-S5-F3A sin tipo de documento (API) | **Cancelled** (descartado) |
| 2026BA00031 | Uno · QA-CP-F11-S5-F3A · QAL131 (primer pesaje Tara) + QAL132 + QAL133 (QA Aceite 10, primer peso 15.000,56) · fecha de ingreso −20 min | Draft; terceros con 2 clientes y 2 importadores agregados por el API (observación F3-MCA-003) |
| 2026BA00032 / 2026BA00033 | Uno · QA-CP-F11-S5-AMB con fechas del documento distintas (F3-MCA-006) | 00032 **Cancelled** (F5-ANU-003, 2026OC00027 cancelada, factura anulada); 00033 Confirmed, stock 4 (pesaje de QAL136 anulado en F6-REC-007, levante QA-LEV-F11-S5-COR6 en 4), 2026OC00026 **Pending** (3), factura refacturada `fc4ae1d9` Draft 184.000 (la original quedó anulada) |
| 2026BA00034 | Uno · unidades de carga, tanquero QAT137 1.000 L (QAL137) | Confirmed; factura Draft 100.000 (mínimo por unidad) |
| 2026BA00035 | Sin cliente · QA-CP-F11-S5-UI2 · QAL152 (10) + QAL153 (5), registrados desde la pantalla | Draft, recibido 14 (recepción de QAL152 con 9 contados + CE-7 15 → 14) |
| 2026BA00036 / 2026BA00039 | QA Cliente Consolidado · QAL162 (12) / QAL191 (8) | 00036 Confirmed; 00039 **Cancelled** (pesaje anulado); consolidada **QA-SIIGO-F11-S5-0002** Paid 35.700 |
| 2026BA00037 / 2026BA00038 | Uno · 2 tanqueros (QAT171/172 1.500 L; QAT173/174 2.000 L) | Confirmed |
| 2026BA00040 | REG F11 · QA Aceite · 2 camiones (QAL193 + QAL194) · PER_VEHICLE | Confirmed; período 06/10–06/11 cerrado por el job y renovado 07/11–07/12 (dos facturas Draft de 119.000) |
| 2026BA00041 | REG F11 · QA Repuestos 10 · COP 10.000.000 · PRORATED | Confirmed, stock 5 (2026OC00029 · 2026S00018); 1.er período 119.000, renovación 59.500 |
| 2026EXP00005 | Uno · EXP · QA Cebolla 10 (QAL181) | Confirmed: 2026OC00028 con QAL182 (guía automática 2026S00016, **anulada**) y luego **revertida** |
| 2026OC00022, 2026OC00025 | Pruebas de orden externa y de levante | Cancelled |
| 2026OC00024 | Multicliente 2026BA00001 (5) + 2026BA00010 (4) con QAL164 | **Pending** |

### Báscula
- Tiquetes 2026T00050 a 2026T00071.
- Solo báscula: QAL139 (Consumidor final, dos pesajes) y QAL192 (REG, IVA incluido).
- Montacargas de QA Cliente Uno: Sencillo 300 → 301 h, uno a 50.000 (convenio) y otro a 45.000 (convenio inactivo), los dos pagados.

### Facturas, pagos y estado financiero
| Dato | Detalle |
|---|---|
| QA-SIIGO-F11-S4-0010 (consolidada S4) | Vuelve a 474.360 con los dos CE-7 de la Parte A. Pagos de 474.000 (transferencia QA-PAG-F11-S5-REC5) y 360 (QA-PAG-F11-S5-REST) → **Paid**. |
| QA-SIIGO-F11-S5-0001 | 2026BA00027, Sent 80.325, sin pagos. |
| QA-SIIGO-F11-S5-0002 | Consolidada de 2026BA00036/39, Paid 35.700 (QA-PAG-F11-S5-REC5B). |
| Estado financiero al cierre | QA Cliente Uno OverdueWarning 246.670,28 · QA Multirol Blocked 18.560 · QA Cliente Mora Active · QA Cliente Consolidado Active · QA Cliente REG F11 Active (sin configuración de facturación). |

### Palanca y restauración (solo base local, `f11_palanca_s5.sql`)
| Hora | Acción |
|---|---|
| 11:34 | `entry_date` de 2026BA00015 −25 días y de 2026BA00003 −35 días (abandono). Restaurado a las 11:36. La prórroga de 2026BA00015 queda registrada. |
| 11:46 | `limit_date` del período de 2026BA00040 al 04/10 y `due_date` de QA-SIIGO-F11-S4-0010 al 04/10. |
| 11:51 | Reinicio del API (autorizado). Los jobs renovaron 2026BA00040 y pasaron QA-SIIGO-F11-S4-0010 a Overdue, con QA Cliente Consolidado en OverdueWarning. Después se pagó el saldo y se repuso el vencimiento original. |

### Otros cambios sobre datos anteriores
- 2026BA00016: fecha de ingreso 06/10 00:30 y TRM DIAN 3.209,78 del 06/10; factura `7f48699a` Draft 487.003,87.
- 2026BA00006: levante QA-LEV-F11-S5-MR, registrado y retirado. Queda «SinNacionalizar», como estaba.

### Equivalencias usadas en S5
| Caso | Dato usado |
|---|---|
| DEF-F11-017 (caso de la ficha) | 2026BA00010, el mismo de S4 |
| F3 `QAA101` / `QAB201` / `QAB202` | QAL151 (con datos), QAL152/QAL153 (sin datos), QAL131–QAL133 (varios camiones), QAL137/QAL138 (unidades de carga) |
| F3-SAL `QAB205` | QAL141 con 2026OC00021 |
| F5 `QA-CP-0001` / `QA-CP-0005` | 2026BA00029 y 2026BA00033 / 2026BA00034 y 2026BA00038 |
| F6 consolidado y TRM | QA Cliente Consolidado (2026BA00036/39) y 2026BA00015 (TRM manual, factura aprobada) |

## Verificación del precio base con centavos (2026-10-08 10:42 – 10:48 hora Colombia) — datos creados o modificados

> Fuera de las sesiones S0–S5: verificación local del arreglo de `ServicePricesList.vue` (el «Precio base» no admitía centavos). API de verificación en 5282 sobre `wmsdb`, usuario `capb90`.

| Dato | Detalle |
|---|---|
| Precio de BASCULA | Nuevo precio vigente **16.806,72** desde el 08/10/2026 (`cf6100c4-d380-4872-846f-e2e7fa9b55d2`), creado desde la pantalla. El de 24.000 pasó a histórico (`valid_to` 08/10/2026). **Cambia el cobro de báscula sin convenio: ahora $20.000 con IVA.** |
| Ingreso QAL167 | Creado por API con Rosa QA Nueva S5 y motivo «Solo Bascula» (`3320d305-48d4-488c-ade7-dd3740f9c8a6`). Registro Solo báscula y cobro inmediato a Consumidor final en efectivo. Queda **en el paso «Peso», sin pesar y sin salida**. |
| Factura de QAL167 | `4cc3e6ef-4eb9-4385-9599-8968e67a33cb`, Paid: 16.806,72 + IVA 3.193,28 = **20.000,00**, sin número SIIGO. |

- No se usó QAG703 (evidencia de Solo báscula descartado) ni QA Cliente Uno SAS (tiene convenio de báscula a $29.750).
- Para volver a la tarifa anterior de báscula, crear un precio nuevo de 24.000 desde Administración › Servicios › BASCULA.
