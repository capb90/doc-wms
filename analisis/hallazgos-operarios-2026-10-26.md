# Hallazgos de los operarios en staging: análisis

> **Fecha:** 26 de octubre de 2026.
> **Fuente:** «Informe de hallazgos y ajustes requeridos en el nuevo sistema», de Bodegas Asociadas, sobre los módulos de Báscula y Comercio Exterior. El usuario lo recibió y pidió revisarlo antes de desplegar la fase 13.
> **Qué se revisó:**
> - el código de `develop` (BE `dafd573`, FE `d838535`);
> - el build que hay en staging (BE `044be08`, FE `4ca4e0a`, del 2026-10-08), que es el que probaron los operarios;
> - el código del legacy;
> - `contexto/decisiones.md` y la auditoría de paridad.
>
> Solo lectura: no se cambió código ni datos.
> **Estado:** decisiones respondidas el 2026-10-26 (`DEC-057`, §6).
> **Sin datos de personas:** los terceros del ejemplo del informe no se nombran (`DEC-007`).

## 1. Resumen

Los operarios probaron una versión de staging de hace 18 días. El informe tiene 15 hallazgos:

| Clasificación | Cuántos | Hallazgos |
| --- | ---: | --- |
| **Ya corregido en `develop`**: sale con la fase 13 | 1 | H11 |
| **La función existe**: falta capacitación | 3 | H1, H4, H5a |
| **Problema de datos**: catálogo migrado | 1 | H6 |
| **Brecha real** | 5 | H3, H5b, H7, H13, H14 |
| **Choca con una decisión tomada**: requiere decidir | 5 | H2, H5c, H10, H12, H15 |

Además, la revisión encontró una brecha que el informe no menciona: V2 no exige el **manifiesto DIAN** al confirmar un depósito de importación, y el legacy sí (§4, H2).

## 2. Báscula

| # | Hallazgo | Qué hace V2 hoy | Legacy | Clasificación |
| --- | --- | --- | --- | --- |
| H1 | Tipo de vehículo obligatorio | **Ya es obligatorio en Báscula, en los tres flujos.** La tarjeta «Camión y conductor» lo pide y «Guardar» no avanza sin él (`CompleteEntryInfo.vue:86-97`; `weighbridge/index.vue:638-645`). Es opcional solo en Vigilancia, para que la entrada sea rápida. Los vehículos migrados llegan sin tipo, así que el primer pesaje lo pide | Opcional (`registrarvehiculo.php:323-337`) | **Existe.** Exigirlo en Vigilancia choca con `DEC-010` y `DEC-056` («Vigilancia y Báscula no agregan controles»). Mejora menor posible: que el backend lo exija también en Solo báscula y Salida, como ya lo hace el frontend |
| H2 | Número de manifiesto obligatorio al registrar el ingreso | En Báscula es opcional («N.º de manifiesto (opcional)», `StorageServiceForm.vue:1028-1052`). Se vuelve obligatorio por camión cuando CE confirma el depósito (`DepositConfirmationRequirements.cs:97-106`) | Opcional en Báscula (`registrarentradabascula.php:832-834`). Obligatorio solo en la pantalla de varios documentos | **Choca con una decisión:** el plan de paridad (P2, BAS-01) lo dejó opcional en Báscula y exigido al confirmar. Exigirlo en Báscula es más estricto que el legacy |
| H3 | Cálculo de pesos como el legacy (indicador, tara, manifiesto, mercancía) | El neto es la diferencia entre el pesaje de entrada y el de salida (`CycleNetWeights.cs:75-119`). **Con un solo pesaje (perecederos, inspección o sin segundo pesaje) no hay neto ni tara.** El peso del manifiesto no se usa para calcular nada: solo se compara con el neto (±2 %) y reparte un neto compartido | Un solo pesaje: P. mercancía = P. manifiesto, y T. vehículo = P. indicador − P. mercancía (`registrarentradabascula.php:643-649`). Ejemplo del informe: 21.380 − 13.700 = 7.680 | **Brecha real.** Ninguna decisión cubre deducir la tara del manifiesto. Hay que decidir la regla |
| H4 | Editar la fecha de ingreso (camión que llegó la noche anterior) | **Existe, en dos pasos:**<br>1. Vigilancia usa «Corregir ingreso» → «Fecha y hora de ingreso» desde su historial (`CorrectEntryLogDialog.vue`; rol Vigilancia o Admin; con motivo).<br>2. Báscula o CE corrigen la fecha del depósito con «Cambiar» al registrar, o con «Editar fecha de ingreso» en el detalle del ciclo o del depósito. Recalcula la facturación.<br>Báscula no puede ir antes del ingreso de Vigilancia sin que Vigilancia lo corrija primero | Editable al registrar y al modificar | **Existe** (`DEC-010` (4), `DEC-012` y `DEC-051` / BR-04-002). Falta capacitación sobre el orden: primero Vigilancia, después el depósito |
| H5a | Eliminar un tiquete con error | **Existe.** «Anular pesaje», con motivo, en Báscula › Historial y en el Detalle del ciclo. Antes del cobro existe «Descartar operación» en «Recuperar». El botón de anular en la tarjeta del camión con el ciclo abierto llega con `develop`. Al anular, la factura de báscula se anula si está en Borrador; si no, va a revisión de Facturación | «Eliminar» como borrado lógico, sin guardas | **Existe.** Falta capacitación |
| H5b | Tiquete en cero según el convenio | V2 rechaza el total en 0: «El total a pagar debe ser mayor a cero.» (`ProcessStoragePaymentHandler.cs:179-182`). Rechaza también la tarifa en 0. El monto que Facturación sobrescribe debe ser mayor que 0 | Permitía tiquetes en ceros (el informe tenía filtro «en ceros») y cobros no tarifados | **Brecha real**, cercana a BR-02-003 (abierta). Hoy solo se resuelve con «Por facturar» y que Facturación anule la factura |
| H5c | Editar el cobro de un tiquete ya guardado (facturar o no) | Báscula corrige solo pesos, hora, observación y datos del camión y del conductor. El cobro no se edita: se anula y se repite. Facturación cambia el destinatario o el monto mientras la factura está en Borrador | «Editar» reescribía el pesaje y el recibo, valor incluido | **Choca con una decisión:** `DEC-050` (BR-02-010) y `DEC-019` D-2 |

