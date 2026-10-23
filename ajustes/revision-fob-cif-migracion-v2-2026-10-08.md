# Revisión de FOB y CIF en la migración a v2

Fecha: 8 de octubre de 2026 (Colombia).

**Dictamen: la mecánica numérica revisada funciona, pero la equivalencia de conceptos no está validada. No se debe dar por cerrada la migración de FOB/CIF.** Hay dos reinterpretaciones del dato legacy que el código y las pruebas reproducen sin resolver la contradicción con las pantallas originales.

Alcance: código actual del backend `2eeaaad` y frontend `704dcef`, legacy, consultas de exportación, informes de la migración del 6 de octubre y lectura de la base local `wms_migracion`. No se consultó el estado actual de staging ni producción. Los planes y prompts existentes se usaron como evidencia, no como instrucciones para ejecutar otra migración. No se modificó código ni datos.

## 1. Hallazgo de prioridad alta: el CIF del formulario legacy se presenta como FOB en v2

El legacy pide **CIF USD** en el formulario de registro de levantes, pero lo guarda en `fob_dolares`. El reporte de pólizas y la pantalla de facturación también presentan ese importe como CIF. La v2 copia el número a `FobUsd` y lo presenta como **FOB del levante**, tanto en captura como en reportes y exportaciones.

Evidencias:

- [Formulario legacy: CIF USD guardado en fob_dolares](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/bodegas-legacy/modulos/mod_levantes/registrarlevante.php:605).
- [Reporte legacy: suma ese campo como CIF](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/bodegas-legacy/modulos/mod_inventario/reportepolizadetalle.php:479).
- [Importador v2: interpreta la columna como FOB](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/Administration/LegacyImport/Importers/ReleasesImporter.cs:54).
- [Formulario v2: solicita FOB](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Frontend/wms/app/features/foreign-trade/components/ReleaseForm.vue:607).
- [Reporte v2: presenta FOB](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Frontend/wms/app/pages/reports/policies.vue:149).

**Efecto:** un importe registrado como CIF en el legacy pasa a verse como FOB sin descontar flete ni seguro. Además, los nuevos registros solicitan FOB, por lo que pueden mezclarse importes históricos CIF con importes nuevos FOB en una misma suma. Ejemplo ilustrativo: si un documento tiene FOB USD 10.000 y CIF USD 11.100, copiar los 11.100 y llamarlos FOB no conserva el significado.

El [plan de frontend](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Frontend/wms/docs/plan-frontend-paridad-legacy.md:1053) declara que «CIF USD» es FOB porque el campo se llama `fob_dolares`. El [calculador de pólizas](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/Reports/Common/PolicySummaryCalculator.cs:12) repite esa premisa. El nombre de una columna no demuestra qué importe se digitó. El legacy también tiene rótulos FOB en otros lugares, por lo que tampoco basta con cambiar todo a CIF sin verificar documentos reales.

## 2. Hallazgo de prioridad alta: el valor comercial del depósito se asume CIF para facturar

La exportación toma `ingreso.preciomercancia` y lo carga directamente como `WarehouseStorage.CargoValue`. El reporte legacy identifica ese mismo campo como **FOB** mediante `vista_poliza`. La v2 lo trata como **CIF** al aplicar las tarifas por porcentaje.

Evidencias:

- [Vista legacy: preciomercancia AS FOB](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/bodegas-legacy/bodegas_schema.sql:2469).
- [Consulta de exportación: copia preciomercancia](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/db_legacy/trabajo/consultas/v2/11_depositos.sql:22).
- [Importador: conserva el valor y la moneda](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs:196).
- [Facturación: conversión del valor comercial a COP](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/Billing/Common/Services/StorageBillingService.cs:871).
- [Fórmula: porcentaje sobre ese importe](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/Billing/Calculators/PercentageOfValueFormulaCalculator.cs:28).
- [Captura actual: solo dice «Valor de la mercancía»](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Frontend/wms/app/features/weighbridge/components/StorageServiceForm.vue:1171).

