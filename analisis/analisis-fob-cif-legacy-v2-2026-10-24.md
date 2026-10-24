# Análisis de FOB y CIF: legacy frente a V2, con comprobación en los datos del legacy

> **Fecha:** 24 de octubre de 2026 (Colombia).
> **Pedido:** el usuario quiere saber cómo se usan el valor FOB y el valor CIF, y en qué se diferencian el legacy y V2, para tomar decisiones. Autorizó la comprobación sobre los datos del legacy.
> **Alcance:**
> - el código actual: backend `develop` `b27c9bf`, frontend según `contexto/estado.md`;
> - el código PHP del legacy y su esquema (`bodegas-legacy/bodegas_schema.sql`);
> - consultas **de solo lectura** sobre la copia del legacy en el contenedor local `legacy-mariadb`, cargada desde `db_legacy/backupBodegas.sql`.
>
> **Qué no se hizo:** no se modificó código, datos, staging ni el plan `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md`.
> **Datos personales:** este documento solo tiene **cifras agregadas**, sin clientes, agencias, personas ni números de documento (`DEC-007`). Las extracciones de trabajo se hicieron fuera del repo y no se versionan.
> **Antecedente:** `analisis/revision-fob-cif-migracion-v2-2026-10-08.md`, cuyos dos hallazgos este análisis confirma y amplía.

## 1. Resumen

1. **V2 tiene los dos conceptos invertidos respecto al legacy.**
   - El valor del depósito (`WarehouseStorage.CargoValue`) viene de `ingreso.preciomercancia`, que el legacy trataba como **FOB**, y V2 lo cobra como **CIF**.
   - El valor del levante (`ImportRelease.FobUsd`) viene de `levante.fob_dolares`, que el legacy pedía y rotulaba como **CIF**, y V2 lo llama **FOB**.
2. **Los datos lo confirman.** En el 74 % de los depósitos totalmente nacionalizados, la suma de los levantes supera el valor del ingreso, con una mediana de +3 % y un percentil 90 de +20 %. Es el patrón del flete y el seguro.
3. **El historial de facturas no decide la base de cobro.** Facturación digitaba los valores, que no siguen un porcentaje constante ni del FOB ni del CIF. En el total, la diferencia entre las dos bases es de un **0,7 %**.
4. **Lo que más dinero mueve es la configuración de la tarifa, no la base.** Simulada sobre el último año del volcado, la tarifa base T1 aprobada para la migración (`DEC-041`), aplicada a todos sin acuerdos, factura **el 205 % de lo que facturó el legacy**. Las renovaciones salen al 372 % y los lotes grandes, hasta el 273 %.
5. **Con acuerdos por cliente, V2 sí puede facturar como el legacy en el total (§5).** Basta un porcentaje calibrado por cliente con la fórmula **prorrateada** (`PERCENTAGE_OF_VALUE_PRORATED`):
   - **dentro de la muestra:** 101,7 % del total, con 101,4 % en primeros períodos y 102,7 % en renovaciones;
   - **por tamaño de lote:** entre el 84 % y el 114 %;
   - **fuera de la muestra, en 2024:** 88 %.

   No hace falta desarrollar tarifas de renovación ni tramos. Lo que no se puede reproducir es cada factura individual, porque el legacy las digitaba a mano.

*Actualizado el 24-oct-2026 con la simulación de acuerdos por cliente (§5), que corrige las conclusiones de la primera versión sobre capacidades faltantes en V2.*

## 2. Cómo usa los valores el legacy (código)

