# Propuesta de convenios calibrados por cliente y su validación por Facturación

> **Fecha:** 2026-10-27 (hora de Colombia). **Ejecutor:** agente (Opus 5.5). **R:** 2026-10-27; corte simulado 2026-10-26 (S3).
> **Plan:** `planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md` §3, fase 2 (`DEC-043`; método de `DEC-029` §7.6 y del análisis `analisis/analisis-fob-cif-legacy-v2-2026-10-24.md` §5).
> **Partida:** BE `911399c` en `develop`, limpio; docs `28eea7e` en `main`, limpio. Sin cambios de código.
> **Aprobación para consultar el volcado** (`DEC-029` §7.6): el usuario, en la sesión del 2026-10-27, antes de la primera consulta. Solo `SELECT` sobre `legacy-mariadb` (`bodegas`, de `backupBodegas.sql`).
> **Datos personales** (`DEC-007`): este resumen lleva conteos e ids del legacy. Los nombres y los documentos están solo en la hoja `db_legacy/trabajo/convenios/propuesta-convenios-v1.xlsx`. Las consultas están en `db_legacy/trabajo/consultas/convenios/` y los resultados intermedios y los scripts, en `db_legacy/trabajo/convenios/`.

## Veredicto

**Pasos 1 a 5: hechos. Criterio OK: pendiente del checkpoint de Facturación (paso 6).**

- La hoja tiene **43 clientes**: los 24 con depósitos vivos en el v4 y los 29 que concentran el 80 % de las quincenas (10 están en los dos grupos).
- **40 tienen porcentaje calibrado.** Los otros 3 tienen depósitos vivos pero ninguna quincena facturada: quedan con la tarifa base, salvo que Facturación fije su porcentaje.
- **Validación fuera de la muestra:** calibrado con 2021–2023 y aplicado a 2024, el universo factura el **86,3 %** de lo que facturó el legacy (análisis §5.5: 88,1 %, con todos los clientes).
- Falta lo que devuelve Facturación: la hoja validada y la tarifa base (§5). Hasta entonces, la fase 4 sigue sin convenios ni `open-billing` (S11).

## 1. Método (S5)

| Elemento | Cómo se tomó |
| --- | --- |
| Períodos | `facturaciigo` en estado `facturada`, importación (`id_modalidad = 1`), de 16 días (las quincenas), con valor de la mercancía, TRM y valor facturado mayor que 0 |
| Cliente | `ingreso.id_importador`, el mismo cliente que lleva el depósito en V2 (`id_cliente` de `11_depositos.csv`) y el que factura `facturarciigo.php` |
| Base | `ingreso.preciomercancia × TRM del día de ingreso`, con la misma subconsulta de `tasa_cambio` que la consulta F6-03 del v4 |
| Prorrateo | Saldo al cierre del día de inicio (`facturarciigo.php:119-145`) ÷ recibido, entre 0 y 1. En un primer período sin saldo registrado se toma lo recibido |
| Simulación de V2 | `PercentageOfValueProratedFormulaCalculator`: neto = máx(% × base prorrateada, mínimo neto), con el mínimo de $50.000 con IVA llevado a neto ($42.016,81) y el IVA del 19 % aparte |
| Lo facturado | `valor_facturaciigo`, que el legacy guarda con IVA; neto = valor ÷ 1,19 |
| Porcentaje por cliente | El que iguala la simulación con lo facturado neto, en todo el período (bisección) |
| Báscula | Por cliente, las líneas de `detallerecibo` del servicio 1 (báscula) de sus recibos, y cuántas en $0 |

**Conteos del universo frente al análisis:**

| Concepto | Esta fase | Análisis §5.2 |
| --- | ---: | ---: |
| Períodos facturados de importación | 13.315 | 13.314 |
| Quincenas | 12.906 | 12.905 |
| Quincenas con valor, TRM y facturado > 0 | 12.523 | 12.522 |
| Clientes con quincenas | 300 | 300 |
| Clientes que concentran el 80 % | 29 | 29 |
| Clientes con al menos 5 quincenas | 142 | 141 |

## 2. Cobertura

| Concepto | Cantidad |
| --- | ---: |
| Clientes en la hoja | 43 |
| — con depósitos vivos | 24 |
| — entre los 29 | 29 |
| — en los dos grupos | 10 |
| Clientes con porcentaje calibrado | 40 |
| Quincenas del universo | 10.322 de 12.523 (82,4 %) |
| Depósitos vivos (v4) | 128 |
| — de clientes con porcentaje calibrado | 90 |
| — de los 3 clientes sin quincenas (ids 464, 1058 y 1059) | 38 (36 del id 464) |

## 3. Porcentajes calibrados

Neto de IVA, por quincena, fórmula prorrateada (40 clientes):

| Mínimo | p25 | Mediana | p75 | Máximo |
| ---: | ---: | ---: | ---: | ---: |
| 0,0524 % | 0,1762 % | 0,2803 % | 0,3222 % | 2,0048 % |