**Efecto condicionado:** si el importe original era FOB y el convenio exige CIF, la base de cobro excluye flete y seguro y puede resultar inferior. Si ya era CIF, la copia numérica es válida y el error está en la identificación del legacy. La revisión no prueba que todas las facturas estén equivocadas ni permite cuantificar una diferencia real sin documentos comerciales.

No se encontró en este flujo una transformación FOB → CIF ni información separada de flete y seguro. Capturar directamente un CIF completo es válido: no es obligatorio calcularlo en el sistema. Lo pendiente es identificar expresamente qué se captura y qué base exige el convenio. Tampoco debe sustituirse automáticamente el valor del depósito por la suma de levantes, porque pueden ser parciales.

## 3. Comprobaciones realizadas

Consulta directa de solo lectura en `wms_migracion`, dentro de `BEGIN READ ONLY`:

| Comprobación | Resultado |
|---|---:|
| Depósitos marcados como migrados | 128 |
| De esos depósitos, con valor comercial | 128 |
| De esos depósitos, con TRM | 128 |
| Levantes existentes en esa base local | 107 |
| Levantes con importe en USD | 107 |
| Diferencias entre COP guardado y USD × tasa, redondeado al peso | 0 |

Se ejecutaron **86 pruebas: 86 aprobadas, 0 fallidas, 0 omitidas**, con este filtro:

```sh
dotnet test Wms.Tests/Wms.Tests.csproj --no-restore --filter 'FullyQualifiedName~Fob|FullyQualifiedName~PolicySummaryCalculator|FullyQualifiedName~LegacyReleaseGrouper|FullyQualifiedName~DepositRowCargoAndModality|FullyQualifiedName~WarehouseStorageMigratedCargo|FullyQualifiedName~PercentageOfValue' --verbosity quiet
```

Verifican conversión USD/COP, redondeo, conservación de la tasa al editar, agrupación de levantes, no multiplicación del importe por producto dentro del archivo, importación de valor/moneda y cálculos porcentuales. No demuestran si el importe fuente era FOB o CIF.

El [informe de migración local](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/docs/migracion-staging/resultados/informe-fase-1-repeticion.md:131) documentó igualdad de importes y pesos para 107 de 107 levantes y, en su sección de facturación, 128 de 128 cálculos coincidentes. El [informe de staging](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/docs/migracion-staging/resultados/informe-fase-3.md:269) documentó el cotejo con local. Son verificaciones numéricas históricas, no una validación documental independiente de FOB/CIF.

La conciliación automática compara stock y cantidades nacionalizadas; [no recibe FOB, CIF, moneda ni TRM](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/Administration/LegacyImport/Common/DepositReconciler.cs:11). Por tanto, un resultado «Ok» no certifica esos conceptos.

## 4. Condiciones para cerrar la revisión

1. Contrastar una muestra de depósitos y levantes con sus documentos originales: valor FOB, flete, seguro, CIF y valor efectivamente digitado en cada campo legacy. Incluir nacionalizaciones parciales.
2. Confirmar con Comercio Exterior qué importe debe conservar el levante y mostrar el reporte de pólizas; confirmar con Facturación si el convenio cobra sobre CIF o sobre otro valor comercial declarado.
3. Corregir juntos la definición, captura, importación, reportes y documentación. Preservar la procedencia de los importes históricos; no recalcularlos o renombrarlos masivamente con una suposición.
4. Añadir casos de aceptación donde FOB y CIF sean distintos, verificar la base de cobro y comparar totales antes/después de cualquier corrección aprobada.

**Resultado de la revisión:** no se encontró un error de multiplicación por TRM en los 107 levantes locales. Sí se encontró una contradicción de significado que puede mezclar FOB/CIF en reportes y afectar la interpretación de la base de facturación. El impacto monetario real queda pendiente del cotejo documental.

## 5. Verificación adicional del uso actual en v2

Realizada a petición del usuario, sobre los mismos commits. Se siguió también el alta de operaciones nuevas, además de la importación histórica.