| Dato | Campo | Rótulos | Uso |
| --- | --- | --- | --- |
| **Valor de la mercancía del ingreso** | `ingreso.preciomercancia`, con `id_paismonedaprecio` | En pantalla, «Valor de la Mercancía». En la base, **FOB**: `vista_poliza` y `vista_deposito_cif_fob` lo exponen `AS FOB` (`bodegas_schema.sql:2298`, `:2469`) | Solo se mostraba a Facturación, en USD y en COP con la tasa del día de ingreso (`modulos/mod_facturacion/listardepositosfacturar.php:525-530`) |
| **Valor del levante** | `levante.fob_dolares`, `fob_pesos` y `tasa_cambio` | **CIF** en las pantallas activas: «CIF USD» al registrar (`mod_levantes/registrarlevante.php:605`) y «CIF USD / CIF CO» al editar (`modificarlevante.php:413-417`). También en el kárdex (`mod_inventario/kardex.php:356`), en «Depósitos por facturar» («Total CIF», `:634-652`) y en la póliza («CIF UAP» y «CIF NUAP», `reportepoliza.php:371-372`). `vista_deposito_cif_fob` expone `SUM(fob_dolares) AS CIF` | Póliza, kárdex e información para Facturación |

**Observaciones del código:**

- **El rótulo del levante cambió de FOB a CIF.** Las copias anteriores del formulario dicen «FOB» (`registrarlevante-copia.php`, `registrarlevante_ante.php`, `modificarlevante_colm.php`, `listarlevantes_ante.php`) y las versiones activas dicen «CIF». Quedan restos de FOB en las activas: «FOB CO» en el campo en pesos (`registrarlevante.php:629`) y «FOB US» en la lista (`:537`). Se interpreta como un cambio deliberado del significado que no llegó al nombre de la columna.
- **El legacy no calculaba el cobro de almacenamiento.** `cron.php` crea los períodos con el valor vacío (`:92`, `:119`, `:130`), y Facturación digitaba el «Valor Factura» (`mod_facturacion/facturarciigo.php:288-291`). Ningún código dice sobre qué base se aplicaba un porcentaje.
- **Tasa del levante:** la vigente el día del registro (`registrarlevante.php:93,599`); la tasa del día de ingreso quedó comentada. **Tasa del ingreso:** la del día de ingreso (`listardepositosfacturar.php:525`).

## 3. Cómo usa los valores V2 (código)

| Dato | Campo | Rótulos | Uso |
| --- | --- | --- | --- |
| **Valor del depósito** | `WarehouseStorage.CargoValue` + `Currency` (solo COP o USD) + `Trm` (DIAN o manual, del día de ingreso) | Captura: «Valor de la mercancía» (`F/features/weighbridge/components/StorageServiceForm.vue:1171`) o «Valor Comercial» (`DepositDetailGeneralInfoCard.vue:205,273`). Facturación y glosario: **CIF**. Ejemplos: «valor de la mercancía (CIF)» (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:34`), «Umbral CIF» (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:432`), «Valor de la mercancía (CIF)» (`F/features/agreements/components/FormulaPreviewPanel.vue:98`), y en el glosario «CIF / valor de la carga = `CargoValue`» (`contexto/contexto-negocio-wms-para-ia.md:67`) | **Base del cobro de almacenamiento**: `PERCENTAGE_OF_VALUE` y `PERCENTAGE_OF_VALUE_PRORATED` sobre `CargoValue × TRM` (`StorageBillingService.cs:868-883`), prorrateado por grupo según `ReceivedQuantity` (`:103-199`; `DEC-025`, `DEC-026`) |
| **Valor del levante** | `ImportRelease.FobUsd`, `FobCop`, tasa y fecha, fijos (RN-060) | **FOB** en todas partes: formulario (`F/features/foreign-trade/components/ReleaseForm.vue:603-622`), listados, detalle del depósito, kárdex («FOB USD», `B/Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs:278`) y póliza («FOB UAP» y «FOB no UAP», `F/pages/reports/policies.vue:100-101`) | Póliza y kárdex. **No interviene en la facturación** |

**Observaciones del código:**

- **La premisa está escrita en el código.** `B/Wms.Application/Reports/Common/PolicySummaryCalculator.cs` y `F/pages/reports/policies.vue:5` dicen que el legacy «rotula CIF pero suma el FOB». La justificación es solo el nombre de la columna `fob_dolares`.
- **El valor del depósito solo se edita en Borrador** (`B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:428-448`): un depósito confirmado no se puede corregir sin anularlo.
- **En V2 el levante es por producto; en el legacy, una fila por levante con varios productos.** El valor solo se registra una vez gracias a un aviso (DF4) que no impide guardar. La póliza lo sumaría dos veces si se repite. La migración lo evita con `LegacyReleaseFobSplitter`.
- **Tres nombres para el mismo dato.** La fórmula se llama «Porcentaje del valor declarado», su umbral «Umbral CIF» y la captura «Valor de la mercancía» o «Valor Comercial».
- **Exportación e inspección** también exigen el valor (P2) y lo tratan igual.
- **Hay paridad en:** la TRM del depósito (fecha de ingreso), la TRM del levante (día del registro, `ReleaseFobService.cs:60-66`), el mes de la póliza (fecha del depósito) y la conversión a pesos.

