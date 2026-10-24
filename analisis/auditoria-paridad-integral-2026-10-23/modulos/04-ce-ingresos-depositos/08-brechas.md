# 04 — Registro de brechas

> Auditoría estática del 2026-10-23 (AG-04). Prefijos: `L/` = `bodegas-legacy/`, `B/` = `Backend/wms-api/`, `F/` = `Frontend/wms/app/`.
> Antes de registrar cada brecha se revisaron `docs/qa/resultados/defectos/INDICE.md` (fichas DEF-F5-*, DEF-F11-*), `docs/planes/migracion-staging/resultados/defectos/` y `docs/contexto/estado.md` §4. Donde ya había antecedente se cita.
> No se registran como brecha: las diferencias con decisión (matriz, `DIFERENCIA_INTENCIONAL`) ni el pendiente FOB/CIF del valor de la mercancía, que ya existe (`docs/contexto/estado.md` §4 n.º 8, `docs/analisis/revision-fob-cif-migracion-v2-2026-10-08.md`; se cita en CF-L124).

## Resumen

| ID | Capacidad | Título | Categoría | Criticidad |
| --- | --- | --- | --- | --- |
| BR-04-001 | CF-L260 | Un camión tardío a un depósito cerrado por agotamiento crea otro depósito | REGLAS_NEGOCIO | MEDIA |
| BR-04-002 | CF-L136, CF-V043 | La fecha de ingreso no puede ir antes del ingreso en Vigilancia (DEC-012 dice «sin límite hacia atrás») | REGLAS_NEGOCIO | MEDIA |
| BR-04-012 | CF-L141.a | No existe la etiqueta por vehículo | FRONTEND / BACKEND | MEDIA |
| BR-04-003 | CF-L140.b, CF-LX04-01 | El aviso y la pantalla de abandono abren en «En alerta» y ocultan los vencidos | FRONTEND | BAJA |
| BR-04-004 | CF-L141.b | El PDF de la etiqueta no muestra el número de impresión | REGLAS_NEGOCIO | BAJA |
| BR-04-005 | CF-L124, CF-L136 | Volumen y condiciones del ingreso sin destino; observaciones solo en Borrador | REGLAS_NEGOCIO | BAJA |
| BR-04-006 | CF-L130, CF-L131 | Listas de empaque: sin aviso de archivo repetido, importador sin rol, eliminación más estricta | REGLAS_NEGOCIO | BAJA |
| BR-04-007 | CF-V047 | La validación del depósito contra la plantilla no tiene camino en la UI | INTEGRACION | BAJA |
| BR-04-008 | CF-L133, CF-V047 | `IImportDepositDetailDto` declara 9 campos que el backend no envía | CONTRATOS_API | BAJA |
| BR-04-009 | CF-L138, CF-L139 | Sin seriales por unidad ni su edición, sin decisión fuera de Colmotores | REGLAS_NEGOCIO | BAJA |
| BR-04-010 | CF-L140.a, CF-LX04-01, CF-V084 | Diferencias del flujo de abandono sin decisión en §A | REGLAS_NEGOCIO | BAJA |
| BR-04-011 | CF-L122, CF-L133, CF-L134 | Filtro de manifiesto sobre el del camión; EXP e INSP sin filtro por placa | FRONTEND / BACKEND | BAJA |

Por criticidad: CRÍTICA 0 · ALTA 0 · MEDIA 3 · BAJA 9.

---

### BR-04-001 — Un camión tardío a un depósito cerrado por agotamiento crea otro depósito

