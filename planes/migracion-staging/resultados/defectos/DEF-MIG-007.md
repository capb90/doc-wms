# Ficha de defecto — DEF-MIG-007

| Campo | Valor |
|---|---|
| ID | DEF-MIG-007 |
| Título | La guía de salida de un depósito migrado imprime el manifiesto DIAN en blanco |
| Severidad | MAJOR |
| Prioridad sugerida | Alta antes de la fase 4 (los operarios verán guías de migrados); no bloquea el despliegue de la fase 2 |
| Módulo | Comercio Exterior (guía de salida, PDF) / migración legacy |
| Caso(s) | E19 «despacho»; OK-7; cotejo del manifiesto de la muestra de 30 |
| Riesgo del plan (§9) | «La herramienta nunca se probó con datos reales (E19)» |
| Ambiente y commits | Local (`wms_migracion`) · BE `9c5c81b` · FE `4799cc4` |
| Rol / usuario | `mig.comext` (Comercio Exterior) |
| Estado | Corregido |

## Precondiciones y datos
- Cualquier depósito migrado. Ejemplo: BA0042 (v2 `2024BA00002`).
- Su manifiesto DIAN viene en el CSV (`nro_manifiestodian`, `fecha_manifiestodian`) y queda en `import_warehouse_storages.manifest_number` y `manifest_date`.
- El detalle del depósito lo muestra bien: «MANIFIESTO DIAN · Nro. Manifiesto 1165750140…».
- Los migrados no tienen camiones (`EntryLogs` vacío), así que no tienen filas en `manifests`.

## Pasos para reproducir
1. Comercio Exterior crea una orden de cargue sobre `2024BA00002`.
2. Vigilancia registra el ingreso; Báscula hace la salida (cobro y tara); Bodega carga.
3. Comercio Exterior emite la guía (`POST /api/v1/foreign-trade/dispatch-guides`).
4. Abrir el PDF (`GET /api/v1/foreign-trade/dispatch-guides/{id}/pdf`).

## Resultado esperado
- La columna «Manifiesto» de la línea imprime el manifiesto DIAN del depósito, como en el legacy.
- El legacy lo imprimía desde `ingreso.nro_manifiestodian`, en `modulos/mod_salidas/verguia.php:411,454,626`.

## Resultado obtenido
- La columna «Manifiesto» sale vacía en las 4 guías de la repetición: `2026S00001` a `2026S00004`, sobre BA0042, BA1196 y BA0558.
- También salía vacía en la primera ejecución (`2026S00001` y `2026S00002`), pero no se detectó.
- El resto de la línea es correcto: carta porte, depósito, levante, aceptación y los saldos (DEF-MIG-005 verificado).

Extracto del PDF de `2026S00001`, en texto:
```
 No.  Producto      Doc / CPI   Deposito      Manifiesto   Levante          Aceptacion       ...  Entrada  Saldo Ante.  Cant. Sale  Nvo. Saldo
  1   ATUN RALLADO  EC0004054   2024BA00002   (vacío)      372024000000525  372024000000564  ...  648      448          50          398
```

## Evidencia
Todo fuera de git:
- `db_legacy/trabajo/evidencias/v2/e19/BA0042-g1/guia-pdf.pdf` y su `.txt`.
- Lo mismo en `BA0042-g2/`, `BA1196-op/` y `BA0558-sin/`.
- Primera ejecución: `db_legacy/trabajo/evidencias/e19/guia-2026S00001.pdf`.

## Impacto
- **Alcance:** las guías de los 128 depósitos migrados salen sin el manifiesto DIAN, que el legacy sí imprimía.
- **Documento afectado:** la guía acompaña la mercancía y se entrega al conductor.
- **Lo que no afecta:** stock, saldos, facturación y conciliación.
- **Depósitos nuevos:** no les pasa, porque sus manifiestos se registran por camión en báscula.

