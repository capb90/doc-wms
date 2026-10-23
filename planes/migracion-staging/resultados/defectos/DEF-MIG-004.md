# Ficha de defecto — DEF-MIG-004

| Campo | Valor |
|---|---|
| ID | DEF-MIG-004 |
| Título | Los depósitos migrados no traen CIF ni moneda y el almacenamiento por % cae siempre al mínimo |
| Severidad | MAJOR |
| Prioridad sugerida | Alta antes del corte real; Media para staging |
| Módulo | Administración (migración legacy) / Facturación |
| Caso(s) | FA-MIG-008; OK-5 |
| Riesgo del plan (§9) | «Las tarifas del legacy pueden no estar en tarifa/convenio» |
| Ambiente y commits | Local (`wms_migracion`) · FE `24d742d` · BE `f6f1828` |
| Rol / usuario | Admin |
| Estado | Verificado |

## Precondiciones y datos
- 128 depósitos migrados.
- Tarifa base aprobada (T1): `PERCENTAGE_OF_VALUE`, 0,295 %, mínimo de $50.000 con IVA.
- En el legacy, `ingreso.preciomercancia` (USD) existe en los 128 ingresos vivos (0 en cero o nulo).

## Pasos para reproducir
1. Cargar los depósitos con el CSV de F6-03; sus columnas no incluyen valor ni moneda.
2. Configurar T1 y ejecutar `POST /api/v1/administration/legacy-import/open-billing`.

## Resultado esperado
El período se liquida con la fórmula mapeada sobre el CIF del depósito: CIF en USD × TRM de ingreso × 0,295 % + IVA, con piso de $50.000.

## Resultado obtenido
- Los 127 períodos abiertos quedan con `formula_code = MINIMUM_VALUE`, por $50.000.
- Advertencia en la factura:

> No existe un precio configurado ni acuerdo vigente para … Se facturó el valor mínimo de Importación ($50.000,00 IVA incluido)… Motivo: El campo 'CargoValueCop' es obligatorio para la fórmula PERCENTAGE_OF_VALUE.

- En el detalle del depósito, Moneda y Valor comercial salen «—».
- No hay pantalla ni endpoint para completarlos en un depósito confirmado.

## Evidencia
- `db_legacy/trabajo/evidencias/open-billing.json`: 127 `Opened`.
- Consulta de lectura: `storage_billing_periods` con `formula_code = 'MINIMUM_VALUE'` en 128 de 128.

## Impacto
- Ninguna tarifa por % del CIF (ni la prorrateada) se puede aplicar a los migrados.
- `PER_VEHICLE` y `PER_CARGO_UNIT` también dan 0, porque los migrados no tienen camiones.
- Con datos reales, los 36 depósitos del ciclo de 180 días cobrarían $50.000 por período, frente a ≈ $600.000 en el legacy.
- La advertencia dice «No existe un precio configurado ni acuerdo vigente», aunque la regla existe: confunde a Facturación.

## Pista técnica (opcional)
- Agregar `valor_mercancia` y `moneda` al CSV de F6-03:
  - en la consulta, `I.preciomercancia` e `I.id_paismonedaprecio`;
  - `ECU` = USD.