## 4. Comprobación en los datos del legacy

### 4.1 Universo

| Concepto | Cantidad |
| --- | ---: |
| Períodos de almacenamiento facturados (`facturaciigo`, estado `facturada`), importación | 13.314 |
| De ellos, quincenales | 12.905 |
| Depósitos de importación | 9.680 |
| Levantes | 12.143 |
| Años de facturación | 2021 (6), 2022 (6.924), 2023 (5.455), 2024 (2.160) |
| Moneda del ingreso | Dólares en todos los depósitos con valor (código `ECU`) |

El texto de las facturas (`detallefactura`) no menciona FOB, CIF, porcentajes ni «valor»: describe la mercancía, el depósito, el período y la agencia.

### 4.2 Valor del ingreso frente a suma de levantes

Sobre los 9.599 depósitos totalmente nacionalizados (lo nacionalizado es igual a lo recibido), se calculó la suma de `levante.fob_dolares` dividida por `ingreso.preciomercancia`, las dos en dólares:

| Resultado | Depósitos | % |
| --- | ---: | ---: |
| Igual (±0,5 %) | 2.102 | 21,9 |
| Mayor, entre +0,5 % y +10 % | 4.271 | 44,5 |
| Mayor, entre +10 % y +30 % | 2.445 | 25,5 |
| Mayor en más de un 30 % | 383 | 4,0 |
| Menor, entre −0,5 % y −10 % | 216 | 2,3 |
| Menor, entre −10 % y −50 % | 139 | 1,4 |
| Menor en más de la mitad | 43 | 0,4 |

Los percentiles del cociente son p25 = 1,005; mediana = 1,030; p75 = 1,129; p90 = 1,199.

**Lectura:** el levante casi nunca es menor que el ingreso y suele superarlo en el rango típico del flete y el seguro. Confirma que el ingreso es FOB y el levante CIF, como rotula la vista `vista_deposito_cif_fob`.

### 4.3 ¿Sobre qué base cobraba Facturación?

Se comparó cada valor facturado (neto de IVA, sin los períodos al mínimo) con dos bases:

- **FOB:** `preciomercancia × TRM del día de ingreso`;
- **CIF:** la suma de `levante.fob_pesos`.

| Prueba | FOB | CIF |
| --- | ---: | ---: |
| Períodos a ±2 % del porcentaje más frecuente (todos los clientes) | 2,2 % | 3,1 % |
| Lo mismo, con un porcentaje propio por cliente | 13,2 % | 12,2 % |
| Coeficiente de variación mediano del porcentaje, por cliente (37 clientes donde las bases difieren más de un 10 %) | 0,313 | 0,324 |
| Clientes donde esa base es la más estable | 15 | 22 |
| Correlación de logaritmos con el valor facturado, primer período | 0,60 (pendiente 0,45) | 0,60 (pendiente 0,46) |

Como referencia, el peso bruto tiene una correlación de 0,16 y la cantidad recibida, de −0,15.

**Lectura:**

- El valor facturado depende del valor de la mercancía, pero **no como un porcentaje constante**: la pendiente de 0,45 indica un porcentaje que baja a medida que sube el valor.
- Ninguna de las dos bases se impone, y ningún porcentaje común coincide de forma exacta en más del 2,5 % de las facturas.
- **El historial no permite decidir entre FOB y CIF.**

### 4.4 Primer período frente a renovaciones (quincenales)