| Etapa | Comportamiento verificado | Evaluación |
|---|---|---|
| Captura del depósito | Pide «Valor de la mercancía» o «Valor Comercial» y moneda; envía `cargoValue` sin especificar si es FOB o CIF. | Ambiguo para el operador. |
| Facturación | Convierte `CargoValue` a COP y aplica el porcentaje pactado. No toma `FobUsd` del levante ni agrega flete/seguro. | Cálculo correcto si el valor capturado corresponde a la base pactada; no garantiza por sí mismo que sea CIF. |
| Captura del levante | Solicita FOB USD; lo convierte a COP y conserva la tasa al editar. | Conversión monetaria correcta; sigue pendiente resolver el cambio respecto al CIF solicitado por el legacy. |
| Pólizas | Suma `FobUsd` de los registros y rotula el resultado como FOB. | No puede distinguir un CIF histórico importado de un FOB nuevo. |
| Varios productos del mismo levante | Permite varias filas y advierte dejar el valor vacío en las siguientes. | Prevención parcial: depende del operador. |

### Ejecución de escenarios con el código compilado

Se ejecutó un programa aislado fuera del repositorio, referenciando las DLL actuales de `Wms.Application`, `Wms.Domain` y `Wms.Common`. Sin llamadas al API ni escrituras en bases de datos. Son comprobaciones de funciones reales de dominio y aplicación, no una prueba integral de pantalla/API.

1. **Importación:** `ImportRelease.CreateMigrated` recibe USD 11.100, tasa 4.000 y COP 44.400.000. Guarda exactamente `FobUsd = 11100` y `FobCop = 44400000`. Confirma que se preserva el número, sin transformación CIF → FOB.
2. **Base de facturación:** `PercentageOfValueFormulaCalculator`, al 1 % y sin mínimo, devuelve COP 400.000 cuando la base es USD 10.000 × 4.000, y COP 444.000 cuando es USD 11.100 × 4.000. La diferencia ilustrativa es COP 44.000 antes de IVA. El calculador no determina cuál valor es FOB o CIF: cobra sobre el que recibe. No son facturas reales ni tarifas que se hayan cambiado.
3. **Repetición del valor total:** `ReleaseDuplicateRules.Check` permite el mismo número y aceptación para otro producto del mismo depósito. `PolicySummaryCalculator.Build` suma USD 20.000 si ambas filas traen USD 10.000. El handler aplica el importe a cada fila sin un control adicional de unicidad del valor por levante.

El tercer punto confirma un **riesgo adicional de doble conteo**: si USD 10.000 es el total del documento y se repite en dos productos, el reporte lo duplica. Si cada importe es una fracción del total, la suma sí es válida; la interfaz, sin embargo, define el dato como total del levante y pide registrarlo una sola vez. Esto viene de la decisión DF4 documentada, no es una regresión nueva. El [aviso en pantalla](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Frontend/wms/app/features/foreign-trade/components/ReleaseForm.vue:624) no impide guardar; la [regla del backend](/Volumes/Dock/Projects/bodegas_asociadas/code_workspace/Backend/wms-api/Wms.Application/ForeignTrade/Common/Services/ReleaseDuplicateRules.cs:54) comprueba la identidad del producto y del documento, no el importe ya registrado. No se observaron grupos con valor positivo en más de una fila en la base local de migración revisada.

### Pruebas del frontend

Se ejecutaron `DepositDetailGeneralInfoCardValues.spec.ts` y `DepositDetailGeneralInfoCard.spec.ts`: **7 pruebas aprobadas, 0 fallidas**. Cubren presentación de moneda/valor y edición de la tarjeta; no verifican la naturaleza FOB/CIF del importe. Son adicionales a las 86 pruebas de backend de la primera revisión, cuyo código no cambió.

**Conclusión de esta ampliación:** la v2 maneja dos importes independientes y convierte sus monedas correctamente, pero no garantiza el uso adecuado de FOB/CIF. Deben resolverse la identificación de la base comercial, la equivalencia de los levantes históricos y el control de un único valor total por documento (o un reparto explícito entre sus productos).