- **ID funcional:** CF-L260 (RN-023); relacionado con DEC-013.
- **Descripción:** en el legacy, el listado de depósitos devuelve a `activo` un depósito `facturado` mientras quede cantidad o peso amparado por entrar. En V2 no hay estado «facturado», pero el depósito se **cierra solo** cuando el cargue deja todo su stock en cero. Si después llega otro camión con el mismo documento y Comercio Exterior no ha cerrado el ingreso de camiones, báscula no lo asocia (solo busca depósitos `Draft`/`Confirmed`) y, como el ingreso de camiones no está cerrado, **crea un depósito nuevo** con otro número.
- **Comportamiento esperado:** el camión tardío entra al mismo depósito, a su stock y al recálculo de su período (DEC-013), o queda documentado que un depósito agotado no recibe más camiones.
- **Comportamiento actual:** nuevo depósito `Draft` con nuevo consecutivo, nueva factura del período (con su mínimo) y su propio plazo de abandono.
- **Capa:** backend (báscula y cargue).
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `B/Wms.Application/Warehouse/Commands/LoadingOrder/ExecuteLoadingOrderCommandHandler.cs:275-281` (cierre automático); `B/Wms.Application/Weighbridge/Common/Services/StorageDocumentLookup.cs:27-37` (candidatos solo `Draft`/`Confirmed`), `:73-118` (bloqueo solo si `TruckEntriesClosedAt != null`); `B/Wms.Application/Weighbridge/Commands/Storage/Initiate/InitiateStorageWeighingHandler.cs:272`, `:352-360` (sin candidato → primer camión); `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:363-371` (solo la reversión reabre). Legacy: `L/modulos/mod_depositos/listardepositos.php:507-521`, `:562-576`. Sin ficha DEF ni pendiente en `estado.md`.
- **Impacto:** un mismo documento queda partido en dos depósitos: doble mínimo de almacenamiento, dos plazos de abandono y trazabilidad aduanera separada. Probable en perecederos o despachos rápidos (todo sale antes de que llegue el último camión).
- **Criticidad:** MEDIA — escenario específico, con efecto en facturación y control aduanero.
- **Dependencias:** módulo 02 (báscula), módulo 03 (cargue), módulo 06 (recálculo).
- **Acción recomendada:** confirmar con el negocio. Si el documento sigue abierto, reabrir el depósito `Closed` por agotamiento (como `ReopenAfterReversal`) al asociar el camión; o registrar la decisión de no hacerlo.
- **Criterio verificable de resolución:** con un depósito confirmado, despachado hasta stock 0 (cerrado) y sin cierre del ingreso de camiones, un nuevo camión con el mismo documento queda en el **mismo** `WarehouseStorageNumber` y el depósito vuelve a `Confirmed`; o existe una `DEC-nnn` que lo descarta.

### BR-04-002 — La fecha de ingreso no puede ir antes del ingreso en Vigilancia

