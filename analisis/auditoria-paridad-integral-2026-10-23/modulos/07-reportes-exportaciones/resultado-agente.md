# 07 · Reportes y exportaciones — Resultado del agente AG-07

> Auditoría estática del 2026-10-23. Sin Git, sin builds, sin pruebas, sin APIs ni bases de datos. Código en disco, que según `docs/contexto/estado.md` corresponde a BE `35a61b2` / FE `c924a8b`. Rutas relativas a `code_workspace/`.
> **Prefijos:** `L:` = `bodegas-legacy/`; `FE:` = `Frontend/wms/app/`; `BE:` = `Backend/wms-api/`.

## 1. Cobertura

- **Legacy asignado:** 15 capacidades (CF-L208…216, CF-L229, CF-L231…233, CF-L252, CF-L258), auditadas las 15, con 12 desgloses por operación (CF-L210.a/b/c, CF-L214.a/b, CF-L229.a/b/c, CF-L231.a/b, CF-L233.a/b).
- **Filas referidas:** CF-L172.c (reporte general de Bodega, que el módulo 03 dejó `NO_VERIFICADO`: queda **PARCIAL** por BR-07-010) y CF-L121.c (exportación del reporte de báscula: `COMPLETO_CODIGO`, coherente con `modulos/02-bascula/`).
- **Legacy no catalogado:** CF-LX07-01 (caché HTML por usuario y descarga sin sesión de `reporteexcel.php`/`crearpdf.php`) y CF-LX07-02 (`L:reportes/ejemplo.php`, sin invocador).
- **V2:** CF-V070 confirmada como `SOLO_V2`; CF-V071 reasignada a CF-L209 (es el kardex). Sin `SOLO_V2` nuevas.
- **Archivos legacy leídos:** los informes de `L:modulos/mod_inventario/` en sus partes funcionales (permisos, SQL, columnas, totales, exportación), `L:modulos/mod_bodegas/reportegeneral.php`, los 8 `.php` de `L:reportes/`, `L:reportesweb/reportesias.php` y `reportesiasdetalle.php` (consultas y encabezados), `L:includes/barcode/code128.php`, `L:menus/menuizquierda.php`. Las variantes Colmotores se identificaron por menú sin leerse a fondo.
- **Facturación:** `modulos/06-facturacion/` no existía al cerrar: de `FE:pages/billing/reports/*` se evaluaron solo forma, columnas, contrato y exportación (`05-analisis-v2.md` §1.1, `09-integraciones.md` §6), sin filas en la matriz.

## 2. Conteos (matriz `06-matriz-paridad.md`, 33 filas)

**Paridad integral — 15 capacidades asignadas:** COMPLETO_CODIGO 3 (CF-L208, 216, 252) · PARCIAL 9 (CF-L209, 210, 211, 213, 215, 229, 231, 232, 258) · DIFERENCIA_INTENCIONAL 2 (CF-L214 por P6a/P6c/DEC-016; CF-L233 por GAP-012) · NO_APLICA 1 (CF-L212, Colmotores) · NO_IMPLEMENTADO 0 · NO_VERIFICADO 0.

**Todas las filas legacy (31):** COMPLETO_CODIGO 6 · PARCIAL 16 · DIFERENCIA_INTENCIONAL 7 · NO_APLICA 2.

| Dimensión | Legacy (31 filas) | V2 (2 filas) |
| --- | --- | --- |
| Frontend | COMPLETO 13 · PARCIAL 13 · NO_APLICA 5 | COMPLETO 2 |
| Backend | COMPLETO 17 · PARCIAL 9 · NO_APLICA 5 | COMPLETO 2 |
| Integración | CONECTADO 23 · PARCIAL 2 · NO_APLICA 6 | CONECTADO 1 · PARCIAL 1 |
| Reglas | COMPLETO 14 · PARCIAL 13 · NO_APLICA 4 | NO_APLICA 2 |

**Validación por ejecución:** 17 de 33 filas citan una ejecución previa (F7 y re-tests F11-S3 de DEF-F7-*; tres de ellas según los módulos 02 y 04: F3-HIS-003, F5-ETI-*); 5 filas padre remiten a su desglose; CF-L214.a/.b tienen caso previsto (F7-REP-005/006, «NO VERIFICABLE» por falta de datos); las demás, «No ejecutada en esta auditoría» o «No aplica».

**`all=true`:** honrado en código por las 17 consultas que se exportan (13 listados + inventario general, ingresos por producto, detalle de pólizas, mercancía en abandono) y pedido por las 20 pantallas con Excel; ninguna sube `pageSize`.

**Datos simulados:** ninguno.

## 3. Brechas (13)

| Criticidad | Cantidad | IDs |
| --- | ---: | --- |
| CRÍTICA | 0 | — |
| ALTA | 0 | — |
| MEDIA | 4 | BR-07-001, BR-07-002, BR-07-003, BR-07-004 |
| BAJA | 9 | BR-07-005 … BR-07-013 |

