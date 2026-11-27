# Plan cerrado — Fase 2 · Formatos v2 de PDF: etiqueta y tarjeta, PDF del depósito y guía de salida

> **Fecha:** 26 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-26 («Apruebo los dos planes»), con las respuestas de §9 en D21 a D26. Va después del plan de ajustes de la QA de F05 y del de separadores numéricos (D26). Fase 1 hecha el 2026-11-27 (BE `0612773`, §4); fase 2 hecha el 2026-11-27 (BE `bf61eac`). **Enmendado el 2026-11-27, antes de la fase 2:** D27 (la tarjeta por vehículo v2 sin Ampara ni Saldo) y D28 (el PDF de inspección también con `DEPOSIT_PDF_FORMAT`), respuestas del usuario a las dos dudas del cierre de la fase 1.
> **Origen:** los rediseños del hallazgo 8 de la QA manual de F05 integrado ([`qa-manual/hallazgos-int-F05.md`](qa-manual/hallazgos-int-F05.md), `H/` 8), con tres mockups hechos con IA: [`formato-etiqueta-v2/`](qa-manual/formato-etiqueta-v2/), [`pdf-deposito-v2/`](qa-manual/pdf-deposito-v2/) y [`formato-guia-v2/`](qa-manual/formato-guia-v2/) (cada uno con `screen.png` y `code.html`). El usuario decidió el 2026-11-26 tratarlo en un plan propio (`AJQ/` D1) y elegir el formato con un parámetro por documento (`AJQ/` D2).
> **Base:** BE `fase-2` `348ab15` · FE `fase-2` `00d15e5` · docs `main` `9c90a71`. **Depende del plan de ajustes de la QA de F05** (`AJQ/`): su fase 2 corrige los datos de los PDF actuales (`AJQ/` D17 a D20), y este plan parte de esos datos ya corregidos. Al empezar, el ejecutor mide de nuevo las líneas citadas sobre `fase-2` con ese plan fusionado.
> **Líneas medidas de nuevo (fase 1, 2026-11-27):** sobre BE `fase-2` `6ccff7b`, que ya trae fusionados el plan de ajustes de la QA de F05 y el de formato numérico es-CO (`DEC-082`). Las líneas de `BS/` citadas en §1 son las de esa base. Desde la fase 1, el dibujo legacy está en `BS/Pdf/Legacy*Renderer.cs` y los datos en los registros de `BS/Pdf/` (D8): las fases 2 y 3 parten de ahí.
> **Alcance:** backend y docs. Formatos nuevos y **aditivos**: los legacy se conservan y un parámetro de sistema por documento elige cuál sale. Una migración de datos (los tres parámetros). Sin cambios de contrato ni de frontend: el Admin edita los parámetros en Configuración › Parámetros, como `GUIDE_CODE_TYPE` (`DEC-060`).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `BS/` = `B/Wms.Application/ForeignTrade/Common/Services/`; `F/` = `Frontend/wms/`; `D/` = `docs/`; `AJQ/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-ajustes-qa-2026-11-26.md`; `H/` = el archivo de hallazgos; `MK/` = `D/planes/sprint-11/qa-manual/`.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** los dos `AGENTS.md` de los repos, `D/procesos/flujo-de-trabajo-agentes.md`, `D/contexto/decisiones.md` `DEC-060`, `AJQ/` D1, D2, D5 y D17 a D20 (con su estado de ejecución), `H/` 8 y este plan completo. Los tres `screen.png` de `MK/` y, para medidas y colores, su `code.html`.
2. **Cuándo:** después de fusionar en `fase-2` el plan de ajustes de la QA de F05. No corre en paralelo con el plan de separadores numéricos (`D/planes/sprint-11/plan-cerrado-f2-separadores-numericos-2026-11-26.md`): los dos tocan los mismos servicios. Este plan va después del de separadores (D26).
3. **Ramas y git:** `f2/formatos-pdf-v2` en BE, desde `fase-2`. Commit y push al cerrar cada fase, con el mensaje de §7; la migración va en el mismo commit que el código (`DEC-081`). Al cerrar la fase 4, fusión en `fase-2` con `--no-ff` y push. Sin `push --force`. Para borrar, `rm`.
4. **Una fase por turno** (`AGENTS.md`): al cerrar cada una, compuertas, commit, estado en este plan (§4) y en la matriz, y reporte.
5. **Líneas citadas:** son de la base. Confírmalas con grep; si el código no coincide, pregunta en un solo mensaje.
6. **Migración:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api`, aplicada solo en la base local.
7. **Verificación:** API local (`dotnet run --project B/Wms.Api --launch-profile http`, puerto 5281) y el frontend con Administrador y Comercio Exterior: se cambia el parámetro en Configuración › Parámetros y se descarga el PDF desde el detalle del depósito. Depósito de la QA: `5f3749d2-6058-4f58-91e9-45d53f832b41`. PDF y capturas en `D/planes/sprint-11/evidencias-formatos-pdf-v2/` (una carpeta por fase, con su `README.md`). Para comparar el legacy antes y después (D8), `pdftotext -layout` y una captura de cada página.

---

## 1. Decisiones

### 1.1 Del usuario

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Formatos nuevos y aditivos.** La etiqueta del depósito y la tarjeta por vehículo, el PDF del depósito y la guía de salida tienen un formato v2 más moderno, organizado y limpio. Los formatos legacy **no se eliminan** | `H/` 8 y su nota |
| D2 | **Un parámetro de sistema por documento**, que el Admin cambia en Configuración, como `GUIDE_CODE_TYPE` | Usuario, 2026-11-26 (`AJQ/` D2) |
| D3 | **El PDF del depósito y la guía comparten encabezado y pie.** El logo sale de los del frontend | `H/` 8, nota |
| D4 | **De los mockups se toman la distribución y el estilo; los datos y las reglas son los de los PDF actuales**, ya corregidos por `AJQ/` D17 a D20. Donde un mockup muestra otro dato u otra regla, gana el PDF actual (p. ej. el mockup de la etiqueta pinta «Unidad(es) de carga: N/A», y `AJQ/` D17 la oculta sin unidades) | Pedido de este plan; `AJQ/` D5 y D17 |
| D5 | **Plan propio**, después del plan de ajustes de la QA de F05 | Usuario, 2026-11-26 (`AJQ/` D1) |
| D21 | **Los tres parámetros arrancan en `LEGACY`.** Se pasan a `V2` cuando el usuario apruebe los formatos en local (P1) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D22 | **El v2 cubre exportación e inspección con el mismo parámetro.** `LABEL_FORMAT` elige también la etiqueta de exportación (`BS/LabelGenerationService.cs:243`) y la de inspección (`:427`) y sus tarjetas por vehículo (`DepositLabelKind.Export` e `Inspection`); `DEPOSIT_PDF_FORMAT`, también el PDF del depósito de exportación (`GET exports/{id}/pdf`) y el de inspección (`GET inspections/{id}/pdf`, D28). Mismo diseño (D11 a D13), con sus datos de hoy y el texto y el color de su banda: azul «MERCANCIA PARA EXPORTACION» (`:299`) y naranja «INSPECCION ADUANERA» (`:493`) (P2) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D23 | **Encabezado con el logotipo vectorial** `bodegasLogoLetras.svg` (nombre, NIT y código del depósito habilitado dibujados) junto al montacargas; sin parámetros nuevos (P3) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D24 | **Se conservan los tamaños de página de hoy:** etiqueta y tarjeta A5 vertical; depósito y guía carta (P4) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D25 | **Sin el sello «DOCUMENTO OFICIAL»** del mockup de la guía (P5) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D26 | **Orden:** este plan va después del de separadores numéricos; los dos, después del plan de ajustes de la QA de F05 y sin correr en paralelo (P6) | Usuario, 2026-11-26 («acepto las recomendaciones») |
| D27 | **La tarjeta por vehículo v2 no lleva Ampara ni Saldo.** La tarjeta de hoy (ya corregida por `AJQ/` D18) solo tiene «Cant. ingresa» y «Mercancía» por fila, y la v2 conserva esos datos (D4). Ampara y Saldo son del depósito completo, no de un vehículo, y ya salen en la etiqueta del depósito (D11). Corrige D12, que los listaba por error | Usuario, 2026-11-27 («Sin Ampara ni Saldo»), duda del cierre de la fase 1 |
| D28 | **El PDF de inspección también cambia con `DEPOSIT_PDF_FORMAT`.** `GET inspections/{id}/pdf` (`B/Wms.Api/Controllers/v1/ForeignTradeController.cs:702`) usa el mismo `GenerateDepositPdfAsync` que importación y exportación: con `V2` sale el diseño de D13 con sus datos de hoy y la banda naranja «INSPECCION ADUANERA», como D22 para la exportación | Usuario, 2026-11-27 («Sí, con el mismo parámetro»), duda del cierre de la fase 1 |

### 1.2 Parámetros (D2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D6 | **Tres parámetros, con el patrón de `GUIDE_CODE_TYPE`.** <br>• **Códigos:** `LABEL_FORMAT` (etiqueta y tarjeta por vehículo), `DEPOSIT_PDF_FORMAT` (PDF del depósito) y `DISPATCH_GUIDE_FORMAT` (guía de salida). Tipo `string`; valores `LEGACY` o `V2`, sin distinguir mayúsculas. <br>• **Respaldo seguro:** un valor nulo, vacío, desconocido o el parámetro inactivo equivalen a `LEGACY`, como `GuideCodeType.Parse` devuelve el código de barras (`BS/GuideCodeType.cs:20-23`). <br>• **Tipos:** `PdfFormatKind { Legacy, V2 }` y `PdfFormatParameters` (códigos, `Parse`, `IsValid`) en `BS/PdfFormatParameters.cs`; `IPdfFormatSettingsProvider.GetAsync(code)` en `B/Wms.Application/Common/Interfaces/` y su implementación en `B/Wms.Application/Common/Services/PdfFormatSettingsProvider.cs`, que lee el parámetro activo en cada descarga, como `GuideCodeSettingsProvider` (`B/Wms.Application/Common/Services/GuideCodeSettingsProvider.cs:15-24`). Un cambio rige en la próxima descarga, sin desplegar. <br>• **Validación al editar:** `UpdateSystemParameterHandler` rechaza con 400 «El parámetro {código} solo admite LEGACY o V2.», como hace con `GUIDE_CODE_TYPE` (`B/Wms.Application/Administration/Commands/UpdateSystemParameter/UpdateSystemParameterHandler.cs:27-33`). <br>• **Semilla:** tres filas en `HasData` (`B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:229-240`, junto a `GUIDE_CODE_TYPE`) y su migración con `InsertData`, como `20261024170332_AddGuideCodeTypeParameter`. Descripción: «Formato del PDF de {documento}: LEGACY (actual) o V2 (nuevo).». Valor inicial: `LEGACY` (D21). <br>• **Frontend:** sin cambios. `F/app/pages/admin/parameters/index.vue` (solo Admin, `:29`) ya edita cualquier parámetro `string` y muestra el 400 del backend | D2; `DEC-060` |
| D7 | **Qué cubre cada parámetro.** <br>• `LABEL_FORMAT`: la etiqueta del depósito de importación (`BS/LabelGenerationService.cs:21`, `GenerateImportLabelAsync`; `GET imports/{id}/label`) y la tarjeta por vehículo de importación (`:625`, `GenerateVehicleLabelAsync` con `DepositLabelKind.Import`; `GET imports/{id}/entries/{entryId}/label`). <br>• `DEPOSIT_PDF_FORMAT`: el PDF del depósito (`BS/DepositPdfService.cs:38`, `GenerateDepositPdfAsync`, que sirven `GET imports/{id}/pdf`, `GET exports/{id}/pdf` y `GET inspections/{id}/pdf`; D28). <br>• `DISPATCH_GUIDE_FORMAT`: la guía completa y la guía por depósito (`BS/DispatchGuidePdfService.cs:68` y `:98`). <br>• **Exportación e inspección:** la etiqueta de exportación (`:243`), la de inspección (`:427`), sus tarjetas por vehículo y el PDF del depósito de exportación no tienen mockup. También entran al v2, con el mismo parámetro (D22) | D1; `H/` 8 |

### 1.3 Arquitectura

| # | Decisión | Fuente |
| --- | --- | --- |
| D8 | **Datos aparte del dibujo, sin cambiar el legacy.** <br>• **Hoy:** cada servicio carga las entidades y dibuja el PDF en el mismo método (p. ej. `BS/DepositPdfService.cs:38-498`; `BS/DispatchGuidePdfService.cs:346-822`, `BuildGuidePdf`; `BS/LabelGenerationService.cs:21-241` y `:625-882`). <br>• **Cambio:** por documento, un registro con los datos ya resueltos (`ImportLabelData`, `VehicleLabelData`, `DepositPdfData`, `DispatchGuidePdfData`, en `BS/Pdf/`), que arma la carga de hoy con las reglas de `AJQ/` D17 a D20; y dos dibujos: el legacy (el código de dibujo de hoy, movido sin cambios) y el v2 (`BS/Pdf/V2/`). El método público lee el parámetro (D6) y elige el dibujo. Firmas públicas, endpoints y nombres de archivo no cambian. <br>• **El legacy no cambia:** antes de mover el dibujo, el ejecutor guarda el texto (`pdftotext -layout`) y una captura de los cuatro PDF legacy del depósito de la QA y de una guía; después del movimiento, deben salir iguales salvo la hora de impresión (QA-PV2-001). <br>• **Reglas compartidas:** lo que hoy calcula el dibujo (textos de levantes y aceptaciones, `FormatReleasesSummary` y `FormatAcceptancesSummary`; color y texto del estado; `CargoUnitText.Format`; `QuantityDisplay`; código QR o de barras de `ResolveGuideCodeAsync`, `BS/DispatchGuidePdfService.cs:138-168`) pasa al registro de datos, para que los dos dibujos muestren lo mismo | D1, D4 |
| D9 | **Encabezado y pie compartidos del PDF del depósito y la guía** (D3), en `BS/Pdf/V2/V2DocumentHeader.cs` y `V2DocumentFooter.cs` (componentes de QuestPDF). <br>• **Encabezado:** a la izquierda, el montacargas `F/public/layout/images/logo/logo_wms_slim.png` (el de la barra de la app, `F/app/components/layout/AppTopbar.vue:46`); a su derecha, el logotipo `F/public/layout/images/logo/bodegasLogoLetras.svg` (vectorial, el de `AppLogo.vue:16`: «BODEGAS ASOCIADAS», NIT y «DEPÓSITO HABILITADO COD. 22080»), y debajo una raya oscura de ancho completo (mockups de depósito y guía). Es el logotipo vectorial (D23). <br>• **Pie:** la banda amarilla de hoy con `CompanyInfo.FooterAddressLine` y `FooterEmailLine` (parámetros `COMPANY_*`, CHG-84; `B/Wms.Application/Common/Models/CompanyInfo.cs`), con el estilo del mockup; encima, cada documento pone su línea «registrado / generado el …, impreso el …» y la guía su línea de contacto, como hoy (`BS/DispatchGuidePdfService.cs:790-800`). El número de página («Página X de Y») va en el pie de los dos. <br>• **Logos en el backend:** el backend no lee archivos del frontend. Se copian a `B/Wms.Application/Common/Resources/Pdf/` como `Content` (como `logo_wms.png`, `B/Wms.Application/Wms.Application.csproj:38`). La copia del SVG quita el `<style>` del modo oscuro y fija el color a negro; QuestPDF 2025.12 lo dibuja con `.Svg()`. Si el frontend cambia un logo, se vuelve a copiar (R3) | D3; `H/` 8 |
| D10 | **Estilo de los mockups, con tipografía embebida.** <br>• **Fuentes:** una sans (Inter) para el texto y una monoespaciada (JetBrains Mono) para números, códigos y fechas, como los mockups (`MK/pdf-deposito-v2/code.html`). Las dos tienen licencia SIL OFL; sus `.ttf` (regular, semibold y bold) se embeben en `B/Wms.Application/Common/Resources/Fonts/` y se registran una vez al iniciar (`FontManager.RegisterFontFromEmbeddedResource`), para que el contenedor de staging no dependa de las fuentes del sistema. Los legacy siguen con las suyas. <br>• **Colores:** la paleta pizarra de los mockups (títulos `#0f172a`, texto `#334155`, bordes y rótulos `#94a3b8` / `#cbd5e1`, fondos de bloque `#f8fafc`), el número del depósito en rojo (`#e11d48`) y la banda del pie en amarillo (`#facc15`). <br>• **Bloques:** datos en pares rótulo-valor dentro de recuadros de borde fino y esquinas suaves; tablas con cabecera gris clara. <br>• **Tamaño de página:** el de hoy en cada documento: etiqueta y tarjeta A5 vertical (`BS/LabelGenerationService.cs:96`), depósito y guía carta (`BS/DepositPdfService.cs:203`, `BS/DispatchGuidePdfService.cs:478`). El mockup de la guía usa A4: no se adopta (D24) | D4 |