- Ningún cliente queda con todo al mínimo.
- Las notas del cálculo, en la hoja, marcan:
  - 1 porcentaje atípico, de más del 1 % (id 773);
  - 2 clientes con menos de 5 quincenas (ids 93 y 995);
  - 1 cliente cuyo número de identificación se repite en otro cliente del legacy (id 925). En la fase 3, si `GET stakeholders?search=` no da exactamente un tercero, su convenio no se carga (S7).

**Pista de báscula** (S5): 4 clientes con todos sus recibos de báscula en $0, 26 con algún cobro y 13 sin recibos a su nombre. Es solo una pista, porque el $0 también salía en los repesajes.

## 4. Validación

| Escenario | Quincenas | Total | Primer período | Renovación | Facturas a ±10 % | Facturas a ±25 % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dentro de la muestra, universo de la hoja | 10.322 | 100,0 % | 100,0 % | 100,0 % | 30,5 % | 57,7 % |
| Dentro de la muestra, todos los clientes | 12.523 | 100,0 % | 99,9 % | 100,4 % | 32,6 % | 59,4 % |
| **Fuera de la muestra (2021–2023 → 2024), universo de la hoja** | 1.483 | **86,3 %** | 82,8 % | 93,9 % | 32,0 % | 64,9 % |
| Fuera de la muestra, todos los clientes | 1.745 | 87,0 % | 84,7 % | 93,8 % | 33,1 % | 62,4 % |

- Todas las cifras son el porcentaje de lo que facturó el legacy, neto de IVA.
- Hay 161 quincenas de 2024 de clientes sin historial previo: no entran en la validación fuera de la muestra (análisis: 165).
- **Lectura:** igual que en el análisis §5.6. La paridad es por cliente y en el total, no por factura. Que 2024 quede por debajo del 100 % puede indicar alzas de tarifa en 2024.

**Referencias para la tarifa base (S4):** un solo porcentaje prorrateado que iguala lo facturado:
- por todos los clientes: **0,1363 %** neto (análisis §5.3: 0,141 %);
- por los clientes que no están en la hoja (2.201 quincenas): **0,1619 %** neto.

T1 actual es el 0,295 % neto sobre el lote completo (`DEC-041`).

## 5. Checkpoint de Facturación (paso 6)

**Qué devuelve Facturación:** la misma hoja, guardada como `db_legacy/trabajo/convenios/propuesta-convenios-v1-validada.xlsx`, sin cambiar los nombres ni el orden de las columnas:

| Pestaña | Qué llena |
| --- | --- |
| Convenios | Por cliente: «Validado» (sí o no), «% acordado» (neto de IVA, en la misma unidad que el calibrado; obligatorio con «Validado = sí»), «Báscula sin cobro» (sí o no) y «Observaciones» |
| Tarifa base | El porcentaje de la tarifa base, neto y prorrateado, o «sí» en dejar T1 como hoy |

Solo se carga lo que diga «Validado = sí» (S6). Los clientes no validados facturan con la tarifa base.

**Resultado de la validación:** *pendiente*. Cuando llegue la hoja, se completa aquí:

| Concepto | Cantidad |
| --- | ---: |
| Convenios validados | [pendiente] |
| No validados | [pendiente] |
| Con «Báscula sin cobro» | [pendiente] |
| Tarifa base de los demás | [pendiente: % de Facturación o T1] |

## 6. Tiempos

| Paso | Tiempo |
| --- | --- |
| Extracción de los períodos (`01_periodos.sql`) | 20,6 s |
| Extracción de la báscula (`02_bascula.sql`) | 0,2 s |
| Calibración y validación (`calibrar.py`) | 0,7 s |
| Hoja (`armar_hoja.py`) | menos de 1 s |

## 7. Desviaciones

1. **Saldo al inicio:** 3.850 primeros períodos sin saldo registrado, frente a 3.272 del análisis §8; se toma lo recibido, como dice el §5.2. La diferencia probablemente viene de los filtros por estado (productos y salidas eliminados): el análisis no deja sus consultas (§9). Ninguna renovación queda sin saldo.
2. **Dentro de la muestra el total da 100,0 %, no 101,7 %:** el porcentaje se calcula para igualar la simulación de V2 con el mínimo incluido, como pide S5. El análisis no deja sus scripts (§9), y la cifra fuera de la muestra, que es la que valida, queda cerca: 87,0 % frente a 88,1 %.
3. **«% acordado» obligatorio con «Validado = sí»:** el plan no dice qué hacer si queda vacío. La hoja lo pide así para que la fase 3 no tenga que suponer un valor.
4. **Calibración para la validación: 2021–2023, no 2022–2023.** Entran también las 4 quincenas que empiezan en 2021 (todo lo anterior a 2024).
5. **`armar_hoja.py` corre sin `python3 -I`,** porque `openpyxl` está en el site-packages del usuario. Es un script propio, sin archivos descargados.