Las más relevantes:
1. **BR-07-001 (MEDIA):** los diarios de ingreso y salida no tienen Excel, contra `DECISIONES_REVISION.md` §2.E.18 y GAP-017.
2. **BR-07-002 (MEDIA):** el diario de ingresos no muestra depósito, importador, agencia, manifiesto DIAN, peso de manifiesto, total de vehículos ni firmas, y pasa de una fila por camión a una por producto.
3. **BR-07-003 (MEDIA):** kardex, diario de ingresos y Excel de importaciones usan `CreatedAt` como fecha de ingreso en lugar de `WarehouseStorage.EntryDate` (DEC-012, DEC-010.4).
4. **BR-07-004 (MEDIA):** en kardex y diarios, «Manifiesto» es la carta porte; el manifiesto DIAN no aparece y el kardex no muestra la agencia.
5. **BR-07-005 (BAJA):** el Excel pierde las firmas del informe de póliza (`footerLines` ignorado en hoja única), escribe «undefined» en su fila de totales y no trae totales en inventario general ni detalle de pólizas.

Ninguna duplica una ficha `DEF-*` (revisión en `08-brechas.md`); BR-07-004 recoge una observación sin ficha de DEF-F7-009 (F11-S3).

## 4. SOLO_V2

- **CF-V070** Estadísticas operativas: confirmada; pantalla oculta por decisión del usuario (`FE:pages/reports/statistics.vue:12-18`, `redirect: "/"`), API activo con el bloque de facturación solo para Admin (CHG-80).
- **CF-V071** «Movimientos de bodega»: reasignada a CF-L209 (no es `SOLO_V2`).

## 5. Contraste con el análisis anterior

### 5.1 Estados de `MIGRATION_MATRIX.md` (15 capacidades)

| Capacidad | Estado previo | Clasificación | Motivo |
| --- | --- | --- | --- |
| CF-L208 | CUBIERTA | CONFIRMADA_EN_CODIGO | Menú CE › Reportes con 9 informes (`FE:components/layout/AppMenu.vue:400-451`) |
| CF-L209 | PARCIAL («no incluye nacionalizaciones») | OBSOLETA | F5-04 agregó levantes, despachos y saldos; sigue PARCIAL por BR-07-003/004/005/013 |
| CF-L210 | CUBIERTA («con PDF») | INCOMPLETA | Hay PDF, pero faltan Excel y columnas (BR-07-001…004) |
| CF-L211 | PARCIAL (sin filtros; exportación rota) | OBSOLETA | F5-05 implementado con Excel `all=true`; quedan BR-07-005/010 |
| CF-L212 | EXCLUIDA | CONFIRMADA_EN_CODIGO | Sin restos de Colmotores en los informes |
| CF-L213 | COMPORTAMIENTO DIFERENTE (un parcial no aparece como pendiente) | CONFIRMADA_EN_CODIGO | Sigue así (`GetImportDepositsHandler.cs:38-39`); BR-07-008 |
| CF-L214 | NO ENCONTRADA | OBSOLETA | F2-10 implementado (P6a, P6c) |
| CF-L215 | NO ENCONTRADA | OBSOLETA | F5-06 implementado; BR-07-005/006/009 |
| CF-L216 | PARCIAL | OBSOLETA | F5-07 implementado |
| CF-L229 | NO ENCONTRADA | OBSOLETA | F5-10 implementado; BR-07-011 |
| CF-L231 | CUBIERTA («QuestPDF en servidor») | INCOMPLETA | Solo kardex y diarios tienen PDF (BR-07-006) |
| CF-L232 | PARCIAL (50 filas; método inexistente) | OBSOLETA | Ambos defectos corregidos (F5-01, DEF-F4-008); quedan BR-07-001/005/007 |
| CF-L233 | PARCIAL (registro de impresión solo para guías) | OBSOLETA | Registro y lista de impresiones de etiquetas (`LabelPrintsController.cs:20-25`) |
| CF-L252 | CUBIERTA | CONFIRMADA_EN_CODIGO | Filtro de ubicaciones por `reports/general-inventory/locations` |
| CF-L258 | CUBIERTA («Code128 en etiquetas, depósito y guía») | CONTRADICHA_POR_CODIGO | Depósito y guía usan Code 39 (`DepositPdfService.cs:546-567`, `DispatchGuidePdfService.cs:784-805`) |

**Totales:** CONFIRMADA_EN_CODIGO 4 · OBSOLETA 8 · INCOMPLETA 2 · CONTRADICHA_POR_CODIGO 1 · NO_VERIFICADA 0.

### 5.2 Afirmaciones de los planes y documentos

