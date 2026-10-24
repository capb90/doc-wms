# Resultado del agente AG-01 · 01-administracion-catalogos

> **Fecha:** 2026-10-23. Auditoría estática: no se ejecutaron builds, pruebas ni llamadas, no se consultó Git ni se abrieron secretos o `db_legacy/`. Código en disco ese día (según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`).

## 1. Cobertura

| Concepto | Cantidad |
| --- | ---: |
| Capacidades legacy asignadas | 98 de 98 auditadas |
| Capacidades legacy no catalogadas agregadas | 2 (`CF-LX01-01`, `CF-LX01-02`) |
| Candidatas V2 asignadas | 11 de 11 confirmadas como `SOLO_V2` |
| Capacidades V2 nuevas | 2 (`CF-V012`, `CF-V013`) |
| Filas de la matriz | 113 (100 legacy + 13 V2) |

Entregables: `01-inventario-legacy.md`, `02-flujos-legacy.md`, `03-reglas-negocio.md`, `04-trazabilidad-legacy.md`, `05-analisis-v2.md`, `06-matriz-paridad.md`, `07-matriz-paridad.csv` (114 líneas, 20 campos en todas, validado con `csv.reader`), `08-brechas.md`, `09-integraciones.md` y este archivo.

## 2. Conteos

### Paridad integral (100 filas legacy)

| Estado | Filas | De las 98 asignadas |
| --- | ---: | ---: |
| `COMPLETO_CODIGO` | 30 | 29 |
| `PARCIAL` | 20 | 20 |
| `DIFERENCIA_INTENCIONAL` | 45 | 44 |
| `NO_APLICA` (Colmotores: CF-L013…016, CF-L244) | 5 | 5 |
| `NO_IMPLEMENTADO` | 0 | 0 |
| `NO_VERIFICADO` | 0 | 0 |

Las 20 `PARCIAL`: CF-L010, 011, 012, 029, 032, 034, 035, 036, 037, 046, 047, 048, 062, 063, 086, 087, 088, 090, 092, 247.

### Por dimensión (100 filas legacy)

| Dimensión | Estados |
| --- | --- |
| Frontend V2 | `COMPLETO_CODIGO` 62 · `PARCIAL` 1 · `NO_APLICA` 37 |
| Backend V2 | `COMPLETO_CODIGO` 64 · `PARCIAL` 1 · `NO_APLICA` 35 |
| Integración | `CONECTADO_CODIGO` 65 · `NO_APLICA` 35 |
| Reglas de negocio | `COMPLETO_CODIGO` 31 · `PARCIAL` 19 · `NO_APLICA` 50 |

Filas V2 (13): frontend `COMPLETO_CODIGO` 13; backend `COMPLETO_CODIGO` 12 y `NO_APLICA` 1 (CF-V011, solo frontend); integración `CONECTADO_CODIGO` 12 y `NO_APLICA` 1.

### Validación mediante ejecución

49 filas legacy citan una ejecución previa de QA o de la migración (`Validada`): 24 `COMPLETO_CODIGO`, 14 `PARCIAL` (QA probó la función V2, no la diferencia), 11 `DIFERENCIA_INTENCIONAL`. Las otras 51 quedan `No ejecutada en esta auditoría`, con caso previsto cuando existe (F1-CIU-003/005, F1-CUA-002/003, F1-EMB-003, F1-TUC-002, F1-CON-003, F1-TER-009, F1-UBI-005).

## 3. Brechas

| Criticidad | Cantidad | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 0 | — |
| MEDIA | 1 | BR-01-001 |
| BAJA | 7 | BR-01-002 … BR-01-008 |

Las más relevantes:

1. **BR-01-001 (MEDIA):** un embalaje no se puede desactivar; el borrado solo mira los productos de depósito y deja sin embalaje, sin auditoría, a los productos del catálogo (FK `SetNull`).
2. **BR-01-006 (BAJA):** terceros, conductores y vehículos se desactivan aunque tengan registros asociados; el legacy lo impedía (error 8).
3. **BR-01-005 (BAJA):** la placa es única sin país; el legacy identificaba el vehículo por placa + país.
4. **BR-01-004 (BAJA):** datos de ficha sin destino ni decisión (DV y ciudad del cliente, sigla de la transportadora, licencia del conductor, motor/chasis/modelo del vehículo).
5. **BR-01-002 / BR-01-008 (BAJA, seguridad):** cinco catálogos legibles sin sesión (OBS-F9-001); el cambio de contraseña no pide la actual (OBS-F1-007).

Ninguna brecha tiene ficha `DEF-*`. **DEC-005:** no se encontró ningún rol que pierda una función por permisos (05-analisis-v2.md §4). **DEC-011:** quedan restos de `INTERMEDIARY`/«SIA» en `CustomsAgencyResolver` (BR-01-003).

## 4. SOLO_V2

Confirmadas: CF-V001 (JWT), CF-V002 (recuperación y cambio de contraseña), CF-V003 (usuarios y 6 roles), CF-V004 (consulta de auditoría), CF-V005 (parámetros), CF-V006 (unidades de medida), CF-V007 (tipos de unidad de carga), CF-V008 (motivos de ingreso), CF-V009 (selector de conductor), CF-V010 (terceros multirol y alta rápida), CF-V011 (inicio por rol). Nuevas: **CF-V012** (carga masiva de ciudades por CSV con simulación) y **CF-V013** (contactos y cuentas bancarias de terceros).

## 5. Contraste con el análisis anterior

### Estados de `MIGRATION_MATRIX.md` (98 capacidades)

| Estado previo | N | CONFIRMADA_EN_CODIGO | OBSOLETA | INCOMPLETA | CONTRADICHA_POR_CODIGO |
| --- | ---: | ---: | ---: | ---: | ---: |
| EXCLUIDA | 14 | 14 | — | — | — |
| CUBIERTA | 30 | 19 | — | 10 (012, 029, 034, 035, 036, 048, 062, 063, 088, 247) | 1 (244) |
| PARCIAL | 15 | 5 (025, 037, 045, 241, 248) | 3 (003, 089, 091) | 6 (010, 011, 046, 047, 086, 087) | 1 (101) |
| NO ENCONTRADA | 26 | 18 (decisión «aceptado»: 026–028, 038–044, 073–076, 093, 094, 100, 256) | 8 (005–008, 021–024: construidas) | — | — |
| COMPORTAMIENTO DIFERENTE | 3 | 2 (090, 092) | — | — | 1 (032) |
| REEMPLAZADA | 10 | 10 | — | — | — |
| **Total** | **98** | **68** | **11** | **16** | **3** |

`NO_VERIFICADA`: 0. Las tres contradicciones:

- **CF-L244:** la matriz la daba por CUBIERTA con el selector de productos; el legacy es el grupo de alias de vehículos de Colmotores (`mod_productos/selecciongrupo.php:7`), así que es `NO_APLICA`.
- **CF-L101:** la matriz decía que la relación documento–modalidad estaba «sembrada»; los 6 tipos se siembran con `OperationModalityId` nulo (`SeedDataExtensions.cs:299-370`).
- **CF-L032:** la matriz decía «borrado físico bloqueado si está en uso por productos»; solo se bloquea por productos de depósito (BR-01-001).

Las `INCOMPLETA` son filas que el análisis anterior no miró campo a campo (fichas, unicidad por país, bloqueo de bajas, lectura anónima).

### Afirmaciones de los planes y documentos

| Afirmación | Fuente | Resultado |
| --- | --- | --- |
| Catálogo de ciudades con días, CRUD Admin, borrado con 409, duplicado, importación CSV y GET para todos | plan-backend F2-06; plan-frontend F2-01 | CONFIRMADA_EN_CODIGO |
| Catálogo de cuadrillas, uso en recepción y orden, cuadrilla en la guía | plan-backend F4-10; plan-frontend F4-01 | CONFIRMADA_EN_CODIGO (el uso en flujos se vio en código; el detalle lo cierran los módulos 03 y 05) |
| Destino de la orden por catálogo y vencimiento calculado | plan-backend F2-07 | CONFIRMADA_EN_CODIGO en lo que toca a este módulo (detalle: módulo 05) |
| Maestros desde el legacy | plan-backend F6-02 | NO_VERIFICADA aquí (importadores existentes; los audita el módulo 08); resultados de la carga en `informe-fase-3.md` |
| No se construyen acceso, catálogos fijos, datos de maestros ni precarga por placa | plan-backend §A.3; plan-frontend §A.3 | CONFIRMADA_EN_CODIGO (no hay código a medias) |
| GAP-025 y GAP-026 «construir» | FUNCTIONAL_GAPS | OBSOLETA (cerradas) |
| GAP-022, GAP-023 y GAP-018 «aceptado» | FUNCTIONAL_GAPS; DECISIONES_REVISION.md §3.6–3.7 | CONFIRMADA_EN_CODIGO; GAP-023 queda INCOMPLETA porque no lista los datos de BR-01-004 |
| Escrituras de catálogos restringidas (CHG-03) | DEF-F9-001 (Verificado) | CONFIRMADA_EN_CODIGO (`WmsPolicyRoles.cs`, controladores) |
| «Toda la funcionalidad planeada está implementada» | `docs/contexto/estado.md` §1 | CONFIRMADA_EN_CODIGO para lo planeado de este módulo; las brechas son diferencias no planeadas |

## 6. Criterio aplicado e incertidumbres

- **Endurecimientos de validación** (duplicados normalizados, longitudes, 409 al desactivar un servicio con convenios, bloqueo de borrado de ciudades y cuadrillas en uso): están especificados en ítems de plan aprobados (F2-06, F4-10), que no son fuente de `DIFERENCIA_INTENCIONAL` según las instrucciones §5. Se trataron como equivalencia que conserva la función (`COMPLETO_CODIGO`) y se listan en 03-reglas-negocio.md (RN-LX01-04, 05). Si el orquestador prefiere el criterio estricto, son candidatos a una brecha documental única de criticidad BAJA.
- **Uso real del legacy:** el checkout no dice qué pantallas se usaban; algunas altas legacy no podrían funcionar (servicios, modalidades: sentencias mal armadas) y los bloqueos de error 8 no hacen `exit`.
- **Prefijos:** qué campos precargaba `campoprefijo` depende de datos (`db_legacy/`, prohibido); confianza MEDIA.
- **Cliente inactivo y facturación:** no se revisó el efecto de desactivar un cliente con convenio sobre los jobs de facturación (módulo 06; BR-01-006).
- **Tipos de identificación fijos:** 8 conductores con cédula de extranjería y 2 transportadoras no se migraron; la decisión se cumple, falta confirmar la alternativa operativa.

## 7. No analizado y por qué

- Tarifas, convenios, precios y mínimos de servicios: módulo 06.
- Ubicar, mover y liberar mercancía y ocupación de bodega (CF-L168…172): módulo 03.
- Uso detallado de ciudades y cuadrillas en órdenes, cargue y guías: módulos 03 y 05 (aquí solo la integración del catálogo).
- Importadores legacy de maestros (F6-02) y respaldos: módulo 08.
- Tablero de Trazabilidad (`pages/index.vue`): módulo 03.
- No se ejecutó ninguna prueba: los estados son de código; la validación se toma de los informes de QA y de migración citados.