### 1.4 Contenido de cada formato v2

| # | Decisión | Fuente |
| --- | --- | --- |
| D11 | **Etiqueta del depósito v2** (`MK/formato-etiqueta-v2/screen.png`). De arriba abajo: <br>• **Encabezado compacto:** montacargas y logotipo (D9, en tamaño de etiqueta); a la derecha, «Depósito No.» con el número en rojo y el código de barras Code 128 de hoy (`BS/LabelGenerationService.cs:84`). <br>• **Recuadro de partes:** Importador e Intermediario (`:126-139`) y Fecha ingreso (`:144-148`, `yyyy-MM-dd HH:mm:ss`). <br>• **Tabla Ampara · Saldo · Mercancía:** las mismas filas, la celda Ampara consolidada o por producto y el «N/A» sin productos (`:170-181`, `:932-971`). <br>• **Recuadro de documentos:** la línea del documento comercial (`:187-191`), «Manifiesto No.» con su fecha (`:193-197`), Placa(s) y, solo con unidades, «Unidad(es) de carga» (`AJQ/` D17). <br>• **Banda de estado:** el mismo texto y el mismo significado del color de hoy (`:86-88`: verde «MERCANCIA NACIONALIZADA» con levantes, rojo «MERCANCIA SIN NACIONALIZAR» sin ellos), con los tonos del mockup. <br>• **Datos de nacionalización:** solo con levantes, «Levantes» y «N Aceptacion» con sus fechas (`:217-235`) | D4; `H/` 8 |
| D12 | **Tarjeta por vehículo v2:** el mismo diseño de D11 con los datos de la tarjeta de hoy ya corregida por `AJQ/` D18: placa del vehículo, «Cant. ingresa» y «Mercancía» de sus filas, sin Ampara ni Saldo (D27) (`BS/LabelGenerationService.cs:711-722` y `:824-851`; tabla de la etiqueta, `:932-971`), manifiesto DIAN con fecha y el bloque de nacionalización con levantes. Las unidades de carga, solo con valor (`AJQ/` D17) | D4; `AJQ/` D17, D18 |
| D13 | **PDF del depósito v2** (`MK/pdf-deposito-v2/screen.png`): <br>• encabezado y pie compartidos (D9); <br>• «Depósito No.» en rojo con el Code 39 de hoy (`BS/DepositPdfService.cs:192` y `:222-236`) y, a la derecha, «Fecha Hora Ingreso»; <br>• bloques separados por rayas finas: Importador con su identificación y dirección (`AJQ/` D19); Carta Porte y su fecha, Manifiesto I.C. y su fecha (`:269-296`); S.I.A. / Agencia de aduanas y su identificación; Transportadora; <br>• «DESCRIPCIÓN DEL INGRESO A BODEGA»: tabla Producto · Pesajes (Placa, Cant., Peso Kg. = P. mercancía, Tiquete) · Cantidades (Entrada, Ampara, Saldo), con las reglas de `AJQ/` D19, y «TOTAL PESO (Kg)» = suma del P. mercancía; <br>• Unidad(es) de carga (en este documento sigue con «N/A», `AJQ/` D17), Observaciones, Responsable y Cuadrilla; <br>• firmas «Recibido por» (nombre e identificación del responsable, `:438-451`) y «Firma Conductor»; la línea «Depósito registrado el …, impreso el …» | D3, D4; `AJQ/` D19 |
| D14 | **Guía de salida v2** (`MK/formato-guia-v2/screen.png`): <br>• encabezado y pie compartidos (D9); <br>• bloque del número: a la izquierda el QR con «Escanee para verificar esta guía» o, con `GUIDE_CODE_TYPE = BARCODE`, el código de barras (`DEC-060`; `AJQ/` D20 lo deja a la izquierda); «GUÍA DE SALIDA NO.» con el número (y el sufijo por depósito, `:98-130`); a la derecha, «FECHA HORA SALIDA»; <br>• Importador, identificación y dirección; Placas (con país), Tiquetes (`AJQ/` D20) y Fecha ingreso por depósito; Conductores, Empresa de transporte y su identificación; Agencia de aduanas (sin el rol repetido, `AJQ/` D20) y su identificación; <br>• tabla con las columnas de la guía de hoy (sin «Unidad», `AJQ/` D7c): No., Producto, Doc / CPI, Depósito, Manifiesto, Levante, Aceptación, Embalaje, Entrada, Saldo Ante., Cant. Sale y Nvo. Saldo. Levantes y aceptaciones en líneas; «Cant. Sale» resaltada; debajo, «Total en esta salida» (`:832-842`); <br>• Unidades de carga, Observaciones, Responsable y Cuadrilla; Destino y «Vence» resaltado (`:738-752`); firmas «Firma Entrega» y la del importador o firmante (`:756-785`); <br>• la marca de agua «ANULADA» de la guía anulada (`:485-495`), igual que en el legacy. <br>• El sello «DOCUMENTO OFICIAL» del mockup no está en la guía de hoy y no se agrega (D25) | D3, D4; `AJQ/` D7c, D20; `DEC-060` |