| | Primer período | Renovación |
| --- | ---: | ---: |
| Quincenas | 9.026 | 3.496 |
| Facturadas al mínimo | 6 % | 16 % |
| % sobre el valor del lote, con IVA: p25 / mediana / p75 | 0,132 / **0,293** / 0,422 | 0,055 / **0,087** / 0,137 |
| % sobre el valor ajustado al saldo al inicio, con IVA: mediana | — | 0,118 |
| Saldo al inicio ÷ recibido: mediana | 1,00 | 0,88 |

**Lectura:**

- El legacy cobraba las renovaciones a cerca de un tercio del porcentaje del primer período.
- Mezclando todos los clientes, el saldo no parece explicarlo: quedaba un 88 % de la mercancía y aun así el porcentaje bajaba a un tercio. **Cliente por cliente sí lo explica (§5.6).**
- El 49,2 % de las renovaciones (1.732 de 3.522) repite el valor del período anterior.

### 4.5 Porcentaje según el tamaño del lote (primer período, por quintiles del valor FOB × TRM)

| Valor de la mercancía | Lo que cobró el legacy (con IVA) | T1 frente al legacy |
| --- | ---: | ---: |
| Menos de $23 M | 0,869 % (efecto del mínimo) | 56 % |
| $23 M – $32 M | 0,381 % | 92 % |
| $32 M – $80 M | 0,325 % | 108 % |
| $80 M – $220 M | 0,200 % | 176 % |
| Más de $220 M | 0,129 % | 273 % |

**Lectura:**

- El porcentaje real baja a medida que sube el valor del lote.
- Los importes fijos que más se repiten sugieren cargos por camión en los lotes grandes; por ejemplo, $110.075 = $92.500 + IVA, que `planes/migracion-staging/resultados/mapeo-tarifas-propuesto.md` ya asociaba a camiones de 33 t.

### 4.6 Simulación de T1 frente a lo que facturó el legacy

**Supuestos:**

- T1 tal como se cargó en staging (`mapeo-tarifas-propuesto.md` §5): 0,295 % neto + 19 % de IVA por período, con un mínimo de $50.000 con IVA;
- quincenas facturadas entre el 1 de julio de 2023 y el 30 de junio de 2024: 4.640.

| Escenario | Total | Frente al legacy |
| --- | ---: | ---: |
| Lo que facturó el legacy | $1.122.306.075 | 100 % |
| T1 sobre FOB, lote completo (lo que hace V2 hoy) | $2.297.636.063 | **205 %** |
| T1 sobre CIF, lote completo | $2.314.294.761 | 206 % |
| T1 sobre FOB, prorrateado por saldo | $1.735.773.401 | 155 % |
| T1 sobre CIF, prorrateado por saldo | $1.741.287.088 | 155 % |

**Por tipo de período:**

| | Quincenas | Legacy | T1 sobre FOB | T1 sobre CIF |
| --- | ---: | ---: | ---: | ---: |
| Primer período | 3.119 | $837.703.390 | 148 % | 150 % |
| Renovación | 1.521 | $284.602.685 | **372 %** | 371 % |

## 5. Simulación con acuerdos por cliente

La simulación del §4.6 aplica una sola tarifa base (T1) a todos los depósitos, como si ningún cliente tuviera acuerdo. En V2 la tarifa sale de un **motor de acuerdos**: Facturación registra los acuerdos de cada cliente y el sistema cobra con ellos. Solo usa la tarifa base cuando no hay acuerdo (`DEC-027`). Esta sección prueba si, con acuerdos por cliente, V2 podría facturar como el legacy.

### 5.1 Qué puede expresar un acuerdo en V2 (código)

- **Dimensiones de una regla del acuerdo** (`B/Wms.Domain/Entities/Agreement/AgreementService.cs:14-27`): cliente (por el acuerdo), servicio, producto, modalidad y si la carga es perecedera.
- **Parámetros de las dos fórmulas de valor** (`SeedDataExtensions.cs`, `PERCENTAGE_OF_VALUE` y `PERCENTAGE_OF_VALUE_PRORATED`): `percentage`, `minimum`, `minimumThreshold`, `minimumPerCargoUnit` y `minimumIncludesVat`.
  - La prorrateada cobra el porcentaje sobre `valor × saldo / recibido` (`PercentageOfValueProratedFormulaCalculator.cs:20-45`).
  - La no prorrateada lo cobra sobre el valor del lote completo.