## 3. Comercio Exterior

| # | Hallazgo | Qué hace V2 hoy | Legacy | Clasificación |
| --- | --- | --- | --- | --- |
| H6 | Al registrar el ingreso aparecen importadores, no clientes | Los selectores de cliente (Báscula, «Asignar cliente» en CE, recepción) listan solo terceros con rol **Cliente**, y la factura va siempre a ese cliente. **Causa:** la migración dio a cada `cliente` del legacy los roles Cliente **e** Importador (`CustomersImporter.cs:42`). Por eso la lista de clientes es la de importadores: 1.053 y 1.053. Las agencias quedaron solo como agencia | El ingreso no tenía cliente, solo importador. En la factura de almacenamiento, «Cliente Factura» era texto libre precargado con el importador | **Datos y capacitación.** CE puede agregar el rol Cliente desde «Terceros» (`StakeholderBusinessRoles.vue`), y desde ahí ese tercero aparece en todos los selectores. **Brechas menores:**<br>• no hay «crear cliente» rápido en Báscula ni en CE;<br>• BR-06-007 sigue abierta: el diálogo para cambiar el destinatario de la factura existe pero no está montado |
| H7 | Cartas porte en mercancías con arrastre: tomar la carta porte correcta y no la de otra mercancía con el mismo número | Báscula busca el depósito abierto por número y tipo de documento, sin mirar cliente, transportadora ni placa (`StorageDocumentLookup.cs:26-43`). Si hay uno solo, asocia el camión de forma automática. **Un depósito sin fecha de documento casa con cualquier fecha** (`StorageDocumentMatcher.cs:63-71`). El formulario carga los productos, el cliente y el importador del otro depósito, en solo lectura, y no ofrece «es otro documento, crear depósito nuevo» | El operario elegía de una lista de sugerencias que mostraba la transportadora. Si no elegía ninguna, se creaba un ingreso nuevo | **Brecha real**, que choca en parte con la decisión P1 del plan de paridad (asociación automática por número y tipo). **Escenario:** el cliente A tiene la carta porte «123» abierta sin fecha. Llega un remolque de otra transportadora con la «123» del cliente B. El camión de B entra al depósito de A (stock y factura de A) y la fecha de B queda escrita en A. Conviene confirmar con los operarios qué llaman «arrastre»: remolque (unidad de arrastre) o varios camiones con un mismo documento |

## 4. Tarjeta del depósito

En todos estos hallazgos la tarjeta de staging y la de `develop` son iguales, salvo en H11.