| Afirmación | Fuente | Clasificación | Evidencia |
| --- | --- | --- | --- |
| F5-01: cada endpoint de C-F5-14 devuelve todas las filas con `all=true` | plan backend §C.5 | CONFIRMADA_EN_CODIGO | `QueryParametersBase.cs:20-32`; 17 consultas verificadas (`05-analisis-v2.md` §4) |
| F5-04: el informe y el PDF muestran las cinco secciones del kardex | plan backend §C.5 | CONFIRMADA_EN_CODIGO | `WarehouseMovementsPdfService.cs:247-321`; encabezado con BR-07-003/004 |
| F5-05: el inventario filtra por cada criterio y devuelve totales | plan backend §C.5 | CONFIRMADA_EN_CODIGO | `GetGeneralInventoryHandler.cs:25-86` |
| F5-06: resumen y detalle de pólizas | plan backend §C.5 | CONFIRMADA_EN_CODIGO | `PolicyReportsController.cs:25-46`; `PolicyReleaseQuery.cs` |
| F5-07 ingresos por producto; F5-10 agencias; F2-10 abandono | plan backend §C.5, §C.2 | CONFIRMADA_EN_CODIGO | Handlers de `BE:Wms.Application/Reports/Queries/` |
| Regla común «Solo leen» | plan backend §C.5 | CONFIRMADA_EN_CODIGO | Sin `SaveChanges` en `BE:Wms.Application/Reports` |
| C.5.0: diarios «existentes» como equivalentes | plan backend §C.5.0 | INCOMPLETA | BR-07-001, BR-07-002 |
| F5-01 frontend: fila 2 con los filtros | plan frontend §C.5 | INCOMPLETA | Utilidad lista (`excel-export.ts:88-92`), solo la usa CPI |
| F5-05 frontend: «Fila de totales. Exportar Excel» | plan frontend §C.5 | INCOMPLETA | Excel sin totales (`general-inventory.vue:113-142`) |
| F5-06 frontend: Excel del resumen con las tres firmas | plan frontend §C.5 | CONTRADICHA_POR_CODIGO | `excel-export.ts:158-166` no pasa `footerLines` |
| F5-10 frontend: salidas del detalle (plan backend desviación 10 agrega `productName`) | planes §C.5 | INCOMPLETA | Tipo TS sin `productName` (BR-07-011) |
| Criterio de salida 2 del frontend (kardex, inventario, pólizas, ingresos, facturación, báscula, agencias con Excel) | plan frontend §C.5 | CONFIRMADA_EN_CODIGO | Excel en las siete pantallas |
| DF12: Excel en el frontend con `exceljs` e `import()` dinámico, siempre `all=true` | plan frontend §A.4 | CONFIRMADA_EN_CODIGO | `excel-export.ts:155`; `useExcelExport.ts` |
| §G.8: el «Exportar» de `AppTable` exporta solo la página | plan frontend §G | CONFIRMADA_EN_CODIGO (sigue sin corregir) | `AppTable.vue:260-265` (BR-07-007) |
| §G.12: el número legacy no se expone | plan frontend §G | CONFIRMADA_EN_CODIGO | `LegacyNumber` solo en `Administration/LegacyImport` (BR-07-013) |
| §2.A.1: el reporte para agencias se construye | `DECISIONES_REVISION.md` | CONFIRMADA_EN_CODIGO | CF-L229.a |
| §2.E.18: Excel sin límite y los mismos informes que el legacy | `DECISIONES_REVISION.md` | CONTRADICHA_POR_CODIGO | Límite resuelto; diarios sin Excel (BR-07-001) |
| GAP-016 «construir» | `FUNCTIONAL_GAPS.md` | CONFIRMADA_EN_CODIGO | Informes construidos (con brechas BAJA/MEDIA) |
| GAP-017 «construir» | `FUNCTIONAL_GAPS.md` | INCOMPLETA | BR-07-001 |
| GAP-010 «construir» | `FUNCTIONAL_GAPS.md` | CONFIRMADA_EN_CODIGO | CF-L229 |
| «Toda la funcionalidad planeada está implementada» (este módulo) | `docs/contexto/estado.md` §1 | INCOMPLETA | 4 brechas MEDIA |

## 6. Incertidumbres

- No se sabe qué informes legacy se usaban en producción ni si la DIAN recibía los diarios y la póliza firmados: condiciona la criticidad de BR-07-002, 004 y 006.
- `L:reportes/reporteimpresionadhesivos.php` parece no funcional (rutas `../../`); no se pudo comprobar.
- La validez del FOB de las pólizas depende del pendiente 8 de `docs/contexto/estado.md` §4 (FOB/CIF de la migración).
- Las líneas citadas de `reports-service.ts` se tomaron por rangos de función; el contrato se comparó sobre los tipos TS y los DTO, no sobre respuestas reales.

## 7. Lo que quedó sin analizar

- **Cálculo de los informes de facturación** (anual y CPI): módulo 06 (aquí solo forma y exportación).
- **Variantes Colmotores** y el portal de clientes Colmotores (RN-077): excluidos; solo se verificó la ausencia de restos.
- **PDF de documentos operativos** (tiquete, etiqueta, depósito, guía, factura, orden de trabajo, novedad): pertenecen a los módulos 02 a 06; aquí solo la simbología del código de barras.
- **Contenido de `L:reportes/*/informe_u*.*`:** salidas generadas con posibles datos de personas; no se abrieron.
- Nada se ejecutó: los estados son de código, no de funcionamiento.