- **Lo que no puede expresar:**
  - no hay una dimensión ni un parámetro que distinga el primer período de las renovaciones;
  - no hay tramos ni tope por valor;
  - el contexto de la fórmula (`B/Wms.Domain/Billing/FormulaContext.cs`) no recibe el número del período.

### 5.2 Método

- **Universo:** las mismas quincenas facturadas de importación del §4: 12.522 con valor de la mercancía y TRM, de 300 clientes.
- **Concentración de clientes:** 29 suman el 80 % de las quincenas y 141 tienen al menos 5.
- **Base:** `preciomercancia × TRM del día de ingreso`, que es el valor que hoy guarda V2 en el depósito.
- **Calibración por cliente:** el porcentaje que iguala lo facturado al cliente (neto de IVA) con su base, con un mínimo de $50.000 con IVA.
- **Fórmula prorrateada:** usa el saldo al cierre del día de inicio, el mismo criterio que construye BR-06-005 del plan P1. En el primer período sin salidas registradas se toma lo recibido.
- **Validación fuera de la muestra:** porcentajes calibrados con 2022–2023 y aplicados a 2024.

### 5.3 Resultados (todo el período, calibración dentro de la muestra)

| Escenario | Total | Primer período | Renovación | Facturas a ±10 % | Facturas a ±25 % |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Acuerdo por cliente, fórmula prorrateada** | **101,7 %** | **101,4 %** | **102,7 %** | 32 % | 59 % |
| Acuerdo por cliente, fórmula sin prorrateo | 101,1 % | 95,4 % | 119,1 % | 28 % | 52 % |
| Referencia, imposible hoy en V2: porcentaje distinto para primer período y renovación, prorrateado | 101,6 % | 101,2 % | 102,7 % | 33 % | 59 % |
| Referencia, imposible hoy en V2: lo mismo, sin prorrateo | 101,1 % | 101,2 % | 100,7 % | 28 % | 54 % |
| Tarifa base única, prorrateada (0,141 % neto), sin acuerdos | 103,0 % | 95,5 % | 126,7 % | — | — |
| Tarifa base única, sin prorrateo (0,120 % neto), sin acuerdos | 103,1 % | 83,3 % | 165,2 % | — | — |
| T1 tal como está (0,295 % neto, sin prorrateo; §4.6) | 205 % | 148 % | 372 % | — | — |

Todas las cifras son el porcentaje de lo que facturó el legacy.

### 5.4 Por tamaño de lote (quintiles del valor de la mercancía)

| Valor de la mercancía | Acuerdo por cliente, sin prorrateo | Acuerdo por cliente, prorrateado | Tarifa base única, prorrateada | T1 (§4.5, solo primer período) |
| --- | ---: | ---: | ---: | ---: |
| Hasta $25 M | 83,2 % | 84,2 % | 51 % | 56 % |
| $25 M – $49 M | 94,8 % | 95,7 % | 48 % | 92 % |
| $49 M – $151 M | 94,1 % | 95,1 % | 73 % | 108 % |
| $152 M – $279 M | 94,0 % | 94,8 % | 97 % | 176 % |
| Más de $279 M | 113,7 % | 113,8 % | 144 % | 273 % |

Los cortes de los quintiles del §4.5 son distintos porque aquel análisis solo tomaba primeros períodos.

### 5.5 Fuera de la muestra (calibrado con 2022–2023, aplicado a 2024)

| Escenario | Total | Primer período | Renovación |
| --- | ---: | ---: | ---: |
| Acuerdo por cliente, prorrateado | 88,1 % | 85,8 % | 94,8 % |
| Acuerdo por cliente, sin prorrateo | 91,8 % | 81,4 % | 123,3 % |

Hay 165 quincenas de 2024 de clientes sin historial previo, que no se pueden calibrar. Que el total quede por debajo del 100 % puede indicar alzas de tarifa en 2024.

### 5.6 Lectura