---

## 2. Contrato

Ningún endpoint cambia: las mismas rutas devuelven el PDF del formato que diga el parámetro. Cambian los datos:

| Parámetro | Valores | Inicial | Lo edita |
| --- | --- | --- | --- |
| `LABEL_FORMAT` | `LEGACY` · `V2` | `LEGACY` (D21) | Admin, Configuración › Parámetros |
| `DEPOSIT_PDF_FORMAT` | `LEGACY` · `V2` | `LEGACY` (D21) | Admin |
| `DISPATCH_GUIDE_FORMAT` | `LEGACY` · `V2` | `LEGACY` (D21) | Admin |

- **Error:** `PUT` del parámetro con otro valor → 400 «El parámetro {código} solo admite LEGACY o V2.».
- **Migración:** `AddPdfFormatParameters`, solo `InsertData` de las tres filas.

---

## 3. Archivos que se tocan

**Backend**

- `BS/PdfFormatParameters.cs` (nuevo); `B/Wms.Application/Common/Interfaces/IPdfFormatSettingsProvider.cs` y `B/Wms.Application/Common/Services/PdfFormatSettingsProvider.cs` (nuevos); su registro en `B/Wms.Application/DependencyInjection.cs` (junto a `:160-161`).
- `B/Wms.Application/Administration/Commands/UpdateSystemParameter/UpdateSystemParameterHandler.cs` (D6).
- `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs` y la migración `AddPdfFormatParameters`.
- `BS/LabelGenerationService.cs`, `BS/DepositPdfService.cs` y `BS/DispatchGuidePdfService.cs` (D8: carga de datos y elección del dibujo).
- `BS/Pdf/` (nuevo): registros de datos y dibujos legacy movidos; `BS/Pdf/V2/` (nuevo): encabezado, pie, estilos y los cuatro dibujos v2.
- `B/Wms.Application/Common/Resources/Pdf/` (logos, D9) y `B/Wms.Application/Common/Resources/Fonts/` (D10); `B/Wms.Application/Wms.Application.csproj` (`Content` y `EmbeddedResource`); el registro de fuentes al iniciar en `B/Wms.Api/Program.cs` (junto a la licencia de QuestPDF, `:29`).
- Pruebas en `B/Wms.Tests` y `B/Wms.IntegrationTests` (§5).