| # | Hallazgo | Qué hace V2 hoy | Legacy | Clasificación |
| --- | --- | --- | --- | --- |
| H10 | Quitar «Transportadora» | La imprimen las tres tarjetas (importación, exportación e inspección). Se agregó a propósito en WMS-11 (commit `925ec8c`). El caso QA F5-ETI-001 la espera | No la imprimía | **Choca con una decisión** (WMS-11). El cambio es chico |
| H11 | Ampara y Saldo sin decimales (730.00) | **Corregido en `develop`** (DEF-F11-031, BE `3cbf181`): 730,00 sale «730» y 1.350 sale «1.350». Una cantidad fraccionaria sigue saliendo con hasta 2 decimales (730,5), lo que es correcto para unidades como tonelada o litro | Imprimía el número tal cual | **Ya corregido en `develop`.** Sale con la fase 13 |
| H12 | Tarjeta por vehículo o por toda la mercancía | V2 tiene solo la tarjeta del depósito completo | Tenía las dos: «Adhesivo por vehículo» (`adhesivovehiculo.php`) | **Choca con una decisión:** `DEC-051` decidió una tarjeta por depósito y no construir la de vehículo (BR-04-012) |
| H13 | La fecha de la carta porte es la de ingreso, no la del documento | La tarjeta imprime `ws.EntryDate` junto a la carta porte (`LabelGenerationService.cs:201`, `:422` y `:626`). **V2 sí guarda la fecha del documento** (`ServiceRecord.DocumentDate`), capturada en Báscula y migrada del legacy, pero la tarjeta no la usa. También dice siempre «Carta Porte» aunque el documento sea de otro tipo | Imprimía `tipo de documento: número (fecha del documento)` | **Brecha real.** Es un error que ninguna decisión cubre. La corrección es chica |
| H14 | Nombre de la mercancía duplicado («CEBOLLA FRESCA CEBOLLA FRESCA») | `DocumentProductLine.For` concatena nombre y descripción (`DocumentProductLine.cs:17`). Báscula guarda el nombre como descripción cuando el producto del catálogo no tiene descripción (`StorageServiceForm.vue:747-749`). También se duplica en el PDF del depósito y en la guía de salida | Un solo texto | **Brecha real.** La corrección es chica: no repetir la descripción cuando es igual al nombre |
| H15 | Quitar la columna «Unidad» | La tabla es Ampara · Saldo · Unidad · Embalaje · Mercancía (WMS-18) | Ampara · Saldo · Mercancía, con el embalaje dentro del texto | **Choca con una decisión** (`DEC-015`: unidad y embalaje como campos separados). Ojo: con unidades mixtas en un depósito, quitar la unidad deja ambiguo el Ampara |

La «Fecha Ingreso 2026-10-07 01:44:39» de la foto está bien: es la hora de Colombia en que se prepararon los datos de práctica (`informe-fase-5.md`).

## 5. Lo que esto implica para la fase 13

1. **Desplegar `develop` resuelve H11** y trae el botón de anular en el ciclo abierto (H5a).
2. **Antes de abrir staging a los operarios conviene corregir H7, H13 y H14.**
   - H7 es la más seria: mezcla mercancía de dos clientes en un depósito.
   - H13 y H14 son cambios chicos en la tarjeta, el PDF del depósito y la guía.
3. **Capacitación** (H1, H4, H5a y H6): una nota corta para los operarios.
   - tipo de vehículo en Báscula;
   - corregir el ingreso en Vigilancia y luego la fecha del depósito;
   - anular un pesaje y descartar una operación;
   - agregar el rol Cliente en Terceros.
4. **Decisiones del usuario o del negocio:**
   - **Brechas que necesitan una regla:** H3 (tara con un solo pesaje), H5b (tiquete en cero por convenio) y H7 (cómo se elige el depósito).
   - **Hallazgos que contradicen decisiones tomadas:** H2, H5c, H10, H12 y H15.
   - **Manifiesto DIAN:** si se exige al confirmar un depósito de importación.

## 6. Decisiones (2026-10-26, `DEC-057`)

| # | Hallazgo | Respuesta |
| --- | --- | --- |
| 1 | H7, carta porte | El operario confirma el depósito; nada se asocia solo |
| 2 | H3, pesos | Los cuatro campos del legacy siempre en pantalla; tara = indicador − manifiesto |
| 3 | H5b, tiquete en cero | Solo si el convenio lo fija en $0; sin número fiscal |
| 4 | H13 y H14, tarjeta | Tipo, número y fecha del documento; sin repetir la descripción |
| 5 | H2, manifiesto | Obligatorio (número y peso) al registrar un ingreso a depósito |
| 6 | Manifiesto DIAN | Requisito para confirmar un depósito de importación |
| 7 | H5c, editar el cobro | No: se mantiene `DEC-050`; se monta el cambio de destinatario (BR-06-007) |
| 8 | H10, transportadora | Se quita de las tres tarjetas |
| 9 | H12, tarjeta por vehículo | Se construye, además de la del depósito |
| 10 | H15, columna Unidad | Tarjeta como el legacy: Ampara · Saldo · Mercancía (embalaje en el texto) |
| 11 | Orden | Plan cerrado nuevo antes de la fase 13; nota de capacitación mientras tanto |