1. **V2 puede facturar como el legacy en el total, con su configuración actual,** si cada cliente tiene un acuerdo con un porcentaje calibrado y se usa la fórmula **prorrateada**. Queda a ±2 % dentro de la muestra y entre el 86 % y el 95 % fuera de ella.
2. **La fórmula prorrateada explica las renovaciones.** Con un solo porcentaje por cliente, las renovaciones quedan en el 103 %, igual que con una tarifa de renovación aparte, que hoy V2 no tiene. **No hace falta desarrollar esa tarifa.** Esto corrige la lectura del §4.4: mezclando clientes parecía que el saldo no explicaba la caída; cliente por cliente, sí la explica.
3. **El acuerdo por cliente explica el porcentaje decreciente** del §4.5: los clientes con lotes grandes tenían porcentajes más bajos. Por tamaño de lote queda entre el 84 % y el 114 %, frente al 51–144 % de una tarifa única. **No hacen falta tramos por valor.**
4. **Una tarifa única no alcanza**, ni prorrateada: el total cuadra, pero los lotes pequeños quedan en el 51 % y los grandes en el 144 %. La tarifa base solo debe cubrir a los clientes sin acuerdo.
5. **Las facturas una a una no se pueden reproducir:** solo un 32 % queda a ±10 %, con cualquier fórmula, incluida la referencia con tarifa de renovación. El legacy digitaba valores inconsistentes. La paridad alcanzable es en el total y por cliente, no por factura.
6. **Los porcentajes calibrados dependen de la base.** Valen sobre el valor que hoy se captura, el FOB del ingreso. Si el depósito pasa a guardar el CIF, cerca de un 3 % más alto en la mediana y un 13 % en el percentil 75 (§4.2), hay que calibrar sobre el CIF.

## 6. Conclusiones para decidir

1. **FOB o CIF es, sobre todo, una cuestión de significado.** En dinero cambia el total en un 0,7 %. Pesa en la póliza, el kárdex y la coherencia con las declaraciones aduaneras. Los datos respaldan que el levante es CIF, como en el legacy.
2. **La facturación de V2 puede igualar el total del legacy con su configuración actual (§5),** sin desarrollo. Las condiciones son:
   - **fórmula prorrateada:** los datos resuelven a su favor la decisión abierta de `DEC-025`. Con un porcentaje por cliente, las renovaciones quedan en el 103 %, frente al 119 % sin prorrateo; fuera de la muestra, 95 % frente a 123 %;
   - **acuerdos por cliente con porcentajes calibrados:**
     - 29 clientes concentran el 80 % de las quincenas;
     - 141 tienen al menos 5;
     - con acuerdos, el sesgo por tamaño de lote baja al 84–114 %.
3. **La tarifa base actual es el riesgo económico.** T1 (0,295 % neto, **sin** prorrateo) es lo que lleva al 205 %. Todo cliente sin acuerdo factura de más en las renovaciones y en los lotes grandes, y de menos en los lotes pequeños. Una tarifa base prorrateada cercana al 0,141 % neto cuadra el total, pero no corrige el tamaño: queda entre el 51 % y el 144 %. Por eso la tarifa base solo debe cubrir lo marginal.
4. **No hacen falta las capacidades que la primera versión de este documento daba por necesarias:** una tarifa distinta para las renovaciones, tramos por valor o un porcentaje combinado con un cargo por camión. Las referencias con tarifa de renovación del §5.3 no mejoran el resultado.
5. **La paridad alcanzable es por cliente y en el total, no por factura:** solo un 32 % de las facturas queda a ±10 % con cualquier fórmula.
6. **FOB o CIF condiciona la calibración.** Los porcentajes valen sobre la base con que se calibran. Hay que decidir la base antes de cargar los acuerdos, y si se pasa a CIF, calibrar sobre CIF.
7. **Staging ya está expuesto:** los depósitos nuevos de clientes sin acuerdo se facturan con T1 completo en cada renovación.

## 7. Decisiones pendientes