- **ID funcional:** CF-L136, CF-V043.
- **Descripción:** DEC-012 dice que Báscula y Comercio Exterior corrigen la fecha de ingreso «sin límite hacia atrás y nunca hacia el futuro». El código la limita a la **estadía del primer camión**: no antes de su ingreso en Vigilancia (al minuto) ni después de su salida.
- **Comportamiento esperado:** según DEC-012, cualquier fecha pasada.
- **Comportamiento actual:** 400 «La fecha de ingreso del depósito no puede ser anterior al ingreso del camión en Vigilancia (…)» o «…posterior a la salida del camión».
- **Capa:** backend (dominio) y frontend (límites del selector).
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:194-219`; `B/Wms.Common/Time/OperationalDateRules.cs` (`EnsureWithinTruckStay`); `B/Wms.Application/ForeignTrade/Commands/CorrectDepositEntryDate/CorrectDepositEntryDateCommandHandler.cs:29-36`; `F/features/foreign-trade/components/EditDepositEntryDateDialog.vue:53-60`. QA aceptó el comportamiento restrictivo (`docs/qa/fase-05-comercio-exterior.md:135-136`; `docs/qa/resultados/F5-informe-2026-10-02.md:96-97`; `F11-informe-S5-2026-10-06.md:103`). Legacy: `L/modulos/mod_depositos/modificardeposito.php:56-60` (sin límite).
- **Impacto:** la fecha rige el plazo de abandono, la TRM y el inicio del período (DEC-012). Para ir más atrás hay que corregir antes el ingreso de Vigilancia (módulo 03). Contradicción entre la decisión vigente y el código, aunque QA validó el código.
- **Criticidad:** MEDIA — regla de una decisión documentada, con impacto aduanero y de facturación en casos de corrección.
- **Dependencias:** módulo 03 (corrección de Vigilancia), módulo 02 (misma regla en báscula).
- **Acción recomendada:** confirmar con el usuario cuál manda y actualizar `DEC-012` o el código (no reabrirla sin consulta: DEC-002).
- **Criterio verificable de resolución:** `decisiones.md` y `WarehouseStorage.CorrectEntryDate` dicen lo mismo (texto de DEC-012 actualizado, o una fecha anterior al ingreso de Vigilancia aceptada con motivo).

### BR-04-012 — No existe la etiqueta por vehículo

- **ID funcional:** CF-L141.a.
- **Descripción:** el legacy ofrece, junto a la etiqueta del depósito, un botón por placa que imprime la etiqueta con lo que trajo ese camión (`adhesivovehiculo.php`). En V2 los tres endpoints de etiqueta reciben solo el id del depósito y la acción.
- **Comportamiento esperado:** poder rotular la mercancía de cada camión en depósitos de varios camiones, o decisión que lo descarte.
- **Comportamiento actual:** una sola etiqueta por depósito con todas las placas.
- **Capa:** backend y frontend.
- **Categoría:** FRONTEND / BACKEND.
- **Evidencia:** legacy `L/modulos/mod_depositos/adhesivos.php:370` (botones por vehículo), `:574-575`; `L/modulos/mod_depositos/adhesivovehiculo.php:284-370`. V2: `B/Wms.Api/Controllers/v1/ForeignTradeController.cs:280`, `:739-740`, `:857` (firmas sin vehículo ni camión); `B/Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:20` (búsqueda de `entryId`/`vehicle` como parámetro: sin resultados). Sin mención en `DECISIONES_REVISION.md`, plan F4-09 ni DEC-016.
- **Impacto:** en depósitos de varios camiones (DEC-013) la mercancía de cada camión no lleva su rótulo propio.
- **Criticidad:** MEDIA — función secundaria en un escenario frecuente (varios camiones por documento).
- **Dependencias:** ninguna.
- **Acción recomendada:** confirmar con el negocio; si se usa, agregar `entryId` opcional a la etiqueta.
- **Criterio verificable de resolución:** existe una etiqueta por camión del depósito con su mercancía y placa, con su registro de impresión; o decisión documentada de no construirla.

### BR-04-003 — El aviso y la pantalla de abandono abren en «En alerta»

- **ID funcional:** CF-L140.b, CF-LX04-01.
- **Descripción:** la pantalla `/foreign-trade/abandonment` arranca con el filtro «En alerta» y el aviso del tablero enlaza siempre a `?estado=en-alerta`. Si solo hay depósitos vencidos, el aviso dice «0 en alerta y N en abandono» y el enlace abre una lista vacía. El legacy mostraba todos los depósitos desde el día 20, incluidos los vencidos.
- **Comportamiento esperado:** ver de entrada los depósitos en alerta y en abandono.
- **Comportamiento actual:** hay que cambiar el filtro a «En abandono» o «Todos».
- **Capa:** frontend.
- **Categoría:** FRONTEND.
- **Evidencia:** `F/pages/foreign-trade/abandonment/index.vue:51-55`; `F/features/foreign-trade/components/AbandonmentSummaryAlert.vue:21`; legacy `L/modulos/mod_depositos/listardepositosprorroga.php:121-130`. QA lo vio con «Todos» (`F11-informe-S5-2026-10-06.md:144`, `:175`). El plan frontend F2-07 fijó «En alerta» por defecto (`docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md:1128`): el código cumple el plan, pero el plan no es una decisión de §A y deja fuera a los vencidos.
- **Impacto:** un depósito ya vencido puede pasar desapercibido.
- **Criticidad:** BAJA — se corrige con un clic; la información está.
- **Dependencias:** ninguna.
- **Acción recomendada:** filtro inicial «En alerta + En abandono» (o «Todos») y enlace del aviso al estado con casos.
- **Criterio verificable de resolución:** con solo depósitos vencidos, «Ver depósitos» muestra filas.

### BR-04-004 — El PDF de la etiqueta no muestra el número de impresión

- **ID funcional:** CF-L141.b.
- **Descripción:** el legacy escribía «Impresión # N» o «Etiqueta guardada # N» en la etiqueta. V2 cuenta cada acción pero el PDF no la muestra.
- **Comportamiento esperado:** el que confirme el negocio (la decisión solo dice «se registra cada impresión»).
- **Comportamiento actual:** el número solo se ve en el distintivo del encabezado.
- **Capa:** backend.
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `L/reportes/crearpdfetiqueta.php:30-35`; `B/Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:91-253` (sin contador); `F/features/foreign-trade/components/LabelPrintsBadge.vue:16-23`; `bodegas-legacy/docs/legacy_analysis/DECISIONES_REVISION.md` §3.8.
- **Impacto:** una copia impresa no se distingue de la original.
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** confirmar con el negocio; si aplica, imprimir el número de la acción en el pie.
- **Criterio verificable de resolución:** la tercera impresión de un depósito lleva «Impresión # 3», o decisión de no mostrarlo.

### BR-04-005 — Volumen y condiciones del ingreso sin destino; observaciones solo en Borrador

- **ID funcional:** CF-L124, CF-L136.
- **Descripción:** «Modificar ingreso» guardaba volumen y condiciones; V2 no tiene esos campos. Las observaciones del depósito solo se editan en Borrador (el legacy, siempre).
- **Comportamiento esperado:** confirmar si se usan; si sí, capturarlos.
- **Comportamiento actual:** no existen; en Confirmado hay que devolver a corrección para cambiar observaciones.
- **Capa:** backend y frontend.
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `L/modulos/mod_ingresos/modificaringreso.php:89-110`, `:482-494`; `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:433-440` (`UpdateDraftInfo` solo en Borrador); búsqueda `Volume`, `Conditions`, `Incoterm` en `WarehouseStorage.cs`, `ServiceRecord.cs`, `ImportWarehouseStorage.cs`: sin resultados. Plan frontend F1-07 los cita en el legacy y no los incluye (`docs/planes/paridad-legacy/plan-frontend-paridad-legacy.md:676`). En el legacy, condiciones y observaciones se borraban al modificar (defecto, `modificaringreso.php:490`, `:494`).
- **Impacto:** bajo; la migración no los trae.
- **Criticidad:** BAJA.
- **Dependencias:** migración (módulo 08) si se agregan.
- **Acción recomendada:** confirmar con el negocio y registrar la decisión.
- **Criterio verificable de resolución:** decisión documentada, o campos disponibles y editables.

### BR-04-006 — Listas de empaque: archivo repetido, rol del importador y eliminación

- **ID funcional:** CF-L130, CF-L131.
- **Descripción:** (a) no se avisa si el nombre del archivo ya fue cargado (el legacy sí); (b) el importador puede ser cualquier tercero (no se filtra por rol `IMPORTER`); (c) eliminar una lista con artículos asociados responde 409, cuando el legacy la borraba (cambio razonable, sin decisión).
- **Comportamiento esperado:** aviso de duplicado; importador con rol; decisión sobre el bloqueo.
- **Comportamiento actual:** se puede cargar dos veces la misma lista y duplicar artículos activos.
- **Capa:** backend y frontend.
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `L/modulos/mod_listasempaque/evaluaarchivo.php:9-12`; `B/Wms.Application/ForeignTrade/PackingLists/Commands/ImportPackingList/ImportPackingListCommandHandler.cs:30-36` (`Stakeholders` sin rol), sin consulta por `FileName`; `…/DeletePackingList/DeletePackingListCommand.cs:26-28`; legacy `eliminarlistaempaque.php:52`.
- **Impacto:** artículos duplicados pueden asociarse dos veces al mismo camión.
- **Criticidad:** BAJA — función de apoyo, poco volumen (`FUNCTIONAL_GAPS.md` GAP-013: impacto medio según uso).
- **Dependencias:** ninguna.
- **Acción recomendada:** advertencia (no bloqueo) de nombre repetido por importador; filtrar el selector y validar el rol; confirmar el bloqueo de eliminación.
- **Criterio verificable de resolución:** cargar dos veces el mismo archivo muestra el aviso; un tercero sin rol `IMPORTER` es rechazado; decisión sobre la eliminación registrada.

### BR-04-007 — La validación del depósito contra la plantilla no tiene camino en la UI

- **ID funcional:** CF-V047 (SOLO_V2).
- **Descripción:** existen `GET imports/{id}/validation-info`, `POST imports/{id}/validate`, el servicio, el composable y `ValidationForm`, pero ninguna acción abre el diálogo en el listado ni en el detalle.
- **Comportamiento esperado:** botón «Validar depósito e imprimir etiqueta» (caso F5-VAL-001) o retiro del flujo.
- **Comportamiento actual:** solo por API.
- **Capa:** frontend.
- **Categoría:** INTEGRACION.
- **Evidencia:** `F/pages/foreign-trade/imports/index.vue:73`, `:107`, `:234-246`; `F/pages/foreign-trade/imports/[id]/index.vue:259`, `:365`, `:810-812` (ningún `showValidationDialog.value = true`); `B/Wms.Api/Controllers/v1/ForeignTradeController.cs:132-170`. QA la verificó por API (`docs/qa/resultados/defectos/DEF-F5-008.md`, Verificado).
- **Impacto:** la validación y su correo a Admin no se usan.
- **Criticidad:** BAJA — no es capacidad legacy.
- **Dependencias:** BR-04-008.
- **Acción recomendada:** confirmar con el negocio si se usa; exponerla o retirar el código muerto.
- **Criterio verificable de resolución:** existe un control que abre `ValidationForm`, o se eliminan el diálogo y los endpoints.

### BR-04-008 — `IImportDepositDetailDto` declara campos que el backend no envía

- **ID funcional:** CF-L133, CF-V047.
- **Descripción:** la interfaz TypeScript del detalle de importación tiene `releaseNumber`, `releaseDate`, `acceptanceNumber`, `acceptanceDate`, `currentStock`, `receivedQuantity`, `unitMeasure` (los tres últimos obligatorios), `productName` y `productDescription`, que `ImportDepositDetailDto` no tiene.
- **Comportamiento esperado:** la interfaz refleja el DTO.
- **Comportamiento actual:** `depositDetail.unitMeasure` se pasa a `ValidationForm` y llega `undefined`.
- **Capa:** integración.
- **Categoría:** CONTRATOS_API.
- **Evidencia:** `B/Wms.Application/ForeignTrade/Common/DTOs/ImportDepositDetailDto.cs`; `F/features/foreign-trade/types/import-deposit.ts` (interfaz `IImportDepositDetailDto`, campos de las líneas 13-30); `F/pages/foreign-trade/imports/[id]/index.vue:811`. Comparación campo a campo en `05-analisis-v2.md` §5.
- **Impacto:** latente (el único uso está en el diálogo inalcanzable).
- **Criticidad:** BAJA.
- **Dependencias:** BR-04-007.
- **Acción recomendada:** quitar los campos o marcarlos opcionales y usar la unidad de cada producto.
- **Criterio verificable de resolución:** la interfaz no tiene campos ausentes del DTO.

### BR-04-009 — Sin seriales por unidad ni su edición

- **ID funcional:** CF-L138, CF-L139 (RN-021).
- **Descripción:** el legacy crea un detalle con serial automático (código de barras) por unidad al registrar el depósito y permite editarlo. V2 no tiene ese concepto y no hay decisión que lo excluya fuera de Colmotores.
- **Comportamiento esperado:** decisión explícita (probablemente «solo Colmotores») o equivalente.
- **Comportamiento actual:** el depósito solo tiene líneas de producto con cantidades.
- **Capa:** backend y frontend.
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `L/modulos/mod_depositos/registrardeposito.php:124-145`; `detalleproducto.php:59-130`; `modificarserial.php:40-49`. Búsqueda en V2 de `serial`, `productodetalle`, `SerialNumber`, `numero_serie` en `B/Wms.Domain`, `B/Wms.Application`, `F/features`, `F/pages`: solo coincidencias de serialización JSON. `MIGRATION_MATRIX.md:142-143` sin decisión.
- **Impacto:** bajo si solo lo usaba Colmotores (excluido); `DEC-010` (no contar producto por producto) apunta en esa dirección.
- **Criticidad:** BAJA.
- **Dependencias:** exclusión Colmotores (módulo 08).
- **Acción recomendada:** confirmar con el negocio y documentar la exclusión.
- **Criterio verificable de resolución:** decisión registrada en `decisiones.md` o `DECISIONES_REVISION.md`.

### BR-04-010 — Diferencias del flujo de abandono sin decisión en §A

- **ID funcional:** CF-L140.a, CF-LX04-01, CF-V084.
- **Descripción:** la decisión de negocio fue «migrar como está en el legacy» (`DECISIONES_REVISION.md` §2.C.9). P6 autoriza tres correcciones (reporte con prórroga, días desde el ingreso, marca de destino). Quedan sin decisión: (a) la alerta (tablero y job) incluye los depósitos ya vencidos (el legacy solo la ventana 20–30 / 50–60); (b) la prórroga se puede registrar a cualquier edad del depósito (el legacy solo la ofrecía en el listado, desde el día 20); (c) la alerta pasa de «al abrir el panel, nivel ≤ 1» a una notificación diaria solo al rol Comercio Exterior (Admin la ve solo en el tablero de CE).
- **Comportamiento esperado:** confirmación del negocio (son ampliaciones razonables, escritas en el plan F2-09, §C).
- **Comportamiento actual:** el descrito.
- **Capa:** backend y frontend.
- **Categoría:** REGLAS_NEGOCIO.
- **Evidencia:** `B/Wms.Application/ForeignTrade/Common/Services/AbandonmentCalculator.cs:47-51`; `AbandonmentReader.cs:86-89`; `B/Wms.Application/ForeignTrade/Jobs/AbandonmentAlertService.cs:45`, `:62-72`; `…/RegisterStorageExtension/RegisterStorageExtensionCommandHandler.cs:27-40`; `F/pages/foreign-trade/imports/[id]/index.vue:349`; legacy `L/menus/evaluaabandonos.php:6-14`, `L/inicial.php:78`, `L/modulos/mod_depositos/listardepositosprorroga.php:751-760`.
- **Impacto:** bajo.
- **Criticidad:** BAJA.
- **Dependencias:** módulo 07 (reportes de abandono).
- **Acción recomendada:** confirmar con el negocio y registrar la decisión.
- **Criterio verificable de resolución:** `DEC-nnn` que acepte o ajuste los tres puntos.

### BR-04-011 — Filtros de los listados de depósitos

- **ID funcional:** CF-L122, CF-L133, CF-L134.
- **Descripción:** (a) el filtro «Manifiesto» busca el manifiesto del camión y no el manifiesto DIAN del depósito, que es el que filtraba el legacy (`nro_manifiestodian`); (b) los listados de exportación e inspección no filtran por placa del camión (el legacy sí, en exportación).
- **Comportamiento esperado:** buscar por manifiesto DIAN y por placa en EXP.
- **Comportamiento actual:** sin resultados al buscar el manifiesto DIAN; sin campo de placa en EXP/INSP.
- **Capa:** backend y frontend.
- **Categoría:** FRONTEND / BACKEND.
- **Evidencia:** `B/Wms.Application/ForeignTrade/Common/Queries/DepositSearchQueryExtensions.cs:50-60` (`ManifestNumber` sobre `Entries`/`Manifest`); `B/Wms.Application/ForeignTrade/Queries/GetExportDeposits/GetExportDepositsQuery.cs:14-26` (sin `VehiclePlate`); `F/features/foreign-trade/components/DepositFiltersPanel.vue:210` (placa y levante solo con `showReleaseFilters`); legacy `L/modulos/mod_ingresos/listaringresos.php:104-105`, `L/modulos/mod_depositos/listardepositosexp.php:132-136`. El plan frontend F5-03 solo pidió la placa y el levante para importación (`plan-frontend-paridad-legacy.md:2013-2030`, `IGetImportDepositsQuery`). **Antecedente:** QA lo dejó en backlog (`docs/qa/resultados/F11-informe-S5-2026-10-06.md:232`), sin ficha DEF.
- **Impacto:** búsquedas habituales de CE requieren otro criterio.
- **Criticidad:** BAJA.
- **Dependencias:** ninguna.
- **Acción recomendada:** incluir `ImportWarehouseStorage.ManifestNumber` en el criterio y exponer la placa en EXP/INSP.
- **Criterio verificable de resolución:** buscar un manifiesto DIAN registrado por CE devuelve su depósito; el listado EXP filtra por placa.


---

## Decisiones posteriores (2026-10-23)

> Nota del orquestador. Después de esta auditoría, el usuario respondió las preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054; `06-brechas-priorizadas.md` §3.1). El registro de arriba es la foto previa y no se reescribe. El estado vigente está en `06-brechas-priorizadas.md` y `04-matriz-global.csv`.

| Brecha | Estado | Decisión |
| --- | --- | --- |
| BR-04-001 | Cerrada: se acepta el comportamiento de V2 | DEC-051 |
| BR-04-002 | Cerrada: se acepta el comportamiento de V2 | DEC-051 |
| BR-04-012 | Cerrada: se acepta el comportamiento de V2 | DEC-051 |