- Pasarlos a `WarehouseStorage.CreateMigrated` (`Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:117-152`, que hoy no los recibe) desde `DepositsImporter.cs:189`.
- Revisar el texto de la advertencia cuando la causa es el CIF faltante.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en la fase 1 de la migración; el usuario aprobó T1–T4 sabiendo que los migrados cobrarán el mínimo | BE `f6f1828` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** El CSV de depósitos admite dos columnas opcionales al final, `valor_mercancia` y `moneda` (el de 19 columnas sigue valiendo, sin CIF). Valor sin moneda, moneda desconocida, valor ≤ 0 o con más de 2 decimales, o valor/moneda distintos entre filas del mismo depósito → fila rechazada con un mensaje que nombra el campo. Moneda: `COP`, `USD` o el código de país del legacy (`ECU` → USD, `COL` → COP; `LegacyCurrencyMapper`). `WarehouseStorage.CreateMigrated` recibe `cargoValue` y `currency` y valida como el registro en báscula (valor > 0 con moneda, COP o USD); moneda extranjera sin TRM queda «TRM pendiente» con la regla existente. La consulta del plan exporta `I.preciomercancia` y `I.id_paismonedaprecio`. Cuando el mínimo se cobra porque una regla por % del CIF no tiene CIF, la advertencia dice «El depósito no tiene valor de la mercancía (CIF); se facturó el valor mínimo…» (`StorageFallbackWarning.BuildMissingCargoValue`). Sin cambios de esquema. Pruebas: `DepositRowCargoAndModalityTests`, `WarehouseStorageMigratedCargoTests`, `StorageMissingCargoValueWarningTests` (unitarias) y `MigratedStorageBillingTests` (integración: USD con TRM → 0,295 % × CIF en COP + IVA = $275.910,56; USD 100 → piso de $50.000; COP sin TRM → $351.050; USD sin TRM y la DIAN sin respuesta → TRM pendiente; sin CIF → mínimo con la advertencia nueva; valores distintos entre filas → rechazo). Fuera de alcance: completar el CIF de depósitos ya migrados. Commits: pendiente. | BE `f6f1828` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en la repetición de la fase 1 (`informe-fase-1-repeticion.md`). CSV de 21 columnas: `valor_mercancia` en 133 filas y `moneda = ECU` en 133. Carga sin rechazos. Los 128 migrados quedan en USD, con el CIF y la TRM del CSV (128 de 128). El detalle de `2024BA00002` muestra «Moneda USD · Valor Comercial US$ 34.248,00». `open-billing`: 128 Opened, todos con `PERCENTAGE_OF_VALUE` (0 `MINIMUM_VALUE`): 124 sobre el mínimo y 4 en el piso de $50.000 por CIF bajo (BA0558, BA0860, BA1283 y BA1448: 0,295 % × CIF en COP + IVA < $50.000). Cotejo independiente de los 128 (CIF × TRM × 0,295 % + IVA, piso $50.000): 128 coinciden; 10 en la tabla del informe. TRM pendiente: 0. Advertencia por CIF faltante: no aplica (los 128 traen CIF); 0 facturas con «No existe un precio configurado». Conciliación 133/133 Ok con 21 columnas. Informe de la repetición §7 y §6. | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la repetición de la fase 1
- [x] El CSV de depósitos de la consulta corregida trae 21 columnas; `valor_mercancia` con valor y `moneda` = `ECU` en las 133 filas (dump del 2024-06-10).
- [x] La simulación y el firme de `Deposits` dan 0 rechazos por valor o moneda.
- [x] En el detalle de los migrados, Moneda = USD y Valor comercial = el `preciomercancia` del legacy (ya no «—»).
- [x] Tras cargar T1 y ejecutar `open-billing`, los períodos con CIF liquidan **0,295 % × CIF × TRM de ingreso + IVA**, con el mínimo de $50.000 IVA incluido como piso. Anotar cuántos quedan sobre el mínimo y cuántos en el piso, y cotejar 10 a mano.
- [x] Ningún migrado con CIF y TRM queda con `formula_code = MINIMUM_VALUE`.
- [x] Los migrados con moneda extranjera sin TRM, si hay, quedan «TRM pendiente» (contarlos). Con el dump actual se espera **0**: los 128 traen TRM.
- [x] Si alguno cae al mínimo por falta de CIF, su factura dice «El depósito no tiene valor de la mercancía (CIF); se facturó el valor mínimo…» y no «No existe un precio configurado ni acuerdo vigente». — *No aplica: los 128 traen CIF.*
- [x] La conciliación sigue en 133/133 «Ok» con el CSV de 21 columnas.