**Frontend:** ninguno.

**Docs:** este plan, `D/contexto/decisiones.md` (amplía `DEC-060` §7 «Documentos impresos» con los tres parámetros; fase 4), `D/contexto/estado.md`, `B/deploy/staging/README.md` (la lista de parámetros, junto a `GUIDE_CODE_TYPE`, `:272`; va en el commit BE de la fase 4), `D/planes/README.md`, la matriz y los casos en `D/qa/`.

---

## 4. Fases

| Fase | Repo | Contenido | Cierre | Estado |
| --- | --- | --- | --- | --- |
| 1 | BE | D6 y D8: parámetros, proveedor, validación, semilla y migración; datos separados del dibujo en los tres servicios, con el legacy sin cambios. Con `V2`, aún sale el legacy | Compuertas BE; QA-PV2-001 a 003 en PASA | Hecha el 2026-11-27 (BE `0612773` en `f2/formatos-pdf-v2`, desde `fase-2` `6ccff7b`): migración `20261127060211_AddPdfFormatParameters` aplicada en local; `Wms.Tests` 2408 → 2447, integración 888 → 891, `has-pending-model-changes` limpio. QA-PV2-001 en PASA: 18 pares antes/después con el mismo texto e imagen, salvo la hora de impresión. QA-PV2-002 y 003 en PASA por API (sin acceso de Admin al frontend local) ([evidencias](evidencias-formatos-pdf-v2/README.md)). La etiqueta y la tarjeta de exportación e inspección siguen dibujándose en el servicio (D22, fase 2) |
| 2 | BE | D9, D10, D11, D12 y D22: encabezado y pie compartidos, fuentes, etiquetas y tarjetas por vehículo v2 de importación, exportación e inspección | Compuertas BE; QA-PV2-004 a 006 y 012 en PASA | Hecha el 2026-11-27 (BE `bf61eac` en `f2/formatos-pdf-v2`): `V2LabelRenderer` (etiqueta y tarjeta de importación, exportación e inspección), encabezado y pie v2, logos en `B/Wms.Application/Common/Resources/Pdf/`, Inter 4.1 y JetBrains Mono embebidas (OFL); la etiqueta de exportación e inspección, separada en `DepositLabelData` y `LegacyDepositLabelRenderer` con el legacy igual (texto e imagen). `Wms.Tests` 2447 → 2465, integración 891 → 892, `has-pending-model-changes` limpio. QA-PV2-004 a 006 y 012 en PASA, con el formato fijo en una prueba temporal y el parámetro por API en la de integración ([evidencias](evidencias-formatos-pdf-v2/README.md)). En A5, «Deposito No.» va sobre el número, no en la misma línea del mockup |
| 3 | BE | D13, D14, D22 y D28: PDF del depósito (importación, exportación e inspección) y guía de salida v2 | Compuertas BE; QA-PV2-007 a 010 y 013 en PASA | Pendiente |
| 4 | BE y docs | Casos a `D/qa/`; `DEC-060` ampliada, estado y README de staging; fusión de `f2/formatos-pdf-v2` en `fase-2` | QA-PV2-011 en PASA; fusión con push | Pendiente |