## Pista técnica (opcional)
- `Wms.Application/ForeignTrade/Common/Services/DispatchGuidePdfService.cs:491-492` toma el manifiesto solo de `sr.EntryLogs.SelectMany(el => el.Manifests)`, y en `:517` imprime `manifest?.ManifestNumber ?? ""`.
- **Arreglo posible:** si no hay manifiesto de camión, usar `ImportWarehouseStorage.ManifestNumber` del depósito.
- **Nota:** el encabezado «Tiquetes:» también sale vacío en los migrados. Es esperable, porque los tiquetes de báscula del legacy no se migran.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en la repetición de la fase 1 de la migración, al revisar el PDF de las guías de los migrados | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** `DispatchGuidePdfService.ManifestText` arma la celda «Manifiesto» de cada línea: el manifiesto de los camiones del servicio si hay alguno (igual que antes, aunque el depósito tenga otro); si no, `ImportWarehouseStorage.ManifestNumber` del depósito; si tampoco, vacío. `LoadDepositManifestsAsync` trae los manifiestos de los depósitos de la orden en una sola consulta adicional por guía; la usan la guía completa y la guía por depósito (CE-13). Saldos (DEF-MIG-005), levante congelado (CHG-35) y formato del PDF sin cambios; el encabezado «Tiquetes:» de los migrados sigue vacío (fuera de alcance). Pruebas: `GuideManifestTests` (integración: migrado sin camiones → manifiesto del depósito; depósito con camiones y otro manifiesto en el depósito → el del camión; sin manifiesto → vacío; la reimpresión responde 200 en los tres). Commits: pendiente. | BE `69b1c81` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en `wms_migracion`, con el API local (puerto 5291) arrancado con este build y el mismo `.env.migracion.local`. Reimpresión por el API (`GET dispatch-guides/{id}/pdf`, cuenta `mig.comext`) de `2026S00001` y `2026S00002` (BA0042), `2026S00003` (BA1196) y `2026S00004` (BA0558): la columna «Manifiesto» trae el manifiesto DIAN de cada depósito, el mismo que devuelve su detalle (`GET foreign-trade/imports/{id}`). Frente a los PDF de la repetición solo cambian esa celda y la hora «impreso el»; saldos, levante y aceptación iguales. Sin `fail:` en el log. Evidencia fuera de git: `db_legacy/trabajo/evidencias/v2/def-mig-007/` (4 PDF con su `.txt`, `resumen.json` y `api.log`). Commits: pendiente. | BE `69b1c81` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-07 | **Verificado en staging** (F11-S6): guías nuevas 2026S00002 (BA0042) y 2026S00003 (BA0558) con el manifiesto DIAN del detalle; guía 2026S00001 de un depósito nuevo con el manifiesto de báscula. Texto del PDF extraído con pdf.js. Evidencia: `docs/qa/resultados/evidencias/F11/S6-B-pdf-guias-tiquete-etiqueta.txt` | BE `b31ddb6` / FE `508b91b` | Claude (QA, F11-S6) |

## Lista de verificación para la re-ejecución
- [x] Guía nueva sobre un migrado, por ejemplo BA0042: la columna «Manifiesto» imprime el `nro_manifiestodian` del legacy, el mismo que muestra el detalle del depósito. (Cubierto por `GuideManifestTests`; en `wms_migracion` solo se reimprimieron las guías existentes.)
- [x] La reimpresión imprime lo mismo: las 4 guías de `wms_migracion` imprimen el manifiesto del detalle (2026-10-06).
- [x] Guía sobre un depósito nuevo, con manifiesto registrado en báscula: imprime el de báscula, igual que antes. (Cubierto por `GuideManifestTests`; sin guía de este tipo en `wms_migracion`.)
- [x] Para re-ejecutar basta una guía sobre un migrado en `wms_migracion`; no hace falta repetir la carga.
- [x] **Staging, F11-S6 (2026-10-07, BE `b31ddb6` / FE `508b91b`):** la guía nueva 2026S00002 de BA0042 imprime en «Manifiesto» 116575014058642, y la 2026S00003 de BA0558 imprime 116575014212959, los mismos del detalle. La guía 2026S00001 de un depósito nuevo imprime el manifiesto de báscula, QA-S6-MAN-001. Evidencia: `docs/qa/resultados/evidencias/F11/S6-B-pdf-guias-tiquete-etiqueta.txt`.