| # | Decisión | Fundamento |
| --- | --- | --- |
| 1 | ¿Qué valor es la base del cobro por porcentaje: FOB (lo que hoy se captura en el depósito) o CIF? | §4.3: el historial no decide; §4.6: impacto del 0,7 % |
| 2 | ¿Cómo se rotula y se pide el valor del levante: CIF, como en el legacy, o FOB? ¿Sobre cuál se liquida la póliza? | §2, §4.2 |
| 3 | ¿El depósito guarda los dos valores, FOB del ingreso y CIF, o uno solo con un nombre inequívoco? | §3 |
| 4 | ¿Se permite corregir el valor de un depósito confirmado, con motivo y recálculo? | §3 |
| 5 | **¿Se adopta la fórmula prorrateada para el almacenamiento (`DEC-025`)?** Los datos la respaldan | §5.3, §5.5 |
| 6 | **¿Facturación valida los porcentajes por cliente calibrados con los datos, empezando por los 29 que concentran el 80 %, contra sus convenios reales?** | §5.2, §5.6 |
| 7 | **¿Con qué tarifa base (prorrateada y menor que T1) se cobra a los clientes sin acuerdo?** | §5.3: una base única prorrateada cerca del 0,141 % neto cuadra el total, pero no el tamaño |
| 8 | ¿El valor del levante se registra una sola vez por levante o se reparte entre sus productos? | §3 |
| 9 | ¿Qué valor se captura en exportación e inspección, y alguno de esos convenios cobra por porcentaje? | §3 |
| 10 | Revisar T1 (`DEC-041`) antes de facturar en producción, junto con la carga de los acuerdos y una facturación en paralelo de un mes | §4.6, §5 |

## 8. Límites

- **Es inferencia estadística sobre valores digitados.** No reemplaza el cotejo con los convenios firmados, las declaraciones de importación (FOB, flete, seguro y CIF) ni la confirmación de Facturación y Comercio Exterior sobre qué digitaban.
- **La simulación** supone T1 por período quincenal con el IVA sumado al porcentaje, como se cargó en staging. Si el 0,295 % fuera mensual, los totales cambian.
- **Excluidos:** los períodos de 90 y 180 días no entran en los porcentajes, y los 383 períodos en $0 no entran en los cocientes.
- **«Saldo al inicio»** = lo recibido menos las salidas hasta las 23:59:59 del día de inicio, el criterio de `facturarciigo.php:119-145`. En 3.272 primeros períodos no hay saldo registrado (salidas con fecha anterior o igual al inicio).
- **Equivalencia supuesta:** que el valor del depósito en V2 equivalga a `preciomercancia` vale para los migrados. En los nuevos lo digita báscula sin decir si es FOB o CIF.
- **El volcado** llega hasta junio de 2024 (`DEC-040`).
- **La calibración por cliente del §5 se hizo, en lo principal, dentro de la muestra:** con un solo porcentaje por cliente, el total cuadra casi por construcción. Lo que la valida es que el reparto entre primer período y renovación, y el reparto por tamaño de lote, no estaban forzados, y la prueba fuera de la muestra (2024). Los porcentajes que salen son un punto de partida para que Facturación los valide, no tarifas para cargar tal cual.

## 9. Método (para repetirlo)

1. Se arrancó el contenedor local `legacy-mariadb` (MariaDB 10.11, volumen `legacy-mariadb-data`) y se detuvo al terminar.
2. Las consultas se ejecutaron con `db_legacy/trabajo/consultas/exportar.py`, que lee la credencial local sin mostrarla.
3. Se extrajeron tres conjuntos:
   - por período facturado: valor, fechas, TRM del ingreso y de la factura, períodos previos y suma de levantes (total y registrados hasta la fecha de la factura);
   - por período: cliente (Id numérico), peso, cantidad recibida, salidas hasta el inicio y nacionalizado;
   - por depósito: valor del ingreso y suma de levantes en dólares.
4. El análisis se hizo con scripts de Python sobre esos CSV, en un directorio temporal fuera del repo.
5. La simulación del §5 reutilizó esos mismos CSV, sin consultas nuevas.
6. Los CSV y los scripts **no se versionan**, porque contienen Ids de clientes y depósitos. Para repetirlo, se vuelven a ejecutar las consultas descritas sobre el volcado, con la aprobación del usuario (`DEC-007`).