---

## 5. Pruebas y casos QA

**Backend:**

- `PdfFormatParametersTests`: `Parse` con `LEGACY`, `V2`, `v2`, vacío, nulo y desconocido; `IsValid`; los tres códigos.
- `PdfFormatSettingsProviderTests` (integración): parámetro activo, inactivo y ausente → `Legacy` salvo `V2` activo.
- `UpdateSystemParameter` (integración): 400 con un valor inválido en cada uno de los tres; 200 con `v2`.
- Por documento (integración): con `LEGACY` y con `V2`, el endpoint responde 200 `application/pdf` y los bytes difieren entre formatos; la guía anulada sale en los dos.
- Reglas que pasan al registro de datos (D8): pruebas puras de los textos de levantes y aceptaciones, del estado y su color, y de las unidades de carga.
- Las pruebas de PDF que ya existen (`B/Wms.Tests/ForeignTrade/DispatchGuidePdfTotalTests.cs`, `B/Wms.IntegrationTests/ForeignTrade/DispatchGuideVerificationTests.cs`, `GuideManifestTests.cs`, `GuideReprintTests.cs`) siguen en verde.

**Casos QA** (API local; PDF descargados desde el detalle del depósito de la QA):

| Caso | Pasos | Resultado esperado |
| --- | --- | --- |
| QA-PV2-001 | Fase 1, los tres parámetros en `LEGACY`: etiqueta, tarjeta por vehículo, PDF del depósito y guía | Texto (`pdftotext -layout`) y captura iguales a los de antes de la fase, salvo la hora de impresión |
| QA-PV2-002 | Configuración › Parámetros: `LABEL_FORMAT` = `otro` | 400 «El parámetro LABEL_FORMAT solo admite LEGACY o V2.»; el valor no cambia |
| QA-PV2-003 | Desactivar `DEPOSIT_PDF_FORMAT` con valor `V2` y descargar el PDF del depósito | Sale el legacy |
| QA-PV2-004 | `LABEL_FORMAT` = `V2`: etiqueta del depósito de la QA | Diseño de D11: logotipo, número en rojo con código de barras, partes, tabla Ampara · Saldo · Mercancía, documentos, banda verde «MERCANCIA NACIONALIZADA» y levante 372024000009520 con su aceptación; sin «Unidad(es) de carga» si no hay unidades |
| QA-PV2-005 | Lo mismo con un depósito sin levantes y uno con unidades de carga | Banda roja «MERCANCIA SIN NACIONALIZAR» sin bloque de nacionalización; la línea de unidades con su valor |
| QA-PV2-006 | `LABEL_FORMAT` = `V2`: tarjeta por vehículo de un camión del depósito de la QA | Diseño de D12, con la placa del camión, «Cant. ingresa» y «Mercancía» de sus filas sin Ampara ni Saldo (D27), manifiesto DIAN con fecha y el bloque de nacionalización |
| QA-PV2-007 | `DEPOSIT_PDF_FORMAT` = `V2`: PDF del depósito de la QA | Diseño de D13; importador con identificación; P. mercancía por camión, total 96.050 (es-CO, `DEC-082`); Entrada, Ampara y Saldo con la regla de `AJQ/` D19; encabezado y pie de D9 |
| QA-PV2-008 | `DISPATCH_GUIDE_FORMAT` = `V2`: guía de una salida del depósito de la QA, con `GUIDE_CODE_TYPE` = `QR` | Diseño de D14; QR a la izquierda; tiquetes; agencia sin el rol repetido; encabezado y pie iguales a los del PDF del depósito |
| QA-PV2-009 | La misma guía con `GUIDE_CODE_TYPE` = `BARCODE`, y su PDF por depósito | Código de barras en el lugar del QR; el número con sufijo en el PDF por depósito |
| QA-PV2-010 | Una guía anulada en `V2` | Marca de agua «ANULADA» |
| QA-PV2-012 | `LABEL_FORMAT` = `V2`: etiqueta y tarjeta por vehículo de un depósito de exportación y de uno de inspección | Diseño de D11 con sus datos de hoy; banda azul «MERCANCIA PARA EXPORTACION» y naranja «INSPECCION ADUANERA» (D22) |
| QA-PV2-013 | `DEPOSIT_PDF_FORMAT` = `V2`: PDF de un depósito de exportación y de uno de inspección | Diseño de D13 con sus datos de hoy; banda azul en exportación y naranja «INSPECCION ADUANERA» en inspección (D22, D28) |
| QA-PV2-011 | Volver los tres parámetros a `LEGACY` y descargar los cuatro documentos | Salen los legacy, sin desplegar |

