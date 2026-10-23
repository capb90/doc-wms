# Ficha de defecto — DEF-MIG-001

| Campo | Valor |
|---|---|
| ID | DEF-MIG-001 |
| Título | La consulta de depósitos de F6-03 exporta una modalidad que el importador rechaza |
| Severidad | MAJOR |
| Prioridad sugerida | Media |
| Módulo | Administración (migración legacy) |
| Caso(s) | FA-MIG-001, FA-MIG-003; plan de migración §3.5 |
| Riesgo del plan (§9) | «La herramienta nunca se probó con datos reales (E19)» |
| Ambiente y commits | Local (`wms_migracion`) · FE `24d742d` · BE `f6f1828` |
| Rol / usuario | Admin |
| Estado | Verificado |

## Precondiciones y datos
- Maestros cargados en firme.
- CSV de depósitos generado con la consulta de `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` ≈ línea 2921, que entrega `M.nom_modalidad AS modalidad`.
- En el dump, `modalidad.nom_modalidad` = «Entrada por Importación», «Entrada por Exportación», «Salida por …» y «Solo servicio de pesaje».
- En la v2, `operation_modalities.name` = «Importación», «Exportación» y «Depósito por Inspección».

## Pasos para reproducir
1. Exportar los depósitos con la consulta del plan, completando `saldo` y `trm_ingreso`.
2. `POST /api/v1/administration/legacy-import/Deposits` con `dryRun=true`.

CSV de ejemplo, anonimizado:
```
nro_deposito;fecha_deposito;modalidad;id_cliente;id_importador;id_exportador;id_sia;nro_doccomercial;fecha_doccomercial;nro_manifiestodian;fecha_manifiestodian;id_producto;id_embalaje;ingresan;nacionalizados;salen;saldo;ultimo_fin_facturado;trm_ingreso
BA9001;2024-01-10 11:44:00;Entrada por Importación;900;900;;10;EC0000001;2024-01-09;116570000000001;2024-01-09;100;23;648;648;200;448;2026-09-30;3929.79
```

## Resultado esperado
F6-03 regla 1: «`modalidad` acepta el código v2 (`IMP`, `EXP` o `INSP`) o el nombre legacy». La consulta del plan y el importador deberían entenderse: con la salida de la consulta, la fila se acepta como `IMP001`.

## Resultado obtenido
133 de 133 filas rechazadas:

> Fila 2: la modalidad «Entrada por Importación» no tiene equivalente en la v2. Use IMP, EXP o INSP.

## Evidencia
- Lote de simulación `def1-Deposits-sim` (en `db_legacy/trabajo/evidencias/carga/`).
- `GET /administration/legacy-import/batches` → lote `Deposits` con `errorRows = 133`.

## Impacto
- Con la consulta del plan no se migra ningún depósito.
- **Paliativo aplicado en la fase 1:** la consulta congelada (`db_legacy/trabajo/consultas/11_depositos.sql`) exporta el código de la v2 con `CASE I.id_modalidad WHEN 1 THEN 'IMP' WHEN 2 THEN 'EXP' END`. Con ella, 0 rechazos.

## Pista técnica (opcional)
Hay dos arreglos posibles (con uno basta):
- Corregir la consulta del plan (≈ línea 2921) para que exporte el código.
- O que `LegacyDepositRowParser.ResolveModality` (`Wms.Application/Administration/LegacyImport/Common/LegacyDepositRowParser.cs:130-147`) reconozca los nombres «Entrada por Importación» y «Entrada por Exportación».

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en la fase 1 de la migración (E19) | BE `f6f1828` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** La consulta de depósitos del plan exporta el código (`CASE` por `id_modalidad`) y `LegacyDepositRowParser.ResolveModality` acepta, sin mayúsculas ni tildes, «Entrada por Importación» → IMP y «Entrada por Exportación» → EXP, además de los códigos y los nombres de la v2. El dump no tiene modalidad de inspección. El mensaje para un valor desconocido no cambia. Pruebas: `DepositRowCargoAndModalityTests` (nombres, códigos, «Entrada por Otros», «Salida por…» y «Solo servicio de pesaje» rechazados) y las de `DepositRowParserTests`, sin editarlas. Commits: pendiente. | BE `f6f1828` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en la repetición de la fase 1 (`informe-fase-1-repeticion.md`). La consulta de depósitos del plan, extraída sin editar (`consultas/v2/11_depositos.sql`), exporta `modalidad = IMP` en las 133 filas. La simulación y el firme de `Deposits` dan 133 creados y **0 rechazos**. Prueba opcional: el mismo CSV con «Entrada por Importación» (y números `SIM…`) en simulación da 133 creados y 0 errores (`evidencias/v2/carga/def1-Deposits-nombre-legacy-sim.json`). Informe de la repetición §5.1. | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la repetición de la fase 1
- [x] La consulta de depósitos de `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` (F6-03, «Depósitos. Corregida…», ≈ línea 2938) se ejecuta **tal como está** y la columna `modalidad` sale `IMP` en las 133 filas.
- [x] La simulación de `Deposits` con ese CSV da **0 rechazos por modalidad** (ningún «la modalidad «…» no tiene equivalente»).
- [x] Opcional: una simulación con la columna cambiada a «Entrada por Importación» (como la consulta vieja) también se acepta como `IMP001`.