---

## 6. Compuertas de cada fase

- **BE (fases 1 a 4):** `dotnet build Wms.sln` sin errores; `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde (bases medidas en `fase-2` al empezar, con el plan de ajustes de F05 fusionado); `dotnet ef migrations has-pending-model-changes` limpio.
- PDF descargados de los casos de la fase, con su captura.

---

## 7. Commits

| Fase | Repo | Mensaje |
| --- | --- | --- |
| 1 | BE | `feat(pdf): parámetros de formato por documento y datos separados del dibujo (DEC-080, F05, formatos v2)` |
| 2 | BE | `feat(pdf): etiqueta y tarjeta por vehículo v2 (DEC-080, F05, formatos v2)` |
| 3 | BE | `feat(pdf): PDF del depósito y guía de salida v2 con encabezado y pie comunes (DEC-080, F05, formatos v2)` |
| 4 | BE | `docs(pdf): parámetros de formato en el README de staging (DEC-080, F05, formatos v2)` |
| 4 | docs | `docs(f2): formatos v2 de PDF; DEC-060 con los parámetros de formato` |

Fusión: `f2/formatos-pdf-v2` en `fase-2`, con `--no-ff`, en BE, al cerrar la fase 4.

---

## 8. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | Mover el dibujo legacy cambia sin querer un PDF que ya usan | D8: texto y captura antes y después (QA-PV2-001); el movimiento va solo en la fase 1, sin cambios de diseño |
| R2 | Una regla queda distinta entre el legacy y el v2 | D8: las reglas viven en el registro de datos y los dos dibujos las leen de ahí |
| R3 | El logo del frontend cambia y el del PDF queda viejo | D9: un comentario en `B/Wms.Application/Common/Resources/Pdf/` dice de qué archivo del frontend sale cada copia; si el frontend cambia un logo, se copia de nuevo |
| R4 | Las fuentes embebidas no cargan en el contenedor y QuestPDF cae a otra | Se registran desde recursos embebidos (D10), sin depender del sistema; QA en local y una descarga en staging tras el despliegue |
| R5 | El contenido no cabe en una A5 o en una página carta con muchos productos o levantes | El v2 usa tablas que pasan de página como el legacy, con encabezado y pie en cada página; QA con el depósito de la QA y una guía de varios productos |
| R6 | Un Admin pone `V2` por error y los operarios reciben otro formato | El cambio es reversible al instante (QA-PV2-011) y solo lo hace el Admin |

---

## 9. Preguntas pendientes

Ninguna. P1 a P6 se respondieron el 2026-11-26 con las recomendaciones («acepto las recomendaciones»): D21 a D26 (§1.1).
