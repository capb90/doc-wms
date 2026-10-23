---
titulo: Guiones de Video Tutoriales
subtitulo: Guía de producción para grabar el centro de ayuda del sistema WMS — qué mostrar en pantalla y qué narrar, video por video.
alcance: 8 series · 81 videos cortos (0:37 a 1:52 min; 1 h 20 min en total)
orden: plan maestro de grabación intercalado por rol (sección A.3)
incluye: objetivo, rol, requisitos, guion (acción + narración) y cierre de cada video
version: 2.0
fecha: Octubre de 2026
pie_portada: Complemento del Manual de Usuario del Sistema WMS
---

<!--
Fuente editable de los guiones. El PDF `docs/videos/Guiones_Video_Tutoriales_WMS.pdf` se genera desde
este archivo (ver `generar-pdf.md`). Convenciones del archivo:
- `## ` = capítulo (registro de cambios, sección A o serie). Una serie empieza con «## Serie N · …».
- `### N.M · Título` = guion. Debajo: la línea «**Duración:** … · **Rol:** …», los campos
  «**OBJETIVO** ·», «**GRABA CON** ·», «**REQUISITOS** ·», la tabla de tres columnas y «**Cierre:**».
- Las rutas de menú van entre comillas invertidas: `Bodega › Inventario`.
- Los textos de pantalla van entre «…» tal cual aparecen en el sistema.
- `[verificar en pantalla]` marca un texto que no se pudo confirmar en el código.
-->

## Registro de cambios

**Versión 2.0 · octubre de 2026.** Reemplaza la versión 1.0 de julio de 2026 (queda en el historial de git). La 1.0 se escribió antes de las Olas 1 a 3, de la paridad con el sistema legacy, de la corrección de los defectos del QA (CHG-01 a CHG-90 y DEF-F11-001 a 022) y de la migración: ningún guion de la 1.0 se podía grabar tal cual. El detalle guion por guion, con sus fuentes, está en `docs/videos/guiones/inventario-cambios-guiones.md`.

| Cambio | Guiones |
|---|---|
| **Nuevos (33)** | 0.3 Recuperar la contraseña · 0.4 Notificaciones, Mi cuenta y cerrar sesión · 0.5 Trazabilidad · 1.2 Gestionar la cuenta de un usuario · 1.5 Unidades de medida y tipos de unidad de carga · 1.11 Motivos, conductores y vehículos · 1.12 Ciudades y cuadrillas · 2.5 Previsualizar una tarifa · 2.6 Tarifas para carga perecedera · 2.10 Convenio de montacargas y servicio complementario · 3.6 Sobrescribir el total de una línea · 3.9 TRM pendiente y TRM manual · 3.10 Anular y refacturar · 3.11 Factura recalculada · 3.12 Cartera, mora y bloqueo · 3.13 Reportes de Facturación · 4.4 Corregir un ingreso · 5.6 Unidades de carga e inspección · 5.7 Varios camiones con el mismo documento · 5.8 Multidepósito · 5.11 Historial de báscula · 6.1 Registrar la llegada del camión · 6.3 Recibir unidades de carga · 6.8 Novedades · 6.9 Inventario general e historiales · 7.5 Corregir los productos del depósito · 7.6 Ajuste CE-7 · 7.8 Abandono y prórrogas · 7.9 Listas de empaque · 7.11 Modificar, cancelar y revertir una orden · 7.13 Guías pendientes e historial · 7.14 Anular un depósito · 7.15 Reportes de Comercio Exterior |
| **Actualizados (32 de la 1.0)** | v1 → v2: 0.1 → 0.1 · 1.1 → 1.1 · 1.2 → 1.3 · 1.3 → 1.4 · 1.4 → 1.6 · 1.6 → 1.8 · 1.7 → 1.9 · 1.9 → 1.13 · 2.1 → 2.1 · 2.2 → 2.2 · 2.4 → 2.4 · 2.5 → 2.7 · 2.7 → 2.9 · 3.1 → 3.1 · 3.2 → 3.2 · 3.3 → 3.3 · 3.6 → 3.5 · 3.7 → 3.7 · 4.1 → 4.1 · 4.3 → 4.3 · 5.2 → 5.2 · 5.4 → 5.9 · 5.5 → 5.4 · 5.8 → 5.12 · 6.2 → 6.4 · 6.3 → 6.5 · 6.4 → 6.6 · 6.5 → 6.7 · 7.1 → 7.3 · 7.2 → 7.2 · 7.4 → 7.4 · 7.7 → 7.12 |
| **Reemplazados (17 de la 1.0)** | v1 → v2: 0.2 → 0.2 · 1.5 → 1.7 · 1.8 → 1.10 · 2.3 → 2.3 · 2.6 → 2.8 · 3.4 y 3.5 → 3.4 (fusionados) · 3.8 → 3.8 · 4.2 → 4.2 · 5.1 → 5.1 · 5.3 → 5.3 · 5.6 → 5.5 · 5.7 → 5.10 · 6.1 → 6.2 · 7.3 → 7.7 · 7.5 → 7.1 · 7.6 → 7.10 |
| **Retirados** | Ningún guion completo. Salen estos pasos y funciones: «Cambiar modo de pago» de báscula (decisión D-2); el efectivo recibido y el cambio a devolver; la autorización de salida y el manifiesto en Vigilancia; el conductor y la transportadora en el ingreso de Vigilancia; el cambio de destinatario de una factura; «Validar depósito» (sin botón); el ajuste de inventario por Bodega; agregar o eliminar contenedores desde Comercio Exterior; «Archivar» un acuerdo (hoy es «Desactivar»); el ciclo «Bajo demanda»; la fórmula «Por unidad de embalaje». |
| **Sin guion** | «Estadísticas» (oculta por decisión del usuario), el cierre manual de período de almacenamiento (sin pantalla), los respaldos y la migración del legacy (tareas técnicas). |

**Otros cambios de la 2.0:**
- **Totales:** 81 videos en 8 series, 1 h 20 min en total.
- **Duraciones:** las de los videos grabados en octubre de 2026 (voz `es-CO-GonzaloNeural`), no estimaciones.
- **Fuente editable:** el archivo Markdown `docs/videos/guiones/guiones-video-tutoriales.md`; el PDF se genera desde ahí, en tamaño carta.
- **Rutas y textos:** las rutas usan los nombres exactos del menú, y los textos de pantalla van entre «…» tal como aparecen.
- **Cada guion dice:**
  - con qué cuenta se graba;
  - el resultado esperado de cada paso;
  - los requisitos, con los datos del dataset ficticio (`docs/videos/guiones/dataset-grabacion.md`).
- **Orden de grabación:** el plan maestro intercala los roles para que cada video deje listos los datos del siguiente.

## A · Cómo usar esta guía

Convenciones, recomendaciones de producción, el plan maestro de grabación y los datos de demostración.

### A.1 Qué encontrarás en cada video

Cada guion tiene el mismo formato, para que grabar sea mecánico:

| Parte | Qué dice |
|---|---|
| Número, título, duración y rol | El número indica la serie. La duración es la del video grabado: de 0:37 a 1:52 min. |
| OBJETIVO | Lo que el espectador sabrá hacer al terminar. |
| GRABA CON | La cuenta con la que se graba. Se ve el menú real de ese rol. |
| REQUISITOS | Los datos que deben existir antes de grabar. Los códigos (T1, P1, V01, PREP-5…) son del dataset de grabación (A.4). |
| Tabla del guion | Columna «En pantalla»: la acción y, tras **Verás:**, el resultado esperado. Columna «Narración sugerida»: lo que dices en voz alta. |
| Cierre | La frase de despedida y el enganche al siguiente video. |

**Convenciones de texto:**
- Las rutas de menú se escriben así: `Administración › Usuarios › Crear`. Son los nombres exactos del menú.
- Los textos que aparecen en pantalla (botones, campos, pestañas, mensajes) van entre comillas latinas: «Registrar ingreso».
- La narración va entre comillas inglesas y en cursiva.
- `[verificar en pantalla]` marca un texto que no se pudo confirmar en el código: confírmalo en el ensayo y corrige el guion si difiere.

### A.2 Recomendaciones de producción

| Aspecto | Recomendación |
|---|---|
| Duración | Corta: los videos grabados duran de 0:37 a 1:52 min. Si un tema se alarga, divídelo en dos videos. |
| Un objetivo por video | No mezcles tareas. El título empieza con un verbo o nombra la tarea. |
| Resolución y cursor | Graba en 1080p, con el cursor visible y zoom (o resaltado) en los campos clave y en los mensajes. |
| Datos de demostración | Usa solo el dataset ficticio. **No grabes en staging**: tiene clientes, conductores, vehículos y depósitos reales. No muestres datos reales ni valores sensibles. |
| Usuario por rol | Graba cada video con la cuenta de «GRABA CON», para que se vea el menú real de ese perfil. |
| Mensajes del sistema | Deja el mensaje en pantalla 2 s antes de seguir. Si un paso no muestra mensaje, el resultado es el cambio en pantalla (estado, fila nueva). |
| Audio y ritmo | Ensaya el guion, habla pausado y deja 1–2 s tras cada clic para que se siga en pantalla. |
| Apertura y cierre | Abre con «En este video vas a…» y cierra anunciando el siguiente. Da continuidad a la serie. |
| Tomas en dos partes | Algunos videos (5.5 y 5.9) esperan a otra área. Graba la primera parte, pausa, deja que la otra área haga su paso y retoma. Edita el corte con una transición. |
| Lo que no se graba | La tarjeta «Acerca del Módulo» de los tableros (texto antiguo), los campos de Trazabilidad que salen en inglés y cualquier pantalla de staging. |

### A.3 Plan maestro de grabación

Las series se publican en el orden 0 a 7, pero se graban en este orden, intercalando roles para que cada video deje listos los datos del siguiente. El recorrido de la mercancía es: crear un tercero → crear el acuerdo → registrar el ingreso → pesar → recibir → confirmar → levante → orden de cargue → cargue → guía → facturar.

| Orden | Videos | Rol que graba | Deja listo |
|---|---|---|---|
| 1 | 1.1 a 1.10 y 1.12 | Administrador | Usuarios, tercero T1, productos, servicios con precio, tarifas, mínimos, ubicaciones, ciudades y cuadrillas. |
| 2 | 2.1 a 2.10 | Administrador (Facturación en 2.1) | Acuerdos activos de T1 y T2. |
| 3 | 3.1 | Facturación | Configuración de facturación de T1. |
| 4 | 4.1 | Vigilancia | VID101 en la cola de báscula. |
| 5 | 5.1, 5.2, 5.3, 5.4 y 5.5 (primera toma) | Báscula | Depósito 2026BA00001 y primer peso de VID101. |
| 6 | 6.1 | Bodega | Llegada de VID101. |
| 7 | 5.5 (segunda toma) | Báscula | Ciclo de VID101 completo. |
| 8 | 6.2 | Bodega | Recepción con diferencia y aviso a Comercio Exterior. |
| 9 | 5.6 → 6.3 → 5.7 → 5.8 → 5.10 | Báscula y Bodega | Tanquero, inspección, segundo camión, multidepósito y operación descartada. |
| 10 | 6.4 y 6.5 | Bodega | Recepción directa y cobro de montacargas. |
| 11 | 7.1, 7.2, 7.3, 7.4, 7.5, 7.7, 7.8, 7.9 y 7.10 | Comercio Exterior | 2026BA00001 confirmado y nacionalizado, y la orden 2026OC00001. |
| 12 | 5.9 (primera toma) → 6.6 → 7.12 → 5.9 (segunda toma) | Báscula, Bodega y Comercio Exterior | Salida, cargue, guía 2026S00001 y repesaje. |
| 13 | 4.2 → 4.4 → 4.3 | Vigilancia | Salida de VID108 y una corrección de ingreso. |
| 14 | 7.11, 7.13 y 7.14 | Comercio Exterior | Orden cancelada y depósito anulado. |
| 15 | 6.7, 6.8 y 6.9 | Bodega | Mercancía ubicada y una novedad. |
| 16 | 5.11 y 5.12 | Báscula | Peso corregido y pesaje anulado. |
| 17 | 3.2 a 3.5 y 3.7 | Facturación | Factura `DEMO-FE-0001` aprobada. |
| 18 | 7.6 → 3.11 | Comercio Exterior y Facturación | Ajuste CE-7 y factura recalculada. |
| 19 | 3.6, 3.8, 3.9, 3.10, 3.12 y 3.13 | Facturación | Pagos, TRM, refacturación y reportes. |
| 20 | 7.15, 1.11 y 1.13 | Comercio Exterior y Administrador | Reportes, catálogos y auditoría con datos. |
| 21 | 0.1 a 0.5 | Varios | Se graba al final y se publica primero. |

**Series de la guía:**

| Serie | Videos | Rol | Nota |
|---|---:|---|---|
| 0 · Introducción | 5 | Todos | Se graba al final; se publica primero. |
| 1 · Administración | 13 | Administrador | Base: crea los datos maestros. |
| 2 · Acuerdos | 10 | Administrador / Facturación | Requiere servicios y clientes. |
| 3 · Facturación | 13 | Facturación | Consume las operaciones y los acuerdos. |
| 4 · Vigilancia | 4 | Operario vigilancia | Inicia el recorrido de la mercancía. |
| 5 · Báscula | 12 | Operario báscula | Registro, cobro y pesaje. |
| 6 · Bodega | 9 | Operario bodega | Llegada, recepción, montacargas, cargue e inventario. |
| 7 · Comercio Exterior | 15 | Comercio exterior | Depósito, levantes, órdenes y guías. |

Esta guía presenta las series en el orden de grabación por bloques (1, 2, 4, 5, 6, 7, 3 y 0). Cada guion es autónomo: si sus requisitos existen, puedes grabarlo suelto.

### A.4 Ambiente y datos de grabación

- **Dónde se graba:** en un ambiente aparte con datos ficticios.
  - Base de datos local nueva con el build actual (`dotnet ef database update`).
  - API en `localhost:5281` y frontend en `localhost:3000`.
  - Un buzón de correo local para el video de recuperación de contraseña.
  - **Nunca en staging.**
- **Datos:** todos están en `docs/videos/guiones/dataset-grabacion.md`:
  - Cuentas por rol: `video.admin`, `video.vigilancia`, `video.bascula`, `video.bodega`, `video.comext` y `video.facturacion`; las contraseñas se entregan aparte.
  - Terceros ficticios: T1 «Comercializadora Andina Demo S.A.S.», T2 «Distribuidora Nariño Demo S.A.S.», T3 agencia de aduanas, T4 transportadora, T5 exportador y T6 cliente moroso.
  - Productos: P1 «Cebolla cabezona», P2 «Aceite de palma a granel» y P3 «Llantas para camión».
  - Camiones `VID101`–`VID116` y `PVD1001`, con sus conductores «Demo».
  - Tarifas: báscula $16.806,72 + IVA, guía $15.000, almacenamiento de importación 0,295 % con mínimo de $50.000, y montacargas de $40.000 a $220.000.
  - Acuerdos A0–A2.
  - Pasos de preparación fuera de cámara (PREP-1 a PREP-11).
- **Números de documento:** los consecutivos (2026BA00001, 2026T…, 2026OC00001, 2026S00001) salen así si se respeta el plan maestro. Si cambian, usa los que muestre la pantalla.

## Serie 1 · Administración

13 videos · Rol Administrador. Es la base de todo el sistema: crea las cuentas, los terceros, los productos, los servicios con sus tarifas y los catálogos que usan las demás áreas. Grábala primero. Graba con `video.admin` (dataset C1).

### 1.1 · Cómo crear un usuario y asignarle roles
**Duración:** 1:08 min · **Rol:** Administrador

**OBJETIVO** · Crear una cuenta de usuario y darle los permisos correctos mediante roles.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Sesión de Administrador. Crea en cámara la cuenta C7 `video.nuevo`.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Usuarios › Listado`. **Verás:** la tabla «Gestión de Usuarios» con «Nombre», «Usuario», «Correo Electrónico», «Estado» y «Fecha de Creación». | “En este video vas a crear una cuenta de usuario. Entramos a Administración, Usuarios: aquí están todas las cuentas con su estado.” |
| 2 | Abre `Administración › Usuarios › Crear`. Completa «Nombre Completo» (Usuario Nuevo Demo), «Nombre de Usuario» (video.nuevo), «Número de Identificación», «Email» y «Teléfono». **Verás:** la vista previa con el nombre y el usuario a la izquierda. | “Llenamos sus datos básicos. El correo queda registrado, pero la recuperación por correo solo funciona para administradores: si esta persona olvida su clave, se la restablece el administrador.” |
| 3 | Escribe «Contraseña» y, a propósito, una distinta en «Repetir Contraseña». **Verás:** el medidor «Débil / Medio / Fuerte» y el error «Las contraseñas no coinciden». Corrige la segunda. | “Asignamos una contraseña temporal: al menos 8 caracteres, con mayúscula, minúscula, número y un carácter especial, sin espacios. Las dos deben coincidir.” |
| 4 | En «Roles» elige «Operario báscula» y «Facturación». | “Aquí está lo importante: el rol define qué menú verá. Los roles se suman: esta persona verá Báscula y Facturación. El sistema exige al menos un rol.” |
| 5 | Pulsa «Crear Usuario». **Verás:** el mensaje «Usuario creado.» — «El usuario Usuario Nuevo Demo se creó con éxito.» y se abre el detalle del usuario. | “Guardamos y se abre su ficha. La contraseña que escribimos es temporal: en su primer ingreso el sistema le pedirá cambiarla.” |

**Cierre:** Así creamos una cuenta y le damos permisos con roles. En el siguiente video administramos esa cuenta: roles, contraseña y estado.

### 1.2 · Cómo gestionar la cuenta de un usuario
**Duración:** 1:01 min · **Rol:** Administrador

**OBJETIVO** · Cambiar los roles de un usuario, restablecer su contraseña e inactivar o reactivar su cuenta.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · La cuenta C7 `video.nuevo` (creada en 1.1). No inicies sesión con ella después de este video: el video 0.2 necesita su cambio de contraseña pendiente.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Administración › Usuarios › Listado`, pulsa el ojo «Ver detalle» de Usuario Nuevo Demo. **Verás:** «Información Personal», «Roles y Permisos» y, arriba a la derecha, «Estado del Usuario» con la etiqueta «Activo». | “En este video vas a administrar una cuenta. Todo se hace desde su ficha.” |
| 2 | En «Roles y Permisos» pulsa «Asignar Roles», elige «Operario bodega» y pulsa «Asignar». **Verás:** «Roles asignados correctamente» y la nueva etiqueta. | “Agregamos un rol. El cambio rige de inmediato, aunque la persona tenga la sesión abierta.” |
| 3 | Pulsa «Remover Roles», elige «Operario bodega» y pulsa «Remover». **Verás:** «Roles removidos correctamente». | “Y lo quitamos. Dos reglas: el usuario debe conservar al menos un rol, y siempre debe quedar al menos un administrador activo.” |
| 4 | Pulsa «Resetear Contraseña». Completa «Nueva Contraseña» y «Confirmar Contraseña» y pulsa «Resetear». **Verás:** «Contraseña reseteada correctamente». | “Cuando alguien olvida su clave, el administrador se la restablece aquí. Sus sesiones se cierran y en su próximo ingreso deberá cambiarla.” |
| 5 | Apaga el interruptor de «Estado del Usuario». En «Inactivar usuario» deja vacía «Fecha máxima (opcional)» y pulsa «Inactivar». **Verás:** «Estado del usuario actualizado correctamente» y la etiqueta «Inactivo». | “Inactivar corta el acceso al instante. La fecha máxima es solo informativa: la cuenta no se reactiva sola. Y nadie puede inactivar su propio usuario.” |
| 6 | Enciende de nuevo el interruptor. **Verás:** el mismo mensaje y la etiqueta «Activo». | “Para devolverle el acceso, lo activamos de nuevo.” |

**Cierre:** Ya sabes mantener las cuentas al día. Ahora registramos a los terceros: clientes, agencias y transportadoras.

### 1.3 · Cómo registrar un tercero
**Duración:** 1:52 min · **Rol:** Administrador

**OBJETIVO** · Crear un tercero completo: identificación, roles de negocio, cuentas y contactos.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Ninguno. Crea en cámara el tercero T1 «Comercializadora Andina Demo S.A.S.», NIT 999000101.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Terceros › Listado`. Señala el buscador «Buscar por nombre, identificación, correo o teléfono» y los accesos `Terceros › Clientes`, `Terceros › Transportadoras` y `Terceros › Agencias de aduanas`. | “En este video vas a registrar un tercero. Los terceros son todas las empresas y personas con que operamos: clientes, importadores, agencias de aduanas, transportadoras. Comercio Exterior también puede crearlos.” |
| 2 | Abre `Administración › Terceros › Crear`. Completa «Nombre Completo» (Comercializadora Andina Demo S.A.S.), «Tipo de Identificación» «NIT» y «Número de Identificación» (999000101). | “Registramos su identificación, que saldrá en las facturas. El tipo admite NIT, RUT, cédula, pasaporte y RUC, para los terceros ecuatorianos.” |
| 3 | En «Roles de negocio» elige «Cliente» e «Importador». Señala la casilla «UAP (usuario aduanero permanente)» sin marcar. | “El rol de negocio dice qué papel cumple. Cliente es a quien se le factura; importador, exportador, agencia de aduanas y empresa de transporte son los terceros de los documentos. UAP solo se marca si es usuario aduanero permanente: suma en el informe de póliza.” |
| 4 | Pulsa «Agregar Cuenta» y completa «Nombre del Banco» (Banco Demo), «Tipo de Cuenta» «Ahorros» y «Número de Cuenta». Pulsa «Agregar Contacto» y completa «Nombre de Contacto» (Ana Demo Ruiz), «Email», «Teléfono» y «País». | “Cuentas y contactos son opcionales, pero conviene tenerlos. Al contacto ponle siempre el correo.” |
| 5 | Pulsa «Crear Tercero». **Verás:** «Tercero creado.» y se abre la ficha con «Información del Tercero», «Roles de negocio», «Gestión de Acuerdos», «Cuentas Bancarias» y «Contactos». | “Guardamos. Como es cliente, su ficha muestra Gestión de Acuerdos: ahí viven sus convenios, que veremos en la Serie 2.” |
| 6 | Señala «Estado Financiero» con la etiqueta «Activo». | “El estado financiero no se edita: lo calcula la cartera. Pasa a Vencido con facturas vencidas y a Bloqueado si la deuda vencida supera su límite de crédito. Un cliente bloqueado no puede pagar báscula, crear órdenes de cargue ni emitir guías. El límite lo define Facturación en sus Configuraciones.” |
| 7 | (Opcional) Abre otra vez `Administración › Terceros › Crear` y repite el NIT 999000101 con el tipo «NIT». **Verás:** el mensaje «Ya existe un tercero con número de identificación 999000101.». Pulsa «Cancelar». | “El número de identificación no se repite: el sistema evita terceros duplicados.” |

**Cierre:** Ya tenemos a nuestro cliente registrado. Ahora creamos el catálogo de productos.

### 1.4 · Cómo crear productos y tipos de embalaje
**Duración:** 1:07 min · **Rol:** Administrador

**OBJETIVO** · Registrar un producto con su unidad de medida y su tipo de embalaje.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Unidades de medida sembradas. Crea en cámara E1 (embalaje SACO) y P1 «Cebolla cabezona».

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Productos › Crear`. **Verás:** «Información del Producto» con el «SKU» ya sugerido. | “En este video vas a crear un producto. Los productos se usan en báscula, en los depósitos y en las facturas. El SKU se sugiere solo; puedes cambiarlo.” |
| 2 | Escribe «Nombre del producto» (Cebolla cabezona) y una «Descripción». En «Unidad de medida» elige «Bulto». | “La unidad de medida es obligatoria: es la unidad en que se cuentan las cantidades del depósito y la que usan las tarifas por unidad.” |
| 3 | Junto a «Tipo de Embalaje» pulsa «+» («Crear nuevo tipo de embalaje»). En «Crear Tipo de Embalaje» escribe «Código» SACO y «Nombre» Saco, y pulsa «Crear». **Verás:** «Tipo de embalaje creado» y el embalaje seleccionado. | “Al empezar no hay embalajes: los creamos sobre la marcha. El embalaje describe cómo viene la mercancía y sale en los documentos; no cambia el cobro.” |
| 4 | Pulsa «Crear Producto». **Verás:** el detalle con «SKU: … · Unidad: Bulto». | “No aparece un mensaje: el detalle confirma que se creó. El nombre y el SKU no se repiten; el nombre se compara sin tildes ni mayúsculas.” |
| 5 | Abre `Administración › Productos › Tipos de Embalaje`. **Verás:** la tabla con SACO y las acciones «Editar» y «Eliminar». | “Aquí se administran los embalajes. Uno en uso no se puede eliminar.” |
| 6 | Abre `Administración › Productos › Listado` y marca «Solo creados desde báscula». | “Báscula puede crear un producto escribiendo una descripción libre. Esta casilla los muestra para que el administrador los revise y los normalice.” |

**Cierre:** Producto y embalaje listos. Sigue un catálogo que usan las fórmulas de cobro: unidades de medida y tipos de unidad de carga.

### 1.5 · Unidades de medida y tipos de unidad de carga
**Duración:** 0:48 min · **Rol:** Administrador

**OBJETIVO** · Conocer y ampliar los catálogos de unidades de medida y de tipos de unidad de carga.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Catálogos sembrados. Crea en cámara M1 (GALON) y M2 (ISOTANQUE).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Productos › Unidades de medida`. **Verás:** «Unidades de medida» con las diez sembradas (Tonelada, Kilogramo, Unidad, Bulto, Litro…). | “En este video vas a administrar dos catálogos. Las unidades de medida son las unidades en que se cuenta la mercancía.” |
| 2 | Pulsa «Nuevo». En «Crear unidad de medida» escribe «Código» GALON y «Nombre» Galón, y pulsa «Crear». **Verás:** «Unidad de medida creada exitosamente». | “El código se convierte a mayúsculas y no se puede cambiar después, como dice la ayuda.” |
| 3 | Pulsa «Editar» en Galón. **Verás:** el «Código» bloqueado y el interruptor «Activa». Pulsa «Cancelar». | “Una unidad en uso no se elimina: se desactiva con este interruptor.” |
| 4 | Abre `Administración › Productos › Tipos de unidad de carga`. **Verás:** «Contenedor», «Tanquero» y «Remolque». | “Una unidad de carga es el contenedor, tanquero o remolque que entra con el camión: se pesa con él, se anota su placa y sale completo o por partes.” |
| 5 | Pulsa «Nuevo». En «Crear tipo de unidad de carga» escribe ISOTANQUE e Isotanque, y pulsa «Crear». **Verás:** «Tipo de unidad de carga creado exitosamente». | “Los códigos importan: la fórmula Por unidad de medida usa el código de la unidad, y Por unidad de carga, el del tipo. Por eso no se cambian.” |

**Cierre:** Con los catálogos listos pasamos a lo que hace posible el cobro: los servicios.

### 1.6 · Servicios: IVA y precio base
**Duración:** 1:11 min · **Rol:** Administrador

**OBJETIVO** · Ubicar los servicios que cobra la bodega, asignar el IVA y registrar el precio base.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Servicios e impuestos sembrados. Deja listo S1: BASCULA con IVA y precio base $16.807 (el campo no admite centavos). Grábalo al menos tres días antes del recorrido (la preparación PREP-8 usa este precio).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Servicios › Tarifas base`. **Verás:** «Gestión de Servicios» con BASCULA, ALMACENAMIENTO, MONTACARGAS, PAPELERIA y GUIA_SALIDA, y la columna «Precio base actual». | “En este video vas a configurar el precio de un servicio. Un servicio es cada cosa que cobramos. Aunque el menú dice Tarifas base, aquí está la lista de servicios.” |
| 2 | Abre `Administración › Servicios › Crear` y señala «Código del servicio *», «Nombre del servicio *» y «Descripción». Pulsa «Cancelar». | “Los cinco servicios del negocio ya vienen creados. Solo crearías uno si la bodega empieza a cobrar algo nuevo; su código no se cambia después.” |
| 3 | Pulsa el ojo «Ver detalle» de BASCULA. **Verás:** «Información del Servicio» y el aviso «Este servicio está pendiente de precio…». | “La báscula aún no tiene precio.” |
| 4 | Junto a «Impuestos» pulsa «Agregar». En «Agregar impuestos» elige «Iva» y pulsa «Agregar». **Verás:** la etiqueta «Iva (19%)». | “La báscula lleva IVA del 19 %. Sin el impuesto asignado, el sistema no suma IVA aunque la tarifa diga ‘más IVA’.” |
| 5 | En «Historial de precios», sección «Nuevo precio», escribe «Precio base» 16.807, deja «Vigente desde» en la fecha de hoy y pulsa «Agregar». **Verás:** la línea con la etiqueta «Vigente» y, arriba, «Precio actual». | “Es el precio sin IVA: con el IVA, el pesaje queda en $20.000. No se programan precios futuros: el precio nuevo rige desde la fecha indicada y el anterior pasa a histórico.” |
| 6 | Abre el detalle de MONTACARGAS. **Verás:** «El IVA del montacargas se decide en cada cobro (Bodega → Montacargas).» y el aviso que remite a las tarifas de montacargas. Abre ALMACENAMIENTO: tiene «Tarifas base» en lugar de precio. | “Dos excepciones: el montacargas se cobra por tipo de vehículo y Bodega decide el IVA en cada cobro; el almacenamiento se cobra con tarifas base, que vemos en el siguiente video.” |

**Cierre:** La báscula ya tiene precio. En el próximo video creamos la tarifa base del almacenamiento.

### 1.7 · Tarifas base de almacenamiento
**Duración:** 1:16 min · **Rol:** Administrador

**OBJETIVO** · Crear la tarifa general del almacenamiento para los clientes sin convenio.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · ALMACENAMIENTO sembrado con IVA. Deja listo S4: «Importación», 0,295 %, mínimo $50.000 con IVA incluido.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Administración › Servicios › Tarifas base`, abre el detalle de ALMACENAMIENTO. **Verás:** los paneles «Tarifas base» y «Valores mínimos por tipo de depósito». | “En este video vas a crear una tarifa base. El almacenamiento se cobra por períodos, por depósito. La tarifa base es la general: aplica a los clientes que no tienen convenio.” |
| 2 | Pulsa «Crear tarifa base». En «Tipo de fórmula *» elige «Porcentaje del valor declarado (sin prorrateo)». | “Elegimos la fórmula: un porcentaje del valor de la mercancía, el CIF, convertido a pesos.” |
| 3 | En «Tipo de depósito (opcional)» elige «Importación». Deja «Aplica a producto específico (opcional)» en «— Todos los productos —» y «Aplica a» en «Cualquier carga». | “Una tarifa con modalidad solo aplica a esa modalidad: esta, de importación, nunca cobra un depósito de exportación.” |
| 4 | En «Parámetros de la fórmula» escribe «Porcentaje (ej: 5 = 5%)» 0,295 y «Mínimo a cobrar ($)» 50.000. Deja marcado «El mínimo incluye IVA (desmarcado: es neto y se suma el IVA)». Señala la nota del IVA. | “El porcentaje calcula la base sin IVA y el IVA se suma en la factura. El mínimo lo dejamos con IVA incluido: el total nunca baja de $50.000.” |
| 5 | Despliega «Previsualizar», escribe «Valor de la mercancía (CIF)» 10.000.000 y pulsa «Previsualizar». **Verás:** «Importe:», «IVA:», «Total:» y la etiqueta «Mínimo aplicado». Repite con 100.000.000. | “Con 10 millones, el 0,295 % queda por debajo del mínimo, así que se cobra el mínimo. Con 100 millones se cobra el porcentaje.” |
| 6 | Pulsa «Crear». **Verás:** la tarifa en la tabla con el estado «Activa» y la etiqueta «Mínimo con IVA incluido». | “La tarifa nace activa. No sale un mensaje: la ves en la tabla. Si ya hubiera una activa con el mismo producto, modalidad y tipo de carga, el sistema lo avisa en rojo bajo el producto.” |
| 7 | Señala las acciones «Editar», «Desactivar» y «Eliminar» de la fila. | “Desde aquí se edita, se desactiva o se elimina una tarifa base.” |

**Cierre:** Ya hay tarifa general para importación. Falta la red de seguridad: el valor mínimo.

### 1.8 · Valores mínimos por tipo de depósito
**Duración:** 0:45 min · **Rol:** Administrador

**OBJETIVO** · Definir el valor mínimo de almacenamiento por modalidad e indicar si incluye IVA.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Filas sembradas en $0. Deja listo S5: Importación $50.000 «Con IVA incluido».

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En el detalle de ALMACENAMIENTO, baja a «Valores mínimos por tipo de depósito». Lee el texto «Se factura este valor cuando el depósito no tiene convenio ni tarifa base aplicable. La factura queda con advertencia para validar el precio.» | “En este video vas a configurar el valor mínimo. Es la red de seguridad: la factura de almacenamiento siempre se genera, aunque falte la tarifa.” |
| 2 | Señala las filas Importación, Exportación y Depósito por Inspección en $0, con la «Base» «Neto (+ IVA)». | “Al empezar todas están en cero: un depósito sin tarifa se facturaría en $0.” |
| 3 | Pulsa el lápiz «Editar» de Importación. En «Valor mínimo — Importación» escribe 50.000 y en «El valor mínimo se digita» elige «Con IVA incluido». Deja el interruptor en «Activo». | “Quien configura decide si el monto incluye el IVA o si es neto y el IVA se suma encima. Así nadie duda del total.” |
| 4 | Pulsa «Guardar cambios». **Verás:** «Valor mínimo actualizado» — «El valor mínimo se guardó correctamente.» y la «Base» «IVA incluido». | “Desde ahora, un depósito de importación sin tarifa se factura en $50.000 con IVA, y Facturación recibe la advertencia para validar el precio.” |

**Cierre:** El almacenamiento queda blindado. Sigue una tarifa aparte: la del montacargas.

### 1.9 · Tarifas de montacargas
**Duración:** 0:54 min · **Rol:** Administrador

**OBJETIVO** · Definir la tarifa del montacargas por tipo de vehículo.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Ninguno. Deja listo S6 (las cinco tarifas).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Tarifas de montacargas`. **Verás:** «Tarifas de Montacargas» y «Configure la tarifa base por tipo de vehículo. El acuerdo del cliente tiene prioridad sobre la tarifa base.» | “En este video vas a configurar el montacargas. Se cobra una tarifa fija según el tipo de vehículo que se descarga, no por horas.” |
| 2 | Señala las filas «Tractomula», «Doble troque», «Sencillo», «Turbo» y «Guacal / Estiba», con «Sin configurar». | “Hay una tarifa por tipo de vehículo.” |
| 3 | En Tractomula escribe 220.000 en «Tarifa (COP)» y pulsa «Guardar» de esa fila. **Verás:** «Tarifa actualizada» — «La tarifa fue guardada exitosamente.». Repite: Doble troque 150.000, Sencillo 140.000, Turbo 110.000 y Guacal / Estiba 40.000. | “Son valores sin IVA. El IVA lo decide Bodega en cada cobro con la casilla Agregar IVA.” |
| 4 | Señala la columna «Última actualización». | “Si el cliente tiene un convenio de montacargas, ese convenio manda; si no, se usa esta tabla. Sin tarifa para el tipo de vehículo, Bodega no puede cobrar.” |

**Cierre:** Tarifas listas. Ahora preparamos la bodega física: las ubicaciones.

### 1.10 · Ubicaciones de bodega
**Duración:** 0:59 min · **Rol:** Administrador

**OBJETIVO** · Crear las ubicaciones físicas donde Bodega guarda la mercancía.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Base sin ubicaciones. Crea en cámara U1 `A01-R01-N01` y U2 `PATIO-01`.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Ubicaciones`. **Verás:** «Ubicaciones de Bodega» y los indicadores «Total», «Disponibles», «No disponibles» y «Cap. Total» en cero. | “En este video vas a crear ubicaciones. Son los lugares físicos donde se guarda la mercancía. Una base nueva no trae ninguna: hay que crearlas antes de que Bodega reciba.” |
| 2 | Pulsa «Crear Ubicación». Completa «Código» A01-R01-N01, «Nombre» Pasillo A - Rack 01 - Nivel 01, «Pasillo» A, «Rack» 01, «Nivel» 01 y «Capacidad (kg)» 5000. Pulsa «Crear». **Verás:** «Ubicación creada exitosamente». | “La convención es pasillo, rack y nivel. La capacidad va en kilogramos.” |
| 3 | Crea PATIO-01, «Patio Principal», sin pasillo, rack ni nivel, con 50000 kg. **Verás:** la etiqueta «Zona especial». | “Las zonas especiales, como el patio, no tienen pasillo ni rack.” |
| 4 | Pulsa «Editar» en una ubicación. **Verás:** «Código: …» sin poder cambiarlo y el interruptor «Disponible». Pulsa «Cancelar». | “Una ubicación no disponible deja de aparecer en las listas de Bodega. Y no se puede eliminar una ubicación que tenga mercancía.” |
| 5 | Usa el buscador «Buscar por código, nombre o pasillo...» y la casilla «Solo disponibles». | “Con el buscador ubicamos rápido cualquier posición.” |

**Cierre:** La bodega ya tiene dónde guardar. Siguen los catálogos de portería: motivos de entrada, conductores y vehículos.

### 1.11 · Motivos de entrada, conductores y vehículos
**Duración:** 0:59 min · **Rol:** Administrador

**OBJETIVO** · Administrar los motivos de entrada y consultar y corregir conductores y vehículos.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Grábalo al final (orden 20 del plan maestro), cuando ya existan los vehículos y conductores de las Series 4 y 5. Crea en cámara MV1 «Entrega de documentos».

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Motivos de Entrada`. **Verás:** «Motivos de Entrada» con las columnas «Descripción» y «Requiere Pesaje». | “En este video vas a administrar catálogos de portería. Vigilancia elige el motivo en cada ingreso. Si requiere pesaje, el camión pasa a la cola de báscula; si no, aparece en la recepción directa de Bodega.” |
| 2 | Pulsa «Nuevo». En «Crear Motivo de Entrada» escribe «Descripción» Entrega de documentos, deja apagado «Requiere Pesaje» y pulsa «Crear». **Verás:** «Motivo de entrada creado exitosamente». | “Solo el administrador crea, edita o elimina motivos. Un motivo en uso no se elimina.” |
| 3 | Abre `Administración › Vehículos`. **Verás:** «Gestión de Vehículos» con las placas VID… y las columnas «Placa», «Tipo», «País» y «Estado». | “Los vehículos se crean solos: Vigilancia los registra con la placa y Báscula completa el tipo y el país. Aquí se consultan y se corrigen.” |
| 4 | Pulsa «Editar» en VID107: cambia «Tipo de Vehículo» y pulsa «Guardar Cambios». **Verás:** «Vehículo actualizado exitosamente». Escribe la placa A1. **Verás:** «La placa debe tener de 3 a 20 letras, números o guiones.»; cancela. | “La placa admite de 3 a 20 letras, números o guiones; los espacios se quitan y todo queda en mayúsculas.” |
| 5 | Abre `Administración › Conductores` y pulsa «Editar» en un conductor. Cambia el «Teléfono» y pulsa «Guardar Cambios». **Verás:** «Conductor actualizado exitosamente». | “Los conductores nacen en Báscula al registrar el camión, o en la orden de cargue de Comercio Exterior. Aquí corregimos sus datos.” |

**Cierre:** Catálogos de portería al día. Siguen los catálogos del despacho: ciudades y cuadrillas.

### 1.12 · Ciudades y cuadrillas
**Duración:** 0:58 min · **Rol:** Administrador

**OBJETIVO** · Crear las ciudades de destino con sus días de tránsito y las cuadrillas de cargue.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Ninguno. Crea en cámara K1 «PASTO», K2 «QUITO» y Q1 «Cuadrilla A».

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Ciudades`. **Verás:** «No hay ciudades. Créelas o impórtelas del legacy.» | “En este video vas a crear ciudades y cuadrillas. Las ciudades de destino se eligen en la orden de cargue, y sus días de tránsito calculan el vencimiento de la guía de salida.” |
| 2 | Pulsa «Nueva ciudad». Completa «Nombre*» PASTO, «País*» COL, «Departamento» Nariño y «Días de tránsito» 1. Pulsa «Guardar». **Verás:** «Ciudad guardada». | “El país va con su código de tres letras.” |
| 3 | Crea QUITO, ECU, Pichincha, 2 días. Señala la casilla «Destino de abandono» y su ayuda «Las salidas a esta ciudad aparecen en el reporte de salidas a destino de abandono.» | “Marcamos como destino de abandono las ciudades cuyas salidas deben vigilarse en ese reporte.” |
| 4 | Señala los filtros «Estado» y «Destino de abandono» y el botón «Importar del legacy». | “La importación del legacy es para la carga inicial; no la usamos aquí.” |
| 5 | Abre `Administración › Cuadrillas`. Pulsa «Nueva cuadrilla», escribe «Nombre*» Cuadrilla A y pulsa «Guardar». **Verás:** «Cuadrilla guardada». | “Las cuadrillas son los equipos que descargan y cargan. Bodega las anota en la recepción y en el cargue.” |
| 6 | Pulsa «Editar» en la cuadrilla y señala el interruptor «Activa». Cancela. | “Una ciudad o una cuadrilla en uso no se elimina: se desactiva.” |

**Cierre:** Ciudades y cuadrillas listas. Cerramos la serie con la auditoría y los parámetros del sistema.

### 1.13 · Auditoría y parámetros del sistema
**Duración:** 1:09 min · **Rol:** Administrador

**OBJETIVO** · Rastrear quién hizo qué en el sistema y conocer los parámetros globales.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Grábalo al final (orden 20 del plan maestro), cuando la auditoría ya tenga registros. El parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` ya configurado (PREP-3).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Auditoría`. **Verás:** «Registro de Auditoría» con «Fecha», «Usuario», «Acción», «Tabla», «Descripción» e «IP». | “En este video vas a revisar la auditoría. Cada alta, cambio y baja queda registrada con el usuario, la IP y los valores anterior y nuevo.” |
| 2 | En «Tabla» elige «Usuario» y en «Acción» «Actualización». Pulsa el ojo «Ver detalle». **Verás:** «Detalle de Auditoría» con «Valor Anterior» y «Valor Nuevo». Pulsa «Cerrar». | “En un cambio solo se guardan los campos que cambiaron. Las contraseñas y los sellos de seguridad nunca se guardan.” |
| 3 | Filtra «Usuario» con Admin Demo. Señala una fila «Roles asignados a …». | “El filtro de usuario busca por el nombre. Los cambios de rol también quedan registrados. La pantalla no filtra por fecha: los registros salen del más reciente al más antiguo.” |
| 4 | Pulsa el ícono de usuario (ayuda «Mi cuenta») y, en «Configuraciones», «Parámetros del sistema». **Verás:** «Gestión de Parámetros del Sistema». | “Los parámetros globales están en Mi cuenta, solo para el administrador.” |
| 5 | Señala INVENTORY_ADJUSTMENT_ADMIN_EMAIL con su correo y los parámetros COMPANY_…. Abre el lápiz de uno, muestra «Editar Parámetro: …» y pulsa «Cancelar». | “Este correo recibe el aviso de cada ajuste de cantidad que hace Comercio Exterior; sin él, el ajuste no se puede registrar. Los parámetros COMPANY son los datos de la empresa que salen en tiquetes, guías y facturas. Se cambian con cuidado.” |

**Cierre:** Con esto termina la configuración inicial. Sigue la Serie 2: los acuerdos con los clientes.

## Serie 2 · Acuerdos (convenios)

10 videos · Rol Administrador (los acuerdos también los gestiona Facturación). Muestra cómo se pactan las condiciones comerciales de un cliente: es el primer insumo del cobro. Requiere los servicios y los clientes de la Serie 1. Las tarifas base y las de montacargas solo las administra el Administrador; los acuerdos, el Administrador y Facturación.

### 2.1 · Qué es un acuerdo y dónde se gestiona
**Duración:** 1:13 min · **Rol:** Administrador y Facturación

**OBJETIVO** · Entender qué es un acuerdo, sus estados, su prioridad en el cobro y cómo se llega a él.
**GRABA CON** · `video.admin` (C1) y, en el paso 5, `video.facturacion` (C6).
**REQUISITOS** · T1 con el acuerdo A0 «Convenio 2025 Andina Demo» activo (PREP-4).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Terceros › Clientes`. **Verás:** «Terceros» filtrado por clientes. Pulsa el ojo «Ver detalle» de Comercializadora Andina Demo S.A.S. | “En este video vas a conocer los acuerdos. Un acuerdo, o convenio, es el contrato comercial con un cliente: cuánto y cómo se le cobra cada servicio. Vive en la ficha del cliente.” |
| 2 | Baja a «Gestión de Acuerdos». **Verás:** las columnas «Referencia», «Nombre», «Estado», «Fecha de Activación Programada» y «Fecha de Creación», y CONV-DEMO-000 en «Activo». | “Esta sección solo aparece cuando el tercero tiene el rol Cliente. No hay un menú de convenios: siempre se entra por el cliente.” |
| 3 | Abre el filtro de «Estado» y señala «Borrador», «Programado», «Activo» y «Archivado». | “Borrador es un acuerdo en preparación. Programado tiene fecha prevista, pero el sistema no lo activa solo: hay que activarlo a mano. Activo es el único que se usa para cobrar, y cada cliente tiene uno solo. Archivado es el que ya no rige.” |
| 4 | Muestra una diapositiva con el orden de cobro: «Acuerdo › Tarifa base › Precio base › Valor mínimo». | “Cuando hay que cobrar, el sistema busca primero el acuerdo activo del cliente. Si no hay, usa la tarifa base del servicio; luego el precio base; y en almacenamiento, el valor mínimo. El acuerdo manda sobre cualquier tarifa general.” |
| 5 | Inicia sesión con `video.facturacion`. Abre `Facturación › Clientes`, pulsa «Ver detalle» del mismo cliente. **Verás:** la ficha en solo lectura y «Gestión de Acuerdos» con su botón «Nuevo». | “Facturación también gestiona los acuerdos, desde Facturación, Clientes. Ve al tercero en solo lectura, pero administra sus acuerdos.” |

**Cierre:** Ya sabemos qué es un acuerdo y dónde vive. Creemos uno paso a paso.

### 2.2 · Cómo crear un acuerdo y agregar un servicio
**Duración:** 1:04 min · **Rol:** Administrador

**OBJETIVO** · Crear un acuerdo en Borrador y configurar su primer servicio.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · T1 con A0 activo (PREP-4). Crea en cámara el acuerdo A1 `CONV-DEMO-001` con su primer servicio.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En la ficha de T1, sección «Gestión de Acuerdos», pulsa «Nuevo». **Verás:** «Crear Acuerdo» — «Complete la información básica del acuerdo.» | “En este video vas a crear un acuerdo. Empezamos por sus datos básicos.” |
| 2 | Escribe «Referencia» CONV-DEMO-001 y «Nombre» Convenio 2026 Andina Demo. Deja «Estado» en «Borrador». Pulsa «Crear Acuerdo». **Verás:** «Acuerdo creado» — «El acuerdo se creó exitosamente.» | “Lo creamos en Borrador para configurarlo con calma; mientras tanto, el acuerdo vigente sigue cobrando. La referencia no se repite para un mismo cliente.” |
| 3 | Pulsa el ojo «Ver detalle» del nuevo acuerdo. **Verás:** el diálogo con «Información General», «Fechas del Acuerdo» y «Servicios del Acuerdo», con «No hay servicios configurados para este acuerdo.» | “El acuerdo todavía no cobra nada: le faltan servicios.” |
| 4 | Pulsa «Agregar servicio al acuerdo». En «Servicio *» elige «ALMACENAMIENTO — Almacenamiento en Bodega» y en «Tipo de fórmula *», «Porcentaje del valor declarado (sin prorrateo)». | “El servicio del acuerdo es la unidad clave: un servicio, una fórmula y su alcance.” |
| 5 | En «Tipo de depósito (opcional)» elige «Importación». Deja el producto en «— Todos los productos del cliente —» y «Aplica a» en «Cualquier carga». En los parámetros: «Porcentaje» 0,25, «Mínimo a cobrar ($)» 45.000 y el check del mínimo con IVA marcado. Deja marcado «Activo». | “Pactamos un 0,25 % del valor de la mercancía para importación, con un mínimo de $45.000 con IVA.” |
| 6 | Revisa los datos y pulsa «Agregar». **Verás:** «Servicio agregado» — «El servicio se agregó al acuerdo correctamente.» y la tarjeta «ALMACENAMIENTO — Almacenamiento en Bodega» con «Fórmula:» y «Tipo de depósito: Importación». | “No puede haber dos servicios activos con el mismo servicio, producto, modalidad y tipo de carga. Revisa antes de pulsar Agregar: si el sistema rechaza, el diálogo se cierra y hay que digitar de nuevo.” |

**Cierre:** El acuerdo ya tiene su primer servicio. Ahora conozcamos las fórmulas, empezando por las de tarifa.

### 2.3 · Las fórmulas de tarifa
**Duración:** 1:08 min · **Rol:** Administrador

**OBJETIVO** · Conocer las fórmulas basadas en tarifa y sus parámetros.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · El acuerdo A1 en Borrador (2.2). En este video no se guarda nada.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En el detalle de CONV-DEMO-001 pulsa «Agregar servicio al acuerdo», elige «MONTACARGAS — Servicio de Montacargas» y abre «Tipo de fórmula *». | “En este video vas a conocer las fórmulas de tarifa. Veremos cada una sin guardar nada.” |
| 2 | Elige «Fijo». **Verás:** «Tarifa», «Mínimo por unidad de carga ($)», el check «El mínimo incluye IVA…» y la casilla «IVA incluido en la tarifa». | “Fijo cobra un valor único. Si la tarifa se cotizó con IVA incluido, marca esa casilla: el sistema separa la base y el IVA.” |
| 3 | Elige «Por unidad de medida». **Verás:** «Tarifa» y «Unidad de medida» (lista del catálogo). | “Multiplica la tarifa por la cantidad: por bulto, por tonelada, por litro. La unidad debe ser la misma de los productos.” |
| 4 | Elige «Por vehículo» y luego «Por unidad de carga». **Verás:** «Tipo de vehículo» en la primera y «Tipo de unidad de carga» en la segunda. | “Por vehículo cobra por cada camión del depósito. Por unidad de carga, por cada contenedor, tanquero o remolque del tipo elegido; reemplaza al antiguo cobro por embalaje.” |
| 5 | Elige «Por tipo de vehículo (montacargas)». **Verás:** «Tarifa Tractomula», «Tarifa Doble troque», «Tarifa Sencillo», «Tarifa Turbo» y «Tarifa Guacal / Estiba». | “Esta es exclusiva del montacargas: una tarifa por tipo de vehículo. No se puede usar en almacenamiento.” |
| 6 | Vuelve a «Fijo» (la fórmula de montacargas no tiene mínimo) y señala «Mínimo por unidad de carga ($)» y el check «El mínimo incluye IVA (desmarcado: es neto y se suma el IVA)». Pulsa «Cancelar». | “Casi todas aceptan un mínimo por unidad de carga, y el check dice si ese mínimo trae el IVA. Cancelamos sin guardar.” |

**Cierre:** Esas son las fórmulas de tarifa. Faltan las de porcentaje del valor de la mercancía.

### 2.4 · Las fórmulas de porcentaje del valor
**Duración:** 1:08 min · **Rol:** Administrador

**OBJETIVO** · Configurar un cobro como porcentaje del valor de la mercancía, con mínimo, umbral y prorrateo.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · El acuerdo A1 (2.2). En este video no se guarda nada.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En CONV-DEMO-001 pulsa «Agregar servicio al acuerdo», elige ALMACENAMIENTO y «Porcentaje del valor declarado (sin prorrateo)». **Verás:** «Porcentaje (ej: 5 = 5%)», «Mínimo a cobrar ($)» y «Umbral CIF por encima del cual no se aplica el mínimo ($)». | “En este video vas a conocer las fórmulas de porcentaje. Cobran un porcentaje del valor de la mercancía, el CIF, en pesos. Ojo: se escribe 0,25 para un 0,25 %.” |
| 2 | Señala la nota «El porcentaje del valor declarado calcula la base sin IVA; el IVA se suma en la factura. El mínimo tiene su propia opción “El mínimo incluye IVA”.» | “Con porcentaje no existe ‘IVA incluido en la tarifa’: el IVA siempre se suma a la base.” |
| 3 | Desmarca y vuelve a marcar el check «El mínimo incluye IVA…». | “Marcado, el mínimo es el total con IVA. Desmarcado, es neto y el IVA se suma encima. Viene marcado por defecto.” |
| 4 | Señala «Umbral CIF por encima del cual no se aplica el mínimo ($)». | “El umbral es opcional: si el CIF lo supera, ya no se aplica el mínimo.” |
| 5 | Cambia a «Porcentaje del valor de la mercancía (prorrateado por saldo)». | “La variante prorrateada cobra el porcentaje sobre el saldo: el CIF multiplicado por el saldo y dividido por la cantidad recibida. El mínimo no se prorratea. La primera, en cambio, cobra el CIF completo en cada período.” |
| 6 | Pulsa «Cancelar». | “El porcentaje debe estar entre 0 y 100; el sistema rechaza otro valor. Cancelamos sin guardar.” |

**Cierre:** Con el catálogo completo, veamos cómo comprobar una tarifa antes de guardarla: la previsualización.

### 2.5 · Previsualizar una tarifa
**Duración:** 0:47 min · **Rol:** Administrador o Facturación

**OBJETIVO** · Calcular una tarifa con valores de ejemplo antes de guardarla.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · El acuerdo A1 con su servicio de almacenamiento (2.2).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En CONV-DEMO-001, pulsa el lápiz «Editar» del servicio ALMACENAMIENTO. **Verás:** «Editar servicio del acuerdo». | “En este video vas a previsualizar una tarifa: calcular cuánto cobraría antes de guardarla.” |
| 2 | Despliega «Previsualizar». **Verás:** «Calcula la tarifa con valores de ejemplo, sin guardar nada. Complete solo las magnitudes que use la fórmula.» | “Llenamos solo lo que la fórmula usa; aquí, el valor de la mercancía.” |
| 3 | Escribe «Valor de la mercancía (CIF)» 10.000.000, deja «IVA (%)» en 19 y pulsa «Previsualizar». **Verás:** el total con la etiqueta «Mínimo aplicado», «Importe:», «IVA:», «Total:» y la frase «Se aplicó el mínimo a cobrar ($ 45.000 IVA incluido).». | “Diez millones al 0,25 % dan $25.000 más IVA: menos que el mínimo, así que se cobra el mínimo de $45.000.” |
| 4 | Cambia el CIF a 50.000.000 y pulsa «Previsualizar». **Verás:** «Se cobró 0,25 % del valor de la mercancía.» y el total de $148.750. | “Con 50 millones se cobra el porcentaje: $125.000 más IVA.” |
| 5 | Pulsa «Cancelar». | “La previsualización calcula exactamente igual que el cobro real, así que es la mejor forma de revisar una tarifa nueva.” |

**Cierre:** Ya puedes comprobar cualquier tarifa. Veamos un caso especial: la carga perecedera.

### 2.6 · Tarifas para carga perecedera
**Duración:** 0:46 min · **Rol:** Administrador

**OBJETIVO** · Crear una tarifa que solo aplica a la carga perecedera, con la fórmula de umbral de peso.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · Tarifa base S4 (1.7). Crea en cámara S7. (La misma dimensión existe en los servicios del acuerdo.)

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Administración › Servicios › Tarifas base`, abre ALMACENAMIENTO y pulsa «Crear tarifa base». En «Tipo de fórmula *» elige «Por umbral de peso (perecederos)». | “En este video vas a crear una tarifa para la carga perecedera, que se cobra distinto al resto.” |
| 2 | En «Aplica a» elige «Solo perecederos». **Verás:** la ayuda «Una tarifa para perecederos prevalece sobre la del producto o la modalidad.» | “Esta tarifa gana a las de producto o modalidad cuando la carga es perecedera.” |
| 3 | Completa «Umbral de peso bruto (kg)» 20000, «Mínimo por debajo del umbral ($)» 60000 y «Tarifa por kg desde el umbral ($)» 3. | “Por debajo del umbral de peso se cobra el mínimo; desde el umbral, una tarifa por kilo.” |
| 4 | Despliega «Previsualizar» y escribe «Peso bruto (kg)» 15000; pulsa «Previsualizar». Repite con 30000. **Verás:** el mínimo en el primer caso y el cobro por kilo en el segundo. | “Comprobamos los dos lados del umbral antes de guardar.” |
| 5 | Pulsa «Crear». **Verás:** la tarifa en la tabla con «Aplica a» «Solo perecederos». | “Puede convivir con una tarifa general del mismo alcance: la de perecederos aplica a la carga perecedera y la general, al resto.” |

**Cierre:** Ahora entendamos cómo elige el sistema cuando varias condiciones podrían aplicar.

### 2.7 · Cómo elige el sistema la tarifa
**Duración:** 1:14 min · **Rol:** Administrador

**OBJETIVO** · Entender cómo el sistema prioriza lo específico sobre lo general.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · El acuerdo A1 con su servicio general (2.2) y el producto P3. Crea en cámara el segundo servicio de A1.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En CONV-DEMO-001 pulsa «Agregar servicio al acuerdo»: ALMACENAMIENTO, «Porcentaje del valor declarado (sin prorrateo)», producto «Llantas para camión», «Tipo de depósito» «Importación», «Porcentaje» 0,20 y «Mínimo a cobrar ($)» 30.000. Pulsa «Agregar». **Verás:** «Servicio agregado». | “En este video vas a ver cómo elige el sistema. Agregamos una condición especial para las llantas.” |
| 2 | Señala las dos tarjetas: la general y la de «Aplica a: Llantas para camión». | “Ahora el cliente tiene una condición general y una específica para un producto.” |
| 3 | Muestra una diapositiva con la escalera: «producto + modalidad › producto › modalidad › general». | “El sistema aplica siempre la más específica que coincida: primero producto y modalidad, luego producto, luego modalidad y por último la general. Las llantas cobran 0,20 %; lo demás, 0,25 %.” |
| 4 | En la diapositiva, señala dos reglas más. | “Una regla de importación nunca cobra un depósito de exportación; una sin modalidad cubre todas. Y la de perecederos va antes que todo. Si hay empate, gana la creada más recientemente.” |
| 5 | Muestra los niveles: «Acuerdo › Tarifa base › Precio base › Valor mínimo». | “Primero cuenta el nivel y luego la especificidad: un acuerdo general gana a una tarifa base específica. En la factura, la columna Método cálculo dice de qué nivel salió cada línea.” |

**Cierre:** Así el sistema cobra lo correcto sin intervención manual. Pongamos el acuerdo en vigencia.

### 2.8 · Activar, desactivar y editar un acuerdo
**Duración:** 1:02 min · **Rol:** Administrador

**OBJETIVO** · Poner un acuerdo en vigencia, entender el archivado y editar sus servicios.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · A0 activo (PREP-4) y A1 en Borrador con dos servicios (2.2 y 2.7). Al terminar, A1 queda **activo** (lo usan las Series 3 y 7).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En «Gestión de Acuerdos» de T1, abre «Ver detalle» de CONV-DEMO-001. **Verás:** el estado «Borrador» y el botón «Activar». | “En este video vas a poner un acuerdo en vigencia. El nuevo acuerdo está listo.” |
| 2 | Pulsa «Activar». **Verás:** «Confirmación» — «Al activar este acuerdo, se archivará el acuerdo que esté activo ahora.». Pulsa «Aceptar». **Verás:** el estado «Activo» y la «Fecha de Activación». | “Un cliente tiene un solo acuerdo activo: al activar el nuevo, el anterior se archiva. No sale un mensaje: el estado lo confirma.” |
| 3 | Cierra el diálogo. **Verás:** CONV-DEMO-000 en «Archivado». Abre su detalle: «Fecha de Archivado» y el botón «Activar». | “El archivado no se borra: se conserva para la trazabilidad y se podría reactivar.” |
| 4 | En el detalle de CONV-DEMO-001 pulsa «Desactivar». **Verás:** «¿Está seguro que desea desactivar este acuerdo?». Pulsa «Cancelar». | “Desactivar no borra: deja el acuerdo Archivado. Cancelamos porque este es el vigente.” |
| 5 | Pulsa el lápiz «Editar» del acuerdo. **Verás:** «Editar Acuerdo» con el «Estado» bloqueado. Pulsa «Cancelar». | “Al editar se cambian la referencia y el nombre. Programar una activación solo se puede al crear el acuerdo, y aun así hay que activarlo a mano llegada la fecha.” |
| 6 | En una tarjeta de servicio pulsa el lápiz «Editar» («Editar servicio del acuerdo»; el servicio no se cambia) y luego la papelera «Eliminar». **Verás:** «¿Eliminar el servicio "…" del acuerdo? Esta acción no se puede deshacer.». Pulsa «Cancelar». | “Los servicios del acuerdo se corrigen o se quitan desde su tarjeta.” |

**Cierre:** Ya dominamos el ciclo del acuerdo. Armemos uno completo de principio a fin.

### 2.9 · Ejemplo completo: convenio de almacenamiento
**Duración:** 1:00 min · **Rol:** Administrador

**OBJETIVO** · Configurar desde cero un convenio de almacenamiento y dejarlo activo.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · T2 «Distribuidora Nariño Demo S.A.S.» (PREP-2). Crea en cámara el acuerdo A2 `CONV-DEMO-002`, que queda activo.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Administración › Terceros › Clientes` › Distribuidora Nariño Demo S.A.S. › «Gestión de Acuerdos» › «Nuevo». Escribe CONV-DEMO-002 y «Convenio almacenamiento Nariño Demo», en «Borrador». Pulsa «Crear Acuerdo». **Verás:** «Acuerdo creado». | “En este video vas a armar un convenio completo para nuestro segundo cliente.” |
| 2 | Abre «Ver detalle» y pulsa «Agregar servicio al acuerdo»: ALMACENAMIENTO, «Porcentaje del valor declarado (sin prorrateo)», «Tipo de depósito» «Importación», «Porcentaje» 0,28 y «Mínimo a cobrar ($)» 50.000 con el check del IVA marcado. | “Pactamos un 0,28 % del valor de la mercancía en importación, con un mínimo de $50.000 con IVA. Indicamos la modalidad: una regla de importación no cubre la exportación.” |
| 3 | Despliega «Previsualizar», escribe CIF 20.000.000 y pulsa «Previsualizar». **Verás:** un total de $66.640, sin «Mínimo aplicado». | “Comprobamos: 20 millones al 0,28 % dan $56.000 más IVA, por encima del mínimo.” |
| 4 | Pulsa «Agregar». **Verás:** «Servicio agregado». | “El servicio queda en el acuerdo.” |
| 5 | Pulsa «Activar» y luego «Aceptar». **Verás:** el estado «Activo». | “Activamos el convenio.” |
| 6 | Señala la tarjeta del servicio. | “Desde ahora, cada factura de almacenamiento de importación de este cliente usará estas condiciones, y la línea dirá Acuerdo, nivel 1.” |

**Cierre:** Convenio listo y activo. Cerremos la serie con el montacargas en el acuerdo y los servicios complementarios.

### 2.10 · Convenio de montacargas y servicio complementario
**Duración:** 0:56 min · **Rol:** Administrador o Facturación

**OBJETIVO** · Pactar el montacargas por tipo de vehículo y facturar un servicio complementario con el almacenamiento.
**GRABA CON** · `video.admin` (C1).
**REQUISITOS** · El acuerdo A2 activo (2.9) y PAPELERIA con precio $10.000 (S3, PREP-3).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En CONV-DEMO-002 pulsa «Agregar servicio al acuerdo»: «MONTACARGAS — Servicio de Montacargas», «Por tipo de vehículo (montacargas)», con Tractomula 200.000, Doble troque 140.000, Sencillo 130.000, Turbo 100.000 y Guacal / Estiba 35.000. Deja vacíos el producto, el tipo de depósito y «Aplica a» en «Cualquier carga». | “En este video vas a pactar el montacargas. Al cliente le damos tarifas propias por tipo de vehículo.” |
| 2 | Pulsa «Agregar». **Verás:** «Servicio agregado». | “Desde ahora, Bodega cobra el montacargas de este cliente con estas tarifas. Un cliente sin convenio de montacargas paga la tarifa general por tipo de vehículo.” |
| 3 | Pulsa el lápiz «Editar» del servicio ALMACENAMIENTO. En «Servicio complementario (opcional)» elige «PAPELERIA — Papelería / Software / Comunicaciones». | “Un servicio complementario se factura junto con el almacenamiento, en la misma factura.” |
| 4 | Pulsa «Guardar cambios». **Verás:** «Servicio actualizado» — «El servicio del acuerdo se actualizó correctamente.» | “El complementario debe tener su propio precio o convenio; aquí, papelería cuesta $10.000.” |

**Cierre:** Con esto cerramos los acuerdos. En la Serie 3 veremos cómo todo esto se convierte en facturas.

## Serie 4 · Vigilancia

4 videos · Rol Operario vigilancia. La portería y el primer eslabón de la trazabilidad: todo camión entra y sale por aquí. El usuario de Vigilancia solo ve «Notificaciones» y «Vigilancia». Graba con `video.vigilancia` (dataset C2).

### 4.1 · Cómo registrar el ingreso de un vehículo
**Duración:** 1:04 min · **Rol:** Operario vigilancia

**OBJETIVO** · Registrar la entrada de un camión con la placa y el motivo.
**GRABA CON** · `video.vigilancia` (C2).
**REQUISITOS** · Motivos de entrada sembrados. VID102 con ingreso abierto (PREP-5, hecho antes de este video). VID101 sin registrar: se crea en cámara (V01).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Inicia sesión con `video.vigilancia`. **Verás:** `Vigilancia › Ingreso` con «Registro de ingreso» a la izquierda y «Camiones en planta» con su número a la derecha. | “En este video vas a registrar el ingreso de un camión. Vigilancia hace una captura mínima: placa y motivo. El conductor y la transportadora los completa Báscula.” |
| 2 | Escribe «vid 101» en «Placa». **Verás:** que queda VID101. Pulsa Enter. **Verás:** «No existe, se creará al registrar.» | “Escribimos la placa; el sistema quita los espacios y pasa a mayúsculas. Con Enter la consulta: este camión viene por primera vez, así que se creará al registrar.” |
| 3 | En «Motivo de ingreso» elige «Descargue mercancia importacion». En «Observaciones» escribe Carga de cebolla, carta porte DEMO-CP-0001. | “El motivo decide el camino del camión. Los motivos con pesaje lo mandan a la cola de báscula; Solo bodega lo lleva directo a Bodega.” |
| 4 | Pulsa «Registrar ingreso». **Verás:** «Ingreso registrado» — «Placa VID101», el formulario limpio y «Camiones en planta» con uno más. | “Listo. La hora del ingreso la pone el sistema: será la fecha de ingreso del depósito.” |
| 5 | Escribe VID102 y pulsa Enter. **Verás:** «Ingreso duplicado» — «Este vehículo ya tiene un ingreso abierto.», el recuadro «Esta placa ya tiene un ingreso abierto desde …» y «Registrar ingreso» deshabilitado. | “Un vehículo no puede tener dos ingresos abiertos: primero debe registrar su salida.” |
| 6 | Escribe AB en «Placa». **Verás:** «Placa no válida. La placa debe tener de 3 a 20 letras, números o guiones.». Pulsa «Limpiar». | “La placa admite de 3 a 20 letras, números o guiones. El botón Limpiar borra el formulario.” |

**Cierre:** El camión ya está adentro y en la cola de báscula. Cuando termine su operación, registraremos su salida.

### 4.2 · Cómo registrar la salida de un vehículo
**Duración:** 0:46 min · **Rol:** Operario vigilancia

**OBJETIVO** · Registrar la salida de un camión y entender por qué el sistema puede impedirla.
**GRABA CON** · `video.vigilancia` (C2).
**REQUISITOS** · VID108 con su pesaje de salida completo y su guía (orden 12 del plan maestro). VID113 con el pesaje «Por repesar» (PREP-6).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Vigilancia › Salida`. **Verás:** «Camiones en planta» con el total y una tarjeta por camión con «Ingreso», «Motivo de ingreso» y el tiempo en planta. | “En este video vas a registrar la salida de un camión. Aquí están todos los camiones que siguen adentro; el reloj muestra cuánto llevan en planta y se resalta a las 24 horas.” |
| 2 | Escribe VID113 en «Buscar por placa...». Pulsa «Registrar salida» y, en «¿Confirma la salida del vehículo con placa VID113?», pulsa «Registrar salida». **Verás:** «El camión VID113 tiene un pesaje de báscula sin terminar (por repesar). Termínelo o anúlelo en Báscula antes de registrar la salida.», con el título «Error al registrar salida» | “Un camión con un pesaje sin terminar no puede salir: primero Báscula termina o anula el pesaje.” |
| 3 | Muestra una diapositiva con el otro bloqueo: «No se puede registrar la salida del vehículo …: la orden … es de importación y no tiene guía de salida vigente. Comercio Exterior debe emitir la guía.» | “Tampoco sale un camión con mercancía de importación sin su guía de salida. Ninguna mercancía de importación sale sin guía.” |
| 4 | Busca VID108, pulsa «Registrar salida» y confirma. **Verás:** «Salida registrada» — «Placa VID108» y la tarjeta desaparece. | “Este camión terminó todo su recorrido y tiene su guía: registramos la salida. La hora es la actual y queda registrado quién la autorizó.” |

**Cierre:** La salida quedó registrada. Veamos cómo consultar el historial de ingresos y salidas.

### 4.3 · Historial de ingresos y salidas
**Duración:** 0:44 min · **Rol:** Operario vigilancia

**OBJETIVO** · Consultar los ingresos y las salidas y rastrear un camión por su placa.
**GRABA CON** · `video.vigilancia` (C2).
**REQUISITOS** · Ingresos con y sin salida y una corrección hecha (grábalo después de 4.4).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Vigilancia › Historial`. **Verás:** «Historial de ingresos y salidas» y la tabla con «Placa», «Motivo», «Estado», «Ingreso», «Salida» y «Corrección». | “En este video vas a consultar el historial. Reúne todos los ingresos, del más reciente al más antiguo.” |
| 2 | Escribe VID10 en «Placa» y pulsa «Buscar». **Verás:** todas las placas que contienen VID10. Elige un «Motivo de ingreso» y luego pulsa «Limpiar filtros». | “La búsqueda es parcial: basta una parte de la placa. También filtramos por motivo.” |
| 3 | Señala la columna «Salida» con «Abierto» y la columna «Estado» con «Registrado» (o «Completado»). | “Abierto significa que el camión sigue adentro. Ojo: Completado no quiere decir que salió, sino que el ingreso ya tiene conductor y motivo; la salida se lee en su columna.” |
| 4 | Pulsa el ojo «Ver detalle» de VID110. **Verás:** «Detalle del Ingreso» con «Fecha Ingreso», «Fecha Salida», «Motivo» y el recuadro «Corregido el … por Vigilancia Demo». Pulsa «Cerrar». | “El detalle muestra las fechas y, si se corrigió, quién y cuándo.” |

**Cierre:** Ya sabes rastrear cualquier camión. Veamos cómo corregir un ingreso mal registrado.

### 4.4 · Cómo corregir un ingreso
**Duración:** 0:58 min · **Rol:** Operario vigilancia

**OBJETIVO** · Corregir la placa, el motivo o la fecha de un ingreso, dejando el motivo de la corrección.
**GRABA CON** · `video.vigilancia` (C2).
**REQUISITOS** · VID109 con ingreso abierto y sin operación (PREP-6). VID101 con operación de báscula (Serie 5).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Vigilancia › Historial`, busca VID109 y pulsa el lápiz «Editar». **Verás:** «Corregir ingreso» con «Placa», «Motivo de ingreso», «Fecha y hora de ingreso» y «Motivo de la corrección». | “En este video vas a corregir un ingreso. En portería se digitó mal una placa: el camión era VID110.” |
| 2 | Cambia «Placa» a VID110 y «Motivo de ingreso» a «Solo bodega». En «Motivo de la corrección» escribe Placa mal digitada en portería; el camión es VID110. Pulsa «Revisar cambios». | “Corregimos la placa y el motivo. El motivo de la corrección es obligatorio, de al menos 10 caracteres.” |
| 3 | **Verás:** la tabla «Campo / Valor anterior / Valor nuevo». Pulsa «Confirmar corrección». **Verás:** «Ingreso corregido», «Vehículo desactivado» — «La placa VID109 quedó sin ingresos y se desactivó.» y la etiqueta «Corregido» en la fila. | “Revisamos antes de confirmar. El ingreso pasa al vehículo correcto y la placa equivocada, que quedó sin ingresos, se desactiva.” |
| 4 | Busca VID101 y pulsa el lápiz. **Verás:** el «Motivo de ingreso» deshabilitado con «El ingreso ya tiene operación de báscula o bodega: el motivo no se puede cambiar.». Abre «Fecha y hora de ingreso»: no deja elegir fechas futuras. Pulsa «Cancelar». | “Si el camión ya tiene operación en báscula o en bodega, el motivo no se cambia. La fecha no puede ser futura, ni posterior a la salida o al primer pesaje. Corregir esta fecha no cambia la del depósito: esa la corrige Comercio Exterior.” |

**Cierre:** Toda corrección queda en la auditoría con su motivo. Con esto cerramos Vigilancia; en la siguiente serie, el camión pasa a la báscula.

## Serie 5 · Báscula

12 videos · Rol Operario báscula. La báscula toma el camión de la cola, registra los documentos y las cantidades declaradas, cobra, pesa e imprime el tiquete, todo en una sola pantalla. Su particularidad: se cobra **antes** de pesar, y las cantidades declaradas aquí son el stock del depósito. Graba con `video.bascula` (dataset C3).

### 5.1 · La pantalla de báscula: cola, ficha y pasos
**Duración:** 1:13 min · **Rol:** Operario báscula

**OBJETIVO** · Ubicarse en la pantalla única de báscula: la cola de camiones, la ficha y sus cuatro pasos.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · Ingresos abiertos de VID101 (4.1) y de VID102, VID103, VID104, VID106 y VID111 (PREP-5).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Inicia sesión con `video.bascula`. **Verás:** `Báscula › Proceso de Pesaje` con el título «Báscula» — «Registro, cobro y peso en la misma ficha». | “En este video vas a conocer la pantalla de báscula. Todo el trabajo se hace en una sola pantalla, para atender un camión en segundos.” |
| 2 | Señala «Cola de camiones» con «{N} con ingreso abierto» y los filtros «Todos», «Sin iniciar», «Por cobrar», «Por pesar» y «Por repesar», cada uno con su conteo. | “A la izquierda está la cola: los camiones que Vigilancia dejó entrar. Sin iniciar: nadie los ha tomado. Por cobrar: registrados, falta el cobro. Por pesar: cobrados, falta el primer peso. Por repesar: esperan el segundo peso.” |
| 3 | Señala en una fila la placa, el estado, el motivo y «{N} min en espera». | “Cada camión muestra cuánto lleva esperando; desde una hora se resalta.” |
| 4 | Pulsa VID101. **Verás:** la ficha con la placa, «{motivo} · Ingreso {fecha}», el botón «Soltar camión» y los pasos «1 Registro › 2 Cobro › 3 Peso › 4 Tiquete»; el «Tipo de operación» ya en «Ingreso con depósito». | “A la derecha se abre la ficha. El motivo de Vigilancia preselecciona la operación: Ingreso con depósito, Salida de mercancía o Solo báscula. Puedes cambiarla.” |
| 5 | Pulsa «Soltar camión». | “Si atiendes otro camión, lo digitado en cada uno se conserva. Si sales del módulo con datos sin guardar, el sistema te avisa.” |
| 6 | Señala el botón «Recuperar operaciones» del encabezado. Abre `Báscula › Dashboard`: «Ciclos Hoy», «Completados Hoy», «En Proceso» y «Pendientes Repesaje». | “Teclado: Enter guarda o cobra, F2 abre la ventana de peso y Esc la cierra. El tablero resume el día y lleva a la cola.” |

**Cierre:** Ya conoces la pantalla. Empecemos por la operación más simple: solo báscula.

### 5.2 · Solo báscula de principio a fin
**Duración:** 1:10 min · **Rol:** Operario báscula

**OBJETIVO** · Atender un camión que solo se pesa: registro, cobro, peso y tiquete.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID102 con motivo «Solo Bascula» (PREP-5); T1, T4; S1 (precio e IVA de báscula).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Filtra «Sin iniciar» y pulsa VID102. **Verás:** el «Tipo de operación» en «Solo báscula» — «Sin depósito · 1 o 2 pesajes». | “En este video vas a atender un camión que solo se pesa: no deja mercancía, no crea depósito.” |
| 2 | En «Camión y conductor» (con «Faltan N datos») completa «Empresa Transportista» (Transportes Frontera Demo Ltda.), «País de Origen», «Tipo de Vehículo» (Sencillo) y el «Conductor». Mario Demo Benavides aún no está registrado: pulsa «+» junto al selector, completa «Tipo de Documento» (Cédula de Ciudadanía), «Número de Documento» (1000000102), «Apellidos» (Demo Benavides) y «Nombres» (Mario) y pulsa «Registrar conductor». **Verás:** «Conductor registrado» y el selector con «Mario Demo Benavides · CC 1000000102». Pulsa «Listo». | “Báscula completa el camión y el conductor que Vigilancia no registró. El conductor se busca en el selector por nombre o documento; si no existe, se registra con «+». La transportadora y el país se recuerdan para el siguiente camión del turno.” |
| 3 | En «Registro», «Cliente*» elige Comercializadora Andina Demo S.A.S. Deja apagado «Tiene segundo pesaje» («Un solo peso completa la operación.»). Pulsa «Guardar». **Verás:** «Operación registrada» — «Complete el cobro para continuar con el pesaje». | “Solo báscula pide el cliente. Con un solo peso el ciclo se cierra.” |
| 4 | En «Cobro»: destinatario «Tercero registrado» con el cliente; «Modo de pago» «Inmediato»; «Método de pago» «Efectivo»; «Total a pagar» $ 20.000. Pulsa «Cobrar». **Verás:** «Pago registrado» y «Cobrado: $ 20.000 · Efectivo». | “Se cobra antes de pesar. El total incluye el IVA. Ya no se registra efectivo recibido ni cambio: solo el método. La factura queda pagada y Facturación le asigna el número SIIGO.” |
| 5 | En «Peso»: «Peso capturado (kg)» 9.800, «Tipo de peso» «BRUTO (Cargado)», «Fecha y hora del pesaje» propuesta. Pulsa «Registrar peso». **Verás:** «Pesaje completado» — «Ciclo completado». | “La hora del pesaje se propone con la hora actual y se puede corregir.” |
| 6 | En «Tiquete»: «Tiquete 2026T…» y «Observación para el tiquete». Pulsa «Imprimir tiquete». **Verás:** «Ticket generado» — «El PDF se ha descargado y está listo para imprimir». Pulsa «Finalizar». | “El tiquete se entrega al conductor. Al finalizar, el camión sale de la cola y queda listo para salir por Vigilancia.” |

**Cierre:** Pesaje y cobro en un solo flujo. Ahora, el camión que sí deja mercancía: el ingreso con depósito.

### 5.3 · Ingreso con depósito: registrar el documento y la mercancía
**Duración:** 1:24 min · **Rol:** Operario báscula

**OBJETIVO** · Registrar el documento y la mercancía declarada de un camión y crear su depósito.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID101 en la cola (4.1); T1, T4; P1, P3. Crea en cámara el depósito 2026BA00001 de `DEMO-CP-0001`.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa VID101. Deja «Ingreso con depósito» («Con depósito · 1 o 2 pesajes») y completa «Camión y conductor»: Tractomula y, como Luis Demo Castillo (1000000101) aún no está registrado, regístralo con «+» → «Registrar conductor». **Verás:** el selector con «Luis Demo Castillo · CC 1000000101». | “En este video vas a registrar un camión que deja mercancía en un depósito.” |
| 2 | En «Documento»: «Modalidad» «Importación» («Según el motivo de ingreso»), «Tipo de documento*» «Carta Porte» y «Número de documento*» DEMO-CP-0001; pulsa Tab. **Verás:** «Documento nuevo: al guardar se crea un depósito.» | “La carta porte y la modalidad forman el depósito. Al salir del número, el sistema busca si ese documento ya tiene depósito: este es nuevo.” |
| 3 | Escribe «N.º de manifiesto» MAN-DEMO-0001 y «Peso según manifiesto (kg)» 28.000. | “El manifiesto de cada camión lo exige Comercio Exterior para confirmar; si lo tienes a la mano, digítalo aquí.” |
| 4 | En «Mercancía de este camión», «Tipo de carga» «Mercancía suelta». Producto Cebolla cabezona (Saco, Bulto) con «Cantidad de este camión» 600. Pulsa «Agregar producto»: Llantas para camión, 40. **Verás:** «Total de este camión: 640». | “Las cantidades son las declaradas en los documentos: con ellas nace el stock del depósito. Bodega solo cuenta y avisa diferencias.” |
| 5 | Despliega «Datos para Comercio Exterior» («Opcionales en báscula · 0 de 7»). Elige «Cliente» e «Importador»: Comercializadora Andina Demo S.A.S. | “Estos datos son opcionales en báscula para no frenar la fila. Comercio Exterior completa la agencia, la fecha, el valor y la moneda antes de confirmar.” |
| 6 | Despliega «Pesaje y observaciones»: «Fecha de ingreso del depósito» «Vigilancia», «Primer pesaje» «Bruto», «Requiere segundo pesaje» activo. Pulsa «Guardar». **Verás:** «Depósito 2026BA00001 creado» — «Documento DEMO-CP-0001» y el Registro en «Registrado · solo lectura». | “La fecha de ingreso del depósito es la de Vigilancia. El depósito nace en Borrador y Comercio Exterior recibe el aviso. El registro queda en solo lectura: si algo quedó mal, Comercio Exterior corrige los productos mientras el depósito esté en Borrador.” |

**Cierre:** El depósito ya existe. Sigue el cobro.

### 5.4 · El cobro: destinatario, inmediato o por facturar
**Duración:** 0:54 min · **Rol:** Operario báscula

**OBJETIVO** · Cobrar la báscula eligiendo el destinatario y el modo de pago correctos.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID101 registrado (5.3). T6 «Cliente Moroso Demo S.A.S.» en estado Bloqueado (PREP-8).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa VID101 («Por cobrar»). **Verás:** el paso «Cobro» con «Destinatario» en «Tercero registrado» y el cliente del depósito ya elegido. | “En este video vas a cobrar la báscula. Se cobra antes de pesar, y el sistema propone al cliente de la operación.” |
| 2 | Recorre los destinatarios: «Conductor del vehículo» («Se facturará al conductor como persona no registrada; no se crea un tercero.»), «Persona no registrada» y «Consumidor final». | “También se puede facturar al conductor, con sus datos ya cargados; a una persona no registrada; o a consumidor final.” |
| 3 | Elige «Tercero registrado» Cliente Moroso Demo S.A.S. y pulsa «Cobrar». **Verás:** «El cliente 'Cliente Moroso Demo S.A.S.' está bloqueado por deuda pendiente. No se puede proceder con la operación.» y la ficha conserva lo digitado. | “Si el destinatario es un cliente bloqueado por mora, el sistema no deja cobrar a su nombre.” |
| 4 | Vuelve a elegir Comercializadora Andina Demo S.A.S. En «Modo de pago» elige «Por facturar». | “Inmediato registra la factura y el pago en el acto, para quien paga de contado. Por facturar deja la factura para Facturación, para clientes a crédito.” |
| 5 | Pulsa «Cobrar». **Verás:** «Ciclo creado» — «Proceda con el pesaje. La factura quedó pendiente por facturar.» y el resumen «Pendiente por facturar». | “La báscula cobra solo lo de este camión, siempre en una factura individual. Después del cobro, el modo de pago ya no se cambia aquí: Facturación registra el pago.” |

**Cierre:** Cobro hecho. Ahora, los pesos y el tiquete.

### 5.5 · Primer peso, llegada a Bodega, segundo peso y tiquete
**Duración:** 0:55 min · **Rol:** Operario báscula

**OBJETIVO** · Tomar el primer y el segundo peso de un ingreso con depósito y entregar el tiquete.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID101 cobrado (5.4). Entre las dos tomas, Bodega registra la llegada de VID101 (video 6.1).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa «Capturar peso» en VID101. **Verás:** «Peso» con «Pesaje 1 de 2». Escribe «Peso capturado (kg)» 34.500 con «Tipo de peso» «BRUTO (Cargado)» y señala la ayuda «Por defecto: la hora actual. Puede corregirla dentro de la estadía del camión.». Pulsa «Registrar peso». **Verás:** «Peso registrado. El ciclo queda abierto.» | “En este video vas a completar el pesaje. El primer peso es con el camión cargado: el bruto.” |
| 2 | Pulsa «Salir y atender otro camión». **Verás:** «Ciclo abierto» — «El ciclo quedó abierto: retómelo desde la cola cuando el camión regrese.». Filtra «Por repesar»: VID101 con la etiqueta «Falta llegada a Bodega». | “El camión va a descargar. El segundo peso exige que Bodega registre su llegada: mientras tanto, la cola lo marca.” |
| 3 | (Segunda toma, después de 6.1.) En «Por repesar», VID101 ya no tiene la etiqueta. Pulsa «Capturar peso» y luego F2. **Verás:** la ventana «Captura de peso» con la placa, el conductor y el cliente. | “Bodega ya registró la llegada. Con F2 el peso se captura en una ventana grande.” |
| 4 | Escribe 6.500 con «TARA (Vacío)». **Verás:** «Neto (bruto − tara)» con 28.000. Pulsa «Registrar peso». **Verás:** «Pesaje completado» — «Ciclo completado». | “El segundo peso es la tara, con el camión vacío. El neto es bruto menos tara. La tara nunca puede superar el bruto: el sistema lo impide con «La tara … no puede ser mayor que el peso bruto …».” |
| 5 | En «Tiquete»: «Tiquete 2026T…» con «Bruto (cargado)», «Tara (vacío)» y «Neto — Bruto − tara». Pulsa «Imprimir tiquete» [verificar en pantalla el PDF «ORDEN DE PESO No.»] y luego «Finalizar». | “Imprimimos el tiquete para el conductor y finalizamos: el camión queda listo para salir por Vigilancia.” |

**Cierre:** Ciclo completo. Veamos los camiones con unidades de carga y el depósito por inspección.

### 5.6 · Ingreso con unidades de carga e inspección
**Duración:** 1:32 min · **Rol:** Operario báscula

**OBJETIVO** · Registrar un camión con tanquero o contenedor y un depósito por inspección.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID103 y VID104 en la cola (PREP-5); T1, T2; P1, P2.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa VID103: «Ingreso con depósito», «Importación», «Carta Porte» DEMO-CP-0002. **Verás:** «Documento nuevo: al guardar se crea un depósito.». Completa «Camión y conductor». | “En este video vas a registrar dos casos especiales. El primero: un camión que trae un tanquero.” |
| 2 | En «Tipo de carga» elige «Unidades de carga». En «Unidades de carga»: «Tipo de unidad*» Tanquero y «Placa o identificación*» TQD9001. Producto Aceite de palma a granel, Litro, 30.000. **Verás:** «La mercancía del camión queda en la unidad TQD9001.» | “La unidad de carga es el contenedor, tanquero o remolque que entra con el camión: se pesa con él, se anota su placa, Bodega la recibe completa sin contar producto y sale completa o por partes.” |
| 3 | En «Datos para Comercio Exterior» elige «Cliente» e «Importador»: Distribuidora Nariño Demo S.A.S. Pulsa «Guardar». **Verás:** «Depósito 2026BA00002 creado». Cobra («Inmediato») y registra el primer peso. | “El cobro y el primer peso son iguales a los de cualquier ingreso.” |
| 4 | Pulsa VID104: «Ingreso con depósito», «Modalidad» «Inspección», DEMO-CP-0003, Cebolla cabezona, 200; «Cliente» Comercializadora Andina Demo S.A.S. En «Pesaje y observaciones», «Primer pesaje» queda fijo en «Bruto» y «Requiere segundo pesaje», apagado. | “El segundo caso es el depósito por inspección: la mercancía espera la inspección de la DIAN y lleva un solo pesaje.” |
| 5 | Pulsa «Guardar». **Verás:** «Depósito 2026INSP00001 creado». Cobra, pesa con «BRUTO (Cargado)» y **verás** «Pesaje completado» y el tiquete. | “Con un solo peso, el ciclo se cierra. Algo parecido pasa con el Flujo perecederos: cierra con el primer peso.” |

**Cierre:** Ya sabes registrar unidades de carga e inspecciones. Veamos qué pasa cuando llega otro camión con el mismo documento.

### 5.7 · Varios camiones con el mismo documento
**Duración:** 1:04 min · **Rol:** Operario báscula

**OBJETIVO** · Asociar un segundo camión al depósito de una carta porte que ya existe.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · 2026BA00001 en Borrador con VID101 (5.3) y VID105 en la cola (PREP-5).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa VID105: «Ingreso con depósito», «Carta Porte» DEMO-CP-0001, Tab. **Verás:** «Se asociará al depósito 2026BA00001 (Borrador) · Camiones ingresados: 1» y el enlace «Ver camiones». | “En este video vas a registrar el segundo camión de un documento. Una carta porte puede llegar en varios camiones, y todos van al mismo depósito.” |
| 2 | Pulsa «Ver camiones». **Verás:** la tabla «Placa», «Tiquete», «Fecha» y «Cantidad declarada». | “Vemos qué camiones ya entraron con este documento.” |
| 3 | En «Mercancía de este camión» **verás** las líneas del depósito precargadas («Vacía si no la trae») y «Lo fijó el primer camión del documento.» en el tipo de carga. Escribe 400 en Cebolla cabezona y deja vacía Llantas para camión. | “La modalidad y el tipo de carga los fijó el primer camión. Digitamos solo lo que trae este. Los datos del depósito están en solo lectura.” |
| 4 | Pulsa «Guardar». **Verás:** «Camión asociado al depósito 2026BA00001». Cobra y registra el primer peso. | “La cantidad de este camión se suma al stock del depósito, y el cobro es solo de este camión.” |
| 5 | Muestra una diapositiva con el bloqueo: «El ingreso de camiones de este documento fue cerrado por {nombre} el {fecha}.» | “Cuando Comercio Exterior cierra el ingreso de camiones del documento, báscula ya no puede asociar más camiones y ve quién lo cerró y cuándo. Tampoco se acepta un camión del mismo documento con otra modalidad.” |

**Cierre:** Varios camiones, un depósito. Ahora el caso contrario: un camión con dos depósitos.

### 5.8 · Multidepósito: agregar otro depósito
**Duración:** 1:38 min · **Rol:** Operario báscula

**OBJETIVO** · Registrar dos depósitos en el mismo camión y entender la factura en cero.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID106 en la cola (PREP-5); T1, T2; P1, P3.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa VID106: «Ingreso con depósito», DEMO-CP-0004, Cebolla cabezona 300 y Llantas para camión 20, «Cliente» Comercializadora Andina Demo S.A.S. Pulsa «Guardar» («Depósito 2026BA00003 creado»), cobra con «Inmediato» y registra el primer peso, 33.000 kg, en bruto. | “En este video vas a registrar un camión que trae mercancía de dos documentos.” |
| 2 | En «Peso registrado. El ciclo queda abierto.» pulsa «Agregar otro depósito». **Verás:** «Depósito adicional» — «Complete los datos del nuevo depósito para el mismo camión.», la marca «Depósito adicional» y la nota «… modalidad … y pesaje heredados …». | “Cada documento es un depósito independiente, con su cliente, sus terceros, su valor y su moneda. Solo comparten el vehículo, el ciclo de pesaje y la modalidad.” |
| 3 | Escribe DEMO-CP-0005 (nuevo), Cebolla cabezona 150 y «Cliente» Distribuidora Nariño Demo S.A.S. Pulsa «Guardar». **Verás:** «Camión asociado al depósito 2026BA00004». | “El depósito adicional necesita un documento propio: si el número ya existe, el sistema lo rechaza.” |
| 4 | **Verás:** «Depósito adicional — factura en cero. El ciclo de báscula ya tiene su cobro principal. Elija a quién se emite la factura en cero.» Deja el destinatario propuesto y pulsa «Confirmar y continuar». **Verás:** «Depósito adicional agregado» y «Depósito adicional: factura en $0». | “La báscula cobra una sola vez por camión: el depósito adicional lleva una factura en cero, que no lleva número fiscal.” |
| 5 | En «Pesaje 2» elige «INTERMEDIO», escribe 26.000 y pulsa «Registrar peso». | “El pesaje intermedio marca la salida de la mercancía del primer depósito y la entrada del nuevo. El pesaje final, con el camión vacío, se toma como en el video 5.5.” |

**Cierre:** Un camión, dos depósitos, un solo cobro. Sigue la salida de mercancía con su orden de cargue.

### 5.9 · Salida de mercancía con orden de cargue
**Duración:** 1:12 min · **Rol:** Operario báscula

**OBJETIVO** · Pesar un camión que retira mercancía con una orden de cargue.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · La orden 2026OC00001 (7.10) y VID108 en la cola con «Cargue mercancia importacion» (PREP-6). Entre las tomas, Bodega carga la orden (6.6) y Comercio Exterior emite la guía (7.12).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa VID108. **Verás:** «Salida de mercancía» — «Con orden de cargue · 1 o 2 pesajes». Completa «Camión y conductor»: en el selector «Conductor» escribe «jaime» (o parte de la cédula 1000000108) y elige «Jaime Demo Revelo · CC 1000000108», registrado en la orden de cargue (7.10). | “En este video vas a pesar un camión que viene a llevarse mercancía.” |
| 2 | En «Buscar orden por» deja «Número de orden», escribe DEMO-OC-0001 en «Número de orden de cargue» y pulsa Enter. **Verás:** «Orden encontrada» y el resumen «OC 2026OC00001», «Externa DEMO-OC-0001 · …», «Solicitada» y «Cargada» «Aún no cargada». | “La orden se busca por su número interno, por el externo o por la placa.” |
| 3 | En «Cómo sale» deja «Pesar en báscula», «Primer peso» «TARA (Vacío)» y «Requiere segundo pesaje» marcado. Pulsa «Guardar». **Verás:** «Orden de cargue validada» — «Orden: 2026OC00001». | “La orden pasa a en cargue: Bodega ya puede cargarla. Solo salen depósitos confirmados.” |
| 4 | Cobra («Tercero registrado» Comercializadora Andina Demo S.A.S., «Inmediato») y registra la tara, 14.000 kg. Señala el enlace «Agregar otra orden a este pesaje». Pulsa «Salir y atender otro camión». | “Primer peso con el camión vacío. Si el camión se lleva otras órdenes, se agregan a este mismo pesaje, sin otro cobro.” |
| 5 | (Segunda toma, después de 6.6 y 7.12.) En «Por repesar» pulsa «Capturar peso» en VID108, escribe 24.500 con «BRUTO (Cargado)» y pulsa «Registrar peso». **Verás:** «Pesaje completado» y el tiquete. Pulsa «Finalizar». | “El repesaje exige la orden cargada y, en importación, la guía vigente. Sin cargue, el sistema responde «No se puede cerrar el pesaje de salida: la orden … aún no está cargada …». Ninguna mercancía de importación sale sin guía.” |
| 6 | Muestra una diapositiva con las dos opciones de «Cómo sale»: «Pesar en báscula» y «Con el tiquete de ingreso», con su texto «Sin pesar ni cobrar: sale con el tiquete de ingreso.». | “Un camión que trajo la mercancía también puede salir con su tiquete de ingreso, sin pesar ni cobrar, pero solo con la mercancía que llegó en ese tiquete.” |

**Cierre:** Salida completa. Veamos cómo retomar o descartar una operación que quedó a medias.

### 5.10 · Retomar y descartar operaciones
**Duración:** 0:51 min · **Rol:** Operario báscula

**OBJETIVO** · Retomar una operación interrumpida o descartarla antes del cobro.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · VID111 registrada en «Solo báscula» y sin cobrar (PREP-5).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Báscula › Proceso de Pesaje` pulsa «Recuperar operaciones». **Verás:** «Recuperar operaciones de báscula» y el texto «Retome operaciones que quedaron sin completar…». | “En este video vas a recuperar operaciones. Si una operación quedó a medias, aquí la encuentras.” |
| 2 | Señala las columnas «Placa», «Conductor», «Cliente», «Tipo», «Estado» (VID111 en «Sin ciclo (abandonada)») y el filtro «Placa:». | “El estado dice dónde quedó: sin ciclo es registrada y sin cobrar.” |
| 3 | Pulsa «Retomar» en VID111. **Verás:** «Operación restaurada» — «Puede continuar desde donde quedó» y la ficha en el paso «Cobro», con el registro en solo lectura. Pulsa «Soltar camión». | “Retomar abre la ficha justo donde quedó. Desde la cola se hace lo mismo con los camiones por cobrar, por pesar o por repesar.” |
| 4 | Vuelve a «Recuperar operaciones» y pulsa «Descartar» en VID111. **Verás:** «Descartar operación» — «¿Descartar la operación abandonada del vehículo VID111? …». Pulsa «Descartar». **Verás:** «Operación descartada» — «Vehículo VID111». | “Si el registro está mal y aún no se cobró, se descarta. Si había creado un depósito, este queda anulado.” |
| 5 | Vuelve a la cola, filtra «Sin iniciar». **Verás:** VID111 de nuevo. | “El camión vuelve a Sin iniciar para registrarlo bien. Una operación ya cobrada no se descarta: se anula el pesaje desde el historial.” |

**Cierre:** Ninguna operación se pierde. Veamos el historial: correcciones, anulaciones y reimpresiones.

### 5.11 · Historial de báscula: corregir, anular y reimprimir
**Duración:** 1:07 min · **Rol:** Operario báscula

**OBJETIVO** · Consultar los pesajes, corregir un peso con su razón, reimprimir un tiquete y anular un pesaje.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · Ciclos del recorrido (VID102 completo). VID113 con su pesaje terminado: el historial solo muestra ciclos cerrados.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Báscula › Historial`. **Verás:** «Historial de Báscula», las tarjetas «Entradas», «Salidas», «Completos» y «En Proceso», las pestañas «Entradas» y «Salidas», la barra de totales y «Exportar Excel». | “En este video vas a trabajar con el historial. Aquí el tiquete aparece como Ticket.” |
| 2 | Señala «Placa», «Estado» y «Más filtros» («Ticket», «Factura», «Carta Porte», «Desde», «Hasta», «Cliente», «En ceros», «Por cobrar», «No impresos»). | “Con los filtros ubicas cualquier pesaje; el Excel exporta lo filtrado.” |
| 3 | Pulsa el ojo «Ver detalle» del tiquete de VID102. **Verás:** «Detalle del Ciclo de Báscula», «Pago inmediato», «Pesajes» con «Operario: …» y la sección «Factura». | “El detalle muestra los pesos, quién los tomó y la factura.” |
| 4 | Pulsa «Editar» junto al peso. En «Modificar Pesaje 1 (Bruto)», escribe «Nuevo Peso (Bruto)» 9.850 y «Razón de la Modificación» Peso digitado con error; la báscula marcaba 9.850 kg. Pulsa «Confirmar Modificación». **Verás:** «Modificación exitosa» y la nota «Peso modificado. Original: … / Modificado por: … / Razón: …». | “Corregir un peso exige una razón de al menos 10 caracteres y deja el autor a la vista. El administrador recibe el aviso. Pueden hacerlo Báscula, Facturación y el Administrador. La fecha del pesaje se corrige igual, con Editar junto a la fecha.” |
| 5 | Pulsa «Imprimir Ticket». En «Observaciones del Ticket» pulsa «Guardar e Imprimir». | “El tiquete se reimprime cuando haga falta, con observaciones si se necesitan.” |
| 6 | Abre el detalle de VID113 y pulsa «Anular pesaje». En «Motivo» escribe Pesaje registrado por error en el turno de prueba (mínimo 10 caracteres) y pulsa «Anular pesaje». **Verás:** «Pesaje anulado» con sus listas de resultados. | “Anular devuelve el ingreso a la cola. Un cobro ya pagado sigue pagado y Facturación lo revisa. Y el modo de pago de un cobro ya no se cambia aquí: se paga en Facturación.” |

**Cierre:** El historial guarda y corrige todo con trazabilidad. Cerramos con el reporte diario.

### 5.12 · Reporte de Facturación Diaria
**Duración:** 0:38 min · **Rol:** Operario báscula

**OBJETIVO** · Consultar y descargar el reporte de facturación del día, tiquete por tiquete.
**GRABA CON** · `video.bascula` (C3).
**REQUISITOS** · Tiquetes del día: ingresos, salidas y solo báscula.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Báscula › Reportes`. **Verás:** «Reporte de Facturación Diaria» — «Consolidado de operaciones y facturación por día», con «Día anterior», «Día siguiente», el selector de fecha y «Hoy». | “En este video vas a consultar el reporte diario. Muestra un día a la vez.” |
| 2 | Señala los indicadores «Total Operaciones», «Completados», «Ingresos», «Salidas», «Peso Neto Total» y «Total Facturado». | “Arriba, el resumen del día.” |
| 3 | Señala «Detalle de Operaciones»: una fila por tiquete con «Ticket», «Placa», «Destinatario», «Tipo» («Ingreso», «Salida», «Solo Pesaje»), «Subtotal», «IVA», «Total» y «Hora». Luego «Resumen por Tipo de Operación» y «Totales del Día». | “Cada tiquete con su destinatario y su IVA. Cuadra con el historial y el tablero: todos usan el día de Colombia.” |
| 4 | Pulsa «Descargar PDF». **Verás:** «PDF descargado correctamente» y el PDF «REPORTE DE FACTURACIÓN DIARIA». | “Lo descargamos para el arqueo del día. El Excel, si lo necesitas, está en el historial.” |

**Cierre:** Con esto termina Báscula. La mercancía pesada pasa ahora a la bodega.

## Serie 6 · Bodega

9 videos · Rol Operario bodega. Bodega registra la llegada de los camiones, cuenta, ubica y fotografía la mercancía, cobra el montacargas, carga las órdenes y cuida el inventario. Ojo: **la recepción no crea ni mueve stock**; el stock del depósito es lo declarado en báscula. Bodega informa las diferencias a Comercio Exterior. Graba con `video.bodega` (dataset C4).

### 6.1 · Cómo registrar la llegada del camión
**Duración:** 0:40 min · **Rol:** Operario bodega

**OBJETIVO** · Registrar que el camión llegó a Bodega y empezó la descarga.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · VID101 con el primer peso (5.5, primera toma).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Inicia sesión con `video.bodega`. **Verás:** `Bodega › Dashboard` con «Módulo de Bodega/Patio» y sus tarjetas «Ingresos», «Recepción», «Historial Recepciones», «Registrar Uso Montacargas», «Historial Montacargas», «Órdenes de Cargue» e «Inventario». | “En este video vas a registrar la llegada de un camión. El tablero de Bodega lleva a cada tarea.” |
| 2 | Abre `Bodega › Recepciones › Ingresos`. **Verás:** «Ingresos a Bodega» — «Camiones listos para descargar. Registre la llegada cuando los operarios inicien la descarga.» y la tarjeta de VID101 con su depósito, «Conductor», «Cliente», «Productos del depósito» y «Pesaje». | “Aquí aparecen los camiones que ya tienen su primer peso. La tarjeta dice qué trae este camión y cuánto ampara todo el documento.” |
| 3 | Pulsa «Ingresar» en VID101. **Verás:** «Llegada registrada» — «Camión VID101 · Depósito 2026BA00001 - Hora de ingreso registrada» y la tarjeta sale de la lista. | “Este paso es obligatorio: sin la llegada, la báscula no puede tomar el segundo peso, y en su cola el camión aparece con Falta llegada a Bodega.” |
| 4 | Señala «Filtrar por placa...» y «Actualizar». | “Con el filtro ubicas un camión cuando hay varios esperando.” |

**Cierre:** El camión ya está en descarga. Ahora completamos la recepción.

### 6.2 · Cómo completar la recepción de mercancía
**Duración:** 1:01 min · **Rol:** Operario bodega

**OBJETIVO** · Registrar lo que se contó, dónde quedó, la firma del conductor y las fotos.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · Llegada de VID101 (6.1). U1, U2 y Q1 (Serie 1). Fotos ARCH-1. Alguien que firme como conductor.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Bodega › Recepciones › Recepción`. **Verás:** «Recepciones en Bodega» y «Camiones con Ingreso Registrado» con VID101. Pulsa «Completar recepción». | “En este video vas a completar una recepción.” |
| 2 | **Verás:** «Completar Recepción Física» con «Información del Depósito»: vehículo, conductor, importador, cliente y «Datos de transporte». | “Arriba confirmamos de qué camión y de qué depósito se trata.” |
| 3 | En «Productos descargados», en Cebolla cabezona («Declarado para este camión: 600 · Unidad: Bulto · Embalaje: Saco»), cambia «Cantidad descargada» de 600 a 598 y elige «Ubicación en bodega» A01-R01-N01. En Llantas para camión deja 40 y elige PATIO-01. **Verás:** «Diferencia con lo declarado para este camión:», «Cebolla cabezona: −2 …» y «El stock del depósito no cambia; se notificará a Comercio Exterior.» | “La cantidad viene precargada con lo declarado: la cambiamos por lo que contamos. Bodega no mueve el stock: si lo contado difiere, Comercio Exterior recibe el aviso y decide si ajusta la cantidad. Un producto declarado y no contado cuenta como faltante.” |
| 4 | Elige «Cuadrilla que descargó» Cuadrilla A y escribe «Comentarios (Opcional)». | “Anotamos qué cuadrilla descargó.” |
| 5 | Pulsa «Capturar Firma». En «Capturar Firma del Conductor», haz firmar y pulsa «Guardar Firma». **Verás:** «Firma capturada exitosamente» y «Firma Capturada». | “La firma del conductor es obligatoria: sin ella no se completa la recepción.” |
| 6 | En «Fotos de la Mercancía (Opcional)» pulsa «Seleccionar Fotos» y elige tres. **Verás:** «3 / 5». | “Hasta cinco fotos JPG, PNG o WebP de máximo 5 MB cada una.” |
| 7 | Pulsa «Completar Recepción». **Verás:** «Recepción completada» — «La recepción fue registrada exitosamente». | “Quien completa la recepción queda registrado como responsable.” |

**Cierre:** Mercancía contada, ubicada y firmada. Veamos cómo se reciben las unidades de carga.

### 6.3 · Cómo recibir unidades de carga
**Duración:** 0:37 min · **Rol:** Operario bodega

**OBJETIVO** · Recibir un tanquero o contenedor completo, sin contar producto por producto.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · VID103 con el tanquero TQD9001 y su primer peso (5.6).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Bodega › Recepciones › Ingresos`, pulsa «Ingresar» en VID103. **Verás:** «Llegada registrada». | “En este video vas a recibir una unidad de carga. Primero, como siempre, la llegada.” |
| 2 | En `Bodega › Recepciones › Recepción` pulsa «Completar recepción» de VID103. **Verás:** en «Datos de transporte», «Unidades de carga:» con TQD9001. | “Este camión trae un tanquero.” |
| 3 | **Verás:** «Unidades de carga del camión» en lugar de los productos: Tanquero TQD9001, «Aceite de palma a granel — 30.000 …» y la casilla «Recibida completa». Captura la firma y pulsa «Completar Recepción» sin marcarla (el botón se habilita con la firma). **Verás:** «Confirme todas las unidades de carga del camión». | “En una unidad de carga no se cuenta producto por producto: se confirma que llegó completa.” |
| 4 | Marca «Recibida completa» y pulsa «Completar Recepción». **Verás:** «Recepción completada». | “Confirmada la unidad y firmada la recepción, el tanquero queda en bodega.” |

**Cierre:** Unidad recibida. Veamos ahora los camiones que no pasan por báscula.

### 6.4 · Recepción directa (sin báscula)
**Duración:** 1:14 min · **Rol:** Operario bodega

**OBJETIVO** · Recibir la mercancía de un camión que no pasa por báscula y crear su depósito.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · VID107 con motivo «Solo bodega» (PREP-5); T1; P1; U2.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Bodega › Recepciones › Recepción` pulsa «Recepción Directa». **Verás:** «Recepción Directa - Seleccionar Ingreso» con «Ingresos Directos Pendientes» — «Sin pesaje en báscula». Pulsa «Recibir» en VID107. | “En este video vas a hacer una recepción directa. Es para los camiones cuyo motivo no pide pesaje, normalmente Solo bodega.” |
| 2 | **Verás:** «Recepción Directa Sin Báscula» y el aviso «Ingreso excepcional. Placa: VID107. Esta operación queda registrada para auditoría.». En «Conductor», Hugo Demo Ortiz aún no está registrado: pulsa «+», completa «Tipo de Documento» (Cédula de Ciudadanía), «Número de Documento» (1000000107), «Apellidos» (Demo Ortiz) y «Nombres» (Hugo) y pulsa «Registrar conductor». **Verás:** el selector con «Hugo Demo Ortiz · CC 1000000107». Completa el vehículo («Empresa Transportista», «País de Origen», «Tipo de Vehículo»). | “Como el camión no pasó por báscula, aquí se eligen el conductor y el vehículo. El conductor se busca por nombre o documento; si no existe, se registra con «+».” |
| 3 | Escribe «Carta Porte*» DEMO-CP-0010; señala «Modalidad» fija en «INSP - Inspección». Elige «Cliente*» Comercializadora Andina Demo S.A.S., «Producto*» Cebolla cabezona, «Cantidad del Documento*» 80 y «Unidad de Medida*» Bulto. | “La recepción directa opera bajo la modalidad de inspección. La cantidad del documento es la declarada: será el stock del depósito.” |
| 4 | En «Recepción Física»: «Cantidad Descargada*» 80 y «Ubicación en Bodega*» PATIO-01; captura la firma. En «Motivo*» escribe Camión de entrega local sin pesaje; mercancía para inspección. | “Aquí la ubicación y la firma son obligatorias, y hay que explicar por qué no pasó por báscula.” |
| 5 | Pulsa «Completar Recepción Manual». **Verás:** «Recepción directa completada» — «La recepción sin báscula fue registrada exitosamente». | “Se crea el depósito en Borrador para que Comercio Exterior lo complete y lo confirme. Si el cliente está bloqueado por mora, el sistema rechaza la recepción.” |

**Cierre:** Recepción sin báscula lista. Sigue el montacargas y su cobro.

### 6.5 · Cómo registrar el uso del montacargas y cobrarlo
**Duración:** 0:59 min · **Rol:** Operario bodega

**OBJETIVO** · Registrar el inicio y el fin de un uso de montacargas y cobrarlo.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · VID105 con su servicio de báscula (5.7). Tarifas de montacargas S6 (1.9).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Bodega › Montacargas › Registrar uso`. **Verás:** «Registrar Uso de Montacargas». Pulsa «Iniciar Uso». | “En este video vas a registrar y cobrar el montacargas.” |
| 2 | En «Iniciar Uso de Montacargas» escribe «Placa del Vehículo *» VID105 y pulsa «Buscar». **Verás:** la placa con «Cliente: …». Escribe «Horómetro Inicial (horas) *» 1250, elige «Tipo de vehículo *» Tractomula y pulsa «Iniciar Uso». **Verás:** «Uso de montacargas iniciado exitosamente» y «1 montacargas en uso». | “No se elige el cliente: sale del servicio del camión. El uso puede empezar aunque Comercio Exterior aún no haya asignado el cliente.” |
| 3 | En la fila del uso pulsa «Finalizar». Escribe «Horómetro Final (horas) *» 1251,5. **Verás:** «Horas trabajadas: 1,50 h». Pulsa «Continuar al cobro». | “El horómetro final debe ser mayor que el inicial. Las horas son informativas: el cobro no es por hora.” |
| 4 | En «Facturación y Cobro — Montacargas»: «Destinatario» «Tercero registrado» con el cliente; «Valor del servicio (sin IVA)» con 220.000 y la ayuda «Precargado automáticamente…». Marca «Agregar IVA (19%)». **Verás:** «Subtotal», «IVA (19%)» y «Total a pagar» $261.800. | “La tarifa sale del tipo de vehículo o del convenio del cliente, y se puede ajustar. El IVA se suma solo si marcamos la casilla.” |
| 5 | Elige «Modo de pago» «Pago inmediato» y «Método de Pago» «Transferencia Bancaria». Pulsa «Finalizar y cobrar». **Verás:** «Uso finalizado. Costo: $ 261.800 (1,50 horas)», con el IVA incluido. | “Pendiente por facturar dejaría la factura para Facturación. Un cliente bloqueado por mora no puede cerrar un uso de montacargas.” |
| 6 | Abre `Bodega › Montacargas › Historial`. **Verás:** «Historial de Montacargas» con «Valor (sin IVA)», «IVA», «Total», «Modo de pago» y «Factura». | “El historial muestra cada uso con su cobro.” |

**Cierre:** Montacargas cobrado. Pasemos a la salida de mercancía: la orden de cargue.

### 6.6 · Cómo ejecutar una orden de cargue
**Duración:** 0:59 min · **Rol:** Operario bodega

**OBJETIVO** · Verificar y cargar una orden de cargue, con firma del conductor.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · La orden 2026OC00001 «en cargue» (5.9, primera toma). Mercancía ubicada (6.2). Alguien que firme.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Bodega › Órdenes de Cargue`. **Verás:** «Órdenes de Cargue», las pestañas «Pendientes» y «Todas las Órdenes» y la tarjeta de VID108 en «En Proceso», con sus ítems «pedido / disponible». | “En este video vas a cargar una orden. Aquí están las pendientes.” |
| 2 | Pulsa «Ver». **Verás:** «Detalle de Orden de Cargue» con «Información General», «Items de la Orden» y «Historial». Pulsa «Imprimir orden de trabajo». **Verás:** «Orden de trabajo» — «El documento se descargó correctamente.» | “Verificamos qué se va a cargar. La orden de trabajo es para la cuadrilla.” |
| 3 | Vuelve y pulsa «Ejecutar». **Verás:** «Ejecutar Orden de Cargue», «Items a cargar:» con «Cantidad cargada» precargada y «Todo el stock está disponible para cargar». | “Se puede cargar menos de lo pedido: lo que no se carga se libera de la reserva.” |
| 4 | Elige «Cuadrilla que cargó» Cuadrilla A, captura la firma del conductor y, si quieres, agrega fotos en «Fotos del Cargue (Opcional)». | “La firma del conductor es obligatoria también en el cargue.” |
| 5 | Pulsa «Ejecutar Cargue». **Verás:** «Confirmar Ejecución» — «¿Confirmar ejecución del cargue para la orden 2026OC00001?». Pulsa «Aceptar». **Verás:** «Cargue ejecutado exitosamente» y la tabla con «Stock anterior», «Stock nuevo», «Reserva liberada» y «Retirar de». | “El stock se descuenta en este momento. Retirar de dice de qué ubicaciones sacar la mercancía. En importación, Comercio Exterior recibe el aviso Guía de salida requerida.” |
| 6 | Pulsa «Cerrar». Señala, en el detalle de otra orden, el botón «Cancelar Orden». | “Bodega puede cancelar una orden con motivo. Revertir una salida o devolver un depósito lo hace Comercio Exterior; Bodega recibe el aviso.” |

**Cierre:** Orden cargada. Veamos el inventario y las ubicaciones.

### 6.7 · Inventario, kárdex y ubicaciones
**Duración:** 0:58 min · **Rol:** Operario bodega

**OBJETIVO** · Consultar el stock de un depósito, sus movimientos y mover mercancía entre ubicaciones.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · 2026BA00001 con movimientos (cargue de 6.6). U3–U5 (PREP-3), con A01-R02-N01 no disponible.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Bodega › Inventario`. **Verás:** «Inventario y Movimientos» y las pestañas «Consultar Stock», «Movimientos» y «Ubicaciones». | “En este video vas a consultar el inventario.” |
| 2 | En «Consultar Stock», escribe 2026BA00001 en «N° Depósito». **Verás:** «Depósito: 2026BA00001 – 2 producto(s)» con «Stock Actual», «Stock Reservado» y «Stock Disponible». | “Escribe el número completo del depósito. También aparecen los depósitos en Borrador que ya tienen mercancía recibida, con la etiqueta Borrador.” |
| 3 | Pulsa «Ubicaciones» en Cebolla cabezona. **Verás:** «Ubicaciones de Cebolla cabezona · depósito 2026BA00001» con «Existencias», «Ubicadas» y «Por ubicar». Pulsa «Mover» en A01-R01-N01, elige «Hacia» A01-R01-N02, «Cantidad» 100 y pulsa «Mover». **Verás:** «Mercancía movida». | “Aquí ubicamos, movemos o liberamos mercancía. Las ubicaciones no disponibles no aparecen en la lista.” |
| 4 | Abre «Movimientos». **Verás:** las columnas «Tipo», «Cantidad», «Stock anterior», «Stock nuevo», «Origen» y «Usuario», con orígenes «Ingreso declarado» y «Orden cargue». Señala «Exportar Excel». | “El kárdex registra cada entrada y salida. La recepción no genera movimiento: la entrada es el ingreso declarado en báscula.” |
| 5 | Abre «Ubicaciones» y elige A01-R02-N01. **Verás:** «Disponible: No». | “Desde aquí se ve qué hay en cada posición.” |

**Cierre:** Bodega no ajusta cantidades: eso lo hace Comercio Exterior con el CE-7, y aquí se ve como Ajuste CE-7. Para mercancía dañada o faltante, Bodega registra una novedad: es el siguiente video.

### 6.8 · Novedades de mercancía
**Duración:** 0:59 min · **Rol:** Operario bodega

**OBJETIVO** · Registrar mercancía dañada, faltante o sobrante e imprimir su reporte.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · 2026BA00001 con stock y la recepción de VID101 (6.2).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Bodega › Novedades` y pulsa «Nueva novedad». Elige «Depósito*» 2026BA00001 y «Producto*» Cebolla cabezona, y pulsa «Continuar». | “En este video vas a registrar una novedad: mercancía dañada, faltante o sobrante. También se registra desde el inventario con Registrar novedad.” |
| 2 | En «Registrar novedad · Cebolla cabezona · depósito 2026BA00001» deja «Inicio» y «Fin», elige «Tipo de novedad» «Rutina», «Camión» VID101 y escribe «Descripción*» Sacos rotos al reubicar en el pasillo A. | “Describimos qué pasó y con qué camión.” |
| 3 | Escribe «Dañada» 2. **Verás:** que «Buena» se ajusta sola. Cambia «Buena» a mano por un número que no cuadre. **Verás:** «La suma de buena, dañada y faltante (…) no coincide con el total (…).». Corrígelo. Elige «Carpa» «Buena» y «Remolque» «Limpio». | “El desglose debe cuadrar con el total. Si no cuadra, el sistema avisa y pide confirmar antes de guardar.” |
| 4 | Pulsa «Registrar novedad». **Verás:** «Novedad registrada» — «Comercio Exterior recibe el aviso.» | “Con dañada, faltante o sobrante, Comercio Exterior recibe el aviso.” |
| 5 | Pulsa «Imprimir» en la fila. **Verás:** el PDF «REPORTE DE MERCANCÍAS». | “El reporte de mercancías se imprime para firmar y archivar.” |
| 6 | Señala «Anular», el filtro «Incluir anuladas» y «Exportar Excel». | “Una novedad se anula con motivo y su reporte queda marcado ANULADA.” |

**Cierre:** Novedad registrada y avisada. Cerramos con el inventario general y los historiales.

### 6.9 · Inventario general e historiales de Bodega
**Duración:** 0:47 min · **Rol:** Operario bodega

**OBJETIVO** · Consultar el inventario de todos los depósitos y los historiales de recepción.
**GRABA CON** · `video.bodega` (C4).
**REQUISITOS** · Depósitos del recorrido con saldo y recepciones completadas.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Bodega › Inventario general`. **Verás:** «Inventario general» — «Inventario de todos los depósitos, por importador, agencia, transportadora, producto, modalidad o ubicación.» | “En este video vas a consultar el inventario general y los historiales.” |
| 2 | Deja «Saldo» en «Con saldo», marca «Incluir levantes» y pulsa «Consultar». **Verás:** las columnas «Depósito», «Entran», «Nalzdos.», «Salen», «Saldo» y «Levantes», y el pie «Totales». Pulsa «Exportar Excel». | “Con Todos hay que indicar un rango de fechas de ingreso. Los totales cubren todo el filtro.” |
| 3 | Abre `Bodega › Recepciones › Historial`. **Verás:** «Historial de Recepciones» con «Contado Bodega» y la etiqueta «Diferencia: −2» de VID101. | “El historial de recepciones muestra qué se contó y las diferencias.” |
| 4 | Pulsa el ojo «Ver detalle». **Verás:** «Detalle de Recepción» con «Fotos de la Mercancía» y «Firma del Conductor». | “Cada recepción guarda sus fotos y la firma.” |
| 5 | Abre `Notificaciones › Notificaciones`. | “En Notificaciones, Bodega recibe los avisos de órdenes canceladas o modificadas, salidas revertidas y depósitos anulados.” |

**Cierre:** Con esto cerramos Bodega. La gestión aduanera del depósito ocurre en Comercio Exterior.

## Serie 7 · Comercio Exterior

15 videos · Rol Comercio exterior. Comercio Exterior es el dueño del depósito: lo completa, lo confirma, imprime la etiqueta, registra los levantes, crea las órdenes de cargue y emite las guías de salida. Al confirmar se dispara el cobro del almacenamiento. Al iniciar sesión, Comercio Exterior llega a `Dashboards › Trazabilidad` (video 0.5). Graba con `video.comext` (dataset C5).

### 7.1 · El tablero y el Kanban de depósitos
**Duración:** 0:54 min · **Rol:** Comercio exterior

**OBJETIVO** · Ubicar los depósitos de importación, exportación e inspección y sus estados.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · Depósitos de las Series 5 y 6 y de PREP-7 (2026BA00005, 2026BA00006 y 2026EXP00001).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Dashboard`. **Verás:** «Comercio Exterior», el aviso «Abandono: … depósitos en alerta y … en abandono.» con «Ver depósitos», y las tarjetas «Depósitos Sin Nacionalizar», «Depósitos Nacionalizados», «Órdenes de Cargue Pendientes» y «Guías Pendientes». | “En este video vas a ubicar los depósitos. El tablero resume lo pendiente; cada tarjeta lleva a su lista.” |
| 2 | Abre `Comercio Exterior › Depósitos`. **Verás:** «Depósitos», el «Tipo de Depósito» en «Importación» y las columnas «Borrador», «Confirmado», «Anulado» y «Cerrado» con sus totales. | “El Kanban muestra los depósitos por estado. El número de cada columna es el total real; si hay más de diez, la columna pagina sola.” |
| 3 | Señala la tarjeta de 2026BA00001: tipo, número, estado, «SIN NACIONALIZAR», cliente, productos, existencias por unidad y «Carta Porte: DEMO-CP-0001». | “Las existencias se muestran por unidad, por ejemplo bultos y unidades por separado: nunca se suman unidades distintas.” |
| 4 | Usa «Buscar por número de depósito...», el filtro «Estado», «Desde», «Hasta» y «Limpiar». | “El buscador encuentra por número de depósito y las fechas usan el día de Colombia.” |
| 5 | Cambia «Tipo de Depósito» a «Exportación» (2026EXP00001) y luego a «Inspección» (2026INSP00001 y 2026INSP00002). Pulsa una tarjeta para abrir su detalle. | “Exportación e inspección ya no tienen menú propio: se llega por aquí. Su detalle es igual al de importación, sin levantes ni plazo aduanero.” |

**Cierre:** Ya sabes dónde está cada depósito. Ahora completamos uno que llegó en Borrador.

### 7.2 · Cómo completar un depósito en Borrador
**Duración:** 1:11 min · **Rol:** Comercio exterior

**OBJETIVO** · Completar el cliente, los terceros, la información general y los manifiestos que exige la confirmación.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00001 en Borrador con VID101 y VID105 (5.3, 5.7) y la recepción con diferencia (6.2). T3.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre 2026BA00001 desde el Kanban. **Verás:** las etiquetas «Importación» y «Camiones ingresados: 2», el aviso de Borrador y la lista «Para confirmar el depósito 2026BA00001 falta:» con «fecha del documento», «agencia de aduanas», «moneda», «valor de la mercancía», «número de manifiesto del camión VID105» y «peso del manifiesto del camión VID105». | “En este video vas a completar un depósito. Báscula lo creó con lo mínimo; el sistema dice qué falta, y cada elemento es un enlace a su sección.” |
| 2 | Pulsa «fecha del documento». En «Información General» pulsa «Editar»: «Fecha del documento», «Moneda» «USD — Dólar estadounidense» y «Valor Comercial» 12.000. Pulsa «Guardar». **Verás:** «Depósito actualizado» — «Los datos del depósito han sido actualizados». | “El valor de la mercancía y su moneda son la base del cobro del almacenamiento.” |
| 3 | En «Partes del depósito», señala «Cliente del Depósito» con «Cambiar cliente». En «Terceros Documentales», junto a «Agencia de aduanas (SIA)» («Obligatorio para confirmar»), pulsa «Asignar», elige Agencia de Aduanas Demo Nivel 1 S.A.S. y pulsa «Guardar». **Verás:** «Tercero actualizado». | “El cliente es a quien se le factura el almacenamiento y puede ser distinto del importador. En importación son obligatorios el importador y la agencia de aduanas; en exportación, el exportador. La transportadora no se asigna aquí: sale del vehículo.” |
| 4 | En «Trazabilidad de ingreso › Entradas al depósito», pulsa «Completar manifiesto» de VID105. En «Manifiesto del camión VID105» escribe MAN-DEMO-0002 y 18.000, y pulsa «Guardar». **Verás:** «Manifiesto del camión VID105 actualizado». | “Cada camión necesita el número y el peso de su manifiesto.” |
| 5 | En «Productos del Depósito» señala «Contada Bodega» (998) y la «Diferencia» de Cebolla cabezona (−2). Señala la tarjeta «Recepción de Bodega (informativa)», que muestra la última recepción. | “Aquí vemos lo que contó Bodega; nos llegó el aviso de diferencia. Si corresponde, se ajusta con el CE-7.” |
| 6 | **Verás:** el aviso verde «El depósito cumple los requisitos para confirmarse.». Señala «Unidades de carga»: «Mercancía suelta: el depósito no tiene unidades de carga.» | “Listo para confirmar. En un depósito con unidades de carga, aquí se corrige el tipo o la placa y se reparte la mercancía de un camión entre sus unidades: las unidades nacen en báscula.” |

**Cierre:** Depósito completo. Ahora lo confirmamos.

### 7.3 · Confirmar el depósito y cerrar el ingreso de camiones
**Duración:** 1:00 min · **Rol:** Comercio exterior

**OBJETIVO** · Confirmar el depósito, entender su efecto en el cobro y cerrar el ingreso de camiones.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00001 completo (7.2); T1 con acuerdo activo (2.8).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Señala «Confirmar depósito» habilitado. | “En este video vas a confirmar un depósito. Si faltara algo, el botón estaría deshabilitado y su ayuda diría Falta y la lista.” |
| 2 | Pulsa «Confirmar depósito». **Verás:** «Confirmar Depósito» — «Al confirmar, el depósito pasará a estado Confirmado y podrá ser usado en operaciones del sistema.». Pulsa «Confirmar». **Verás:** «Depósito confirmado» — «El depósito ha sido confirmado exitosamente» y «La etiqueta del depósito está lista.» | “Confirmar no espera a que Bodega termine. Atención: al confirmar se abre el primer período de almacenamiento y su factura, que cuenta desde la fecha de ingreso del depósito.” |
| 3 | Pulsa «Cerrar ingreso de camiones». **Verás:** «Después de cerrar, báscula no podrá asociar más camiones a la carta porte DEMO-CP-0001. Esta acción no se puede deshacer.». Pulsa «Cerrar ingreso». **Verás:** «Ingreso de camiones cerrado» — «Camiones ingresados: 2.» y la etiqueta «Ingreso de camiones cerrado». | “Cuando ya no llegarán más camiones con este documento, cerramos el ingreso. No tiene reapertura, y báscula verá quién lo cerró y cuándo.” |
| 4 | Pasa el cursor sobre la etiqueta. **Verás:** «Cerrado por … el …». | “Si un camión llega tarde a un depósito confirmado y aún abierto, su cantidad entra al stock, la factura se recalcula y recibes el aviso para reimprimir la etiqueta.” |
| 5 | En «Información General» pulsa «Editar». **Verás:** que en Confirmado solo se edita «Nro. Planilla de Envío». Pulsa «Cancelar». Señala «Editar fecha». | “Confirmado, el depósito solo admite la planilla de envío. La fecha de ingreso se corrige con Editar fecha y un motivo; Facturación revisa el período.” |

**Cierre:** Depósito confirmado y facturándose. Veamos la etiqueta y los documentos.

### 7.4 · Etiqueta y documentos del depósito
**Duración:** 0:50 min · **Rol:** Comercio exterior

**OBJETIVO** · Imprimir la etiqueta del depósito y descargar sus documentos.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00001 confirmado (7.3).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En la cabecera señala «Sin imprimir» y pulsa «Imprimir etiqueta». **Verás:** «Etiqueta generada» — «Se abrió en una pestaña nueva.» y el PDF con «MERCANCIA SIN NACIONALIZAR». | “En este video vas a imprimir la etiqueta. Es el rótulo que se pega a la mercancía. Se puede imprimir desde Borrador, apenas báscula crea el depósito.” |
| 2 | Señala en el PDF la tabla «Ampara», «Saldo» y «Mercancía» y el «Intermediario». | “La etiqueta ampara lo recibido, muestra el saldo y como intermediario la agencia de aduanas.” |
| 3 | Vuelve: el contador dice «Impresa 1 vez · última: …». Púlsalo. **Verás:** «Historial de la etiqueta» con «Acción», «Usuario» y «Fecha». Pulsa «Cerrar». | “Queda registrado quién la imprimió y cuándo.” |
| 4 | Abre «Documentos» y pulsa «Descargar etiqueta» y luego «PDF consolidado». **Verás:** «La etiqueta se ha descargado correctamente» y «PDF generado» — «El consolidado se ha descargado correctamente». | “El consolidado es la descripción del ingreso a bodega.” |
| 5 | Muestra una diapositiva con los textos de la etiqueta: «MERCANCIA NACIONALIZADA», «MERCANCIA PARA EXPORTACION» e «INSPECCION ADUANERA». | “Con un levante, aunque sea parcial, la etiqueta dice nacionalizada. Cuando sale mercancía con guía, reimprime la etiqueta con el saldo nuevo. Un depósito anulado no se imprime.” |

**Cierre:** Etiqueta lista. Veamos cómo corregir los productos de un depósito.

### 7.5 · Cómo corregir los productos del depósito
**Duración:** 1:04 min · **Rol:** Comercio exterior

**OBJETIVO** · Corregir cantidades y productos de un depósito en Borrador y devolver a corrección uno confirmado.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00003 en Borrador (5.8) y 2026BA00001 confirmado sin órdenes (7.3).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre 2026BA00003. En «Productos del Depósito» señala «Declarada», «Cant. depósito», «Contada Bodega», «Diferencia», «Stock Actual» y los botones «Ajustar cantidad del depósito» y «Agregar producto». | “En este video vas a corregir los productos de un depósito. En Borrador se edita todo.” |
| 2 | Pulsa el lápiz «Editar el producto y su cantidad por camión» en Llantas para camión. En «Editar producto del depósito» cambia la «Cantidad por camión» de 20 a 18. **Verás:** «Total del depósito» «20 → 18». Escribe el «Motivo de la corrección» Error de digitación en báscula: el documento ampara 18 llantas y pulsa «Guardar cambios». **Verás:** «Producto actualizado» — «La cantidad del depósito y su factura se ajustaron.» | “La cantidad se corrige por camión y el total es la suma. Cada corrección queda en el kárdex como Corrección de producto.” |
| 3 | Pulsa «Cambiar producto» en una línea y señala «Producto del catálogo» y «Motivo». Pulsa «Cancelar». | “Cambiar producto sirve cuando báscula escribió una descripción libre: se reemplaza por el producto correcto del catálogo.” |
| 4 | Pasa el cursor por la papelera de Cebolla cabezona. **Verás:** «No se puede eliminar: ya tiene movimientos de inventario». | “Un producto se elimina con motivo, salvo que ya tenga recepción, levante, reserva, movimientos u orden de cargue: entonces el botón dice por qué no.” |
| 5 | Abre 2026BA00001 (Confirmado). **Verás:** «Para editar los productos, devuelva el depósito a corrección.». Pulsa «Devolver para corrección». **Verás:** «El depósito 2026BA00001 volverá a Borrador para poder editar sus productos. Después deberá confirmarlo de nuevo. ¿Desea continuar?». Pulsa «Cancelar». | “Un depósito confirmado se devuelve a corrección para editarlo y luego se confirma de nuevo. Si tiene órdenes de cargue activas, el sistema no lo permite: primero se cancelan o se revierten.” |

**Cierre:** Productos corregidos. Para corregir solo la cantidad de un depósito confirmado existe el ajuste CE-7.

### 7.6 · Ajustar la cantidad del depósito (CE-7)
**Duración:** 0:50 min · **Rol:** Comercio exterior

**OBJETIVO** · Corregir la cantidad de un producto del depósito y entender su efecto en el kárdex y en la factura.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00001 con la factura `DEMO-FE-0001` aprobada (3.7); `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` configurado (PREP-3). Grábalo en el orden 18 del plan maestro.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En 2026BA00001, «Productos del Depósito», pulsa «Ajustar cantidad del depósito». **Verás:** el aviso «La corrección de la cantidad del depósito queda en el kárdex (movimiento de entrada o salida, origen «Ajuste CE-7») con la observación y se notifica al administrador por correo. …» | “En este video vas a ajustar la cantidad de un depósito. Es el ajuste CE-7.” |
| 2 | Elige «Producto» Llantas para camión. **Verás:** «Cant. depósito actual», «Stock actual» y «Stock resultante». Escribe «Nueva cantidad del depósito» 38 y la «Observación» Conteo confirmado con el importador: llegaron 38 llantas. | “Se escribe la cantidad total nueva, no la diferencia. El stock resultante avisa en rojo si quedaría por debajo de lo reservado.” |
| 3 | Pulsa «Guardar corrección». **Verás:** «Cantidad del depósito ajustada» — «La cantidad del depósito se corrigió y el administrador fue notificado.» | “El ajuste deja un movimiento Ajuste CE-7 en el kárdex y avisa al administrador.” |
| 4 | Muestra una diapositiva con los efectos. | “Si el depósito tiene un período abierto, su factura se recalcula: una aprobada conserva su número SIIGO y Facturación recibe el total anterior y el nuevo. La cantidad no puede quedar por debajo de lo ya nacionalizado con levantes.” |

**Cierre:** Cantidad ajustada. Pasemos al trámite de importación: los levantes.

### 7.7 · Cómo registrar levantes y nacionalizar
**Duración:** 1:13 min · **Rol:** Comercio exterior

**OBJETIVO** · Registrar el levante de la DIAN y dejar el depósito nacionalizado.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00001 confirmado y sin levantes (7.3).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En 2026BA00001, tarjeta «Levantes», pulsa «Registrar Levante». **Verás:** «Saldo Disponible» y «Saldo Peso». | “En este video vas a registrar un levante. El levante es la autorización de la DIAN para disponer de la mercancía; se consulta en MUISCA. Solo se registra en depósitos confirmados.” |
| 2 | Elige «Producto del depósito *» Cebolla cabezona y completa «Número de Levante *» LEV-DEMO-0001, «Fecha de Levante *», «Número de Aceptación *» ACE-DEMO-0001 y «Fecha de Aceptación *». | “Cada levante va por producto, con su número y su aceptación. Las fechas no pueden ser futuras.” |
| 3 | En «Cantidades a Levantar» deja apagado «Levante total del saldo disponible». Escribe el «Peso (kg) *» y ajusta la «Cantidad (Bulto) *» a 600 [verificar en pantalla el cálculo]. En «FOB del levante (USD)» escribe 7.000. | “Este levante es parcial: 600 de 1.000 bultos. El FOB se convierte con la TRM de la DIAN del día.” |
| 4 | Pulsa «Registrar Levante». **Verás:** «Confirmar Registro de Levante» con el resumen. Pulsa «Confirmar». **Verás:** «Levante LEV-DEMO-0001 registrado para «Cebolla cabezona»» con «Registrar otro producto con este levante» y «Terminar». Pulsa «Terminar». | “Si el mismo levante cubre otro producto, se registra sin volver a digitar los datos.” |
| 5 | **Verás:** el estado «Nacionalizado» y «La etiqueta del depósito está lista.». Pulsa «Imprimir etiqueta». **Verás:** «MERCANCIA NACIONALIZADA». | “Un solo levante, aunque sea parcial, deja el depósito nacionalizado y habilita órdenes de cargue hasta la cantidad nacionalizada.” |
| 6 | Señala los íconos «Editar levante» y «Retirar levante». Abre `Comercio Exterior › Levantes`. **Verás:** «Levantes» — «Levantes de todos los depósitos de importación.», sus filtros y «Exportar Excel». | “Un levante se edita o se retira con motivo, salvo que su mercancía ya haya salido. La página Levantes es de consulta. El Manifiesto DIAN del depósito se edita en el resumen, pero no es requisito para confirmar.” |

**Cierre:** Mercancía nacionalizada. Veamos el control del plazo aduanero: abandono y prórrogas.

### 7.8 · Abandono y prórrogas
**Duración:** 0:44 min · **Rol:** Comercio exterior

**OBJETIVO** · Vigilar el plazo aduanero de la mercancía sin nacionalizar y registrar una prórroga.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00005 (25 días) y 2026BA00006 (35 días), de PREP-7.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Comercio Exterior › Dashboard` pulsa «Ver depósitos» del aviso de abandono. **Verás:** «Abandono y prórrogas» — «Depósitos de importación con mercancía sin nacionalizar y su plazo aduanero: 30 días desde el ingreso, o 60 con prórroga.», con el filtro «Estado» en «En alerta». | “En este video vas a controlar el abandono. La mercancía sin nacionalizar tiene 30 días desde el ingreso, o 60 con prórroga. En alerta son los últimos 10 días.” |
| 2 | Señala 2026BA00005: «Días», «Plazo», «Faltan» en rojo y «Prórroga» «No». Cambia «Estado» a «En abandono». **Verás:** 2026BA00006 con «Vencido hace 5 días». | “En abandono es la que ya venció el plazo.” |
| 3 | Vuelve a «En alerta» y pulsa «Registrar prórroga» en 2026BA00005. **Verás:** «La prórroga amplía el plazo de abandono de 30 a 60 días. No se puede deshacer.». Escribe en «Notas» Prórroga solicitada por el importador y pulsa «Registrar prórroga». **Verás:** «Prórroga registrada: nuevo plazo de 60 días». | “La prórroga se registra una vez y no se deshace.” |
| 4 | Abre el detalle de 2026BA00005. **Verás:** la tarjeta «Plazo aduanero» con «Prórroga registrada el … por …». | “También se registra desde aquí. Cada día llega una alerta con los depósitos en alerta y en abandono.” |

**Cierre:** Plazos bajo control. Veamos las listas de empaque del proveedor.

### 7.9 · Listas de empaque
**Duración:** 0:50 min · **Rol:** Comercio exterior

**OBJETIVO** · Cargar la lista de empaque del proveedor y asociar sus artículos al camión.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · El archivo ARCH-3 `lista-empaque-demo.csv`; 2026BA00003 en Borrador (T1, VID106).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Listas de empaque` y pulsa «Cargar lista de empaque». | “En este video vas a cargar una lista de empaque: el detalle de artículos que envía el proveedor.” |
| 2 | En «Proveedor» pulsa «Nuevo proveedor», escribe Proveedor Andino Demo y pulsa «Guardar». Elige «Importador» Comercializadora Andina Demo S.A.S., selecciona el archivo con «Seleccionar CSV» y deja «Filas de encabezado» en 1. Señala la nota «Columnas en orden: codigo;NOMBRE;CANT_BULTOS;UNID_X_BULTOS;PSO_TOTAL_NETO. …». | “El archivo debe traer las columnas en ese orden.” |
| 3 | Pulsa «Simular». **Verás:** «Filas válidas 3 de 3 · Productos nuevos: …» y la tabla de filas. | “Simular revisa el archivo sin guardar nada.” |
| 4 | Pulsa «Importar». **Verás:** «Lista cargada: 3 artículos». Recorre las pestañas «Archivos» y «Artículos». | “La lista queda guardada por importador y proveedor.” |
| 5 | Abre 2026BA00003. En «Entradas al depósito» pulsa «Agregar artículos de lista de empaque» de VID106. En «Artículos de lista de empaque para el camión VID106» elige DEMO-ART-02, escribe un «Motivo» y pulsa «Asociar». **Verás:** «Se agregaron 1 productos al camión VID106». | “Los artículos se asocian a un camión de un depósito en Borrador y pasan a ser productos del depósito.” |

**Cierre:** Lista asociada. Pasemos a la salida: la orden de cargue.

### 7.10 · Cómo crear una orden de cargue
**Duración:** 1:14 min · **Rol:** Comercio exterior

**OBJETIVO** · Registrar la orden de cargue externa y preparar la salida de mercancía de uno o varios depósitos.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00001 nacionalizado (7.7) y 2026BA00002 con levante (PREP-10); VID108 registrado por Vigilancia (PREP-6); T3; K1; Q2; ARCH-4.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Órdenes de Cargue › Crear Orden`. **Verás:** «Crear Orden de Cargue» y el recuadro «Información Importante» con sus validaciones automáticas. | “En este video vas a crear una orden de cargue: la autorización interna para retirar mercancía. Reserva el stock.” |
| 2 | En «Orden de cargue externa»: «Número de la orden externa *» DEMO-OC-0001, «Emisor *» Agencia de Aduanas Demo Nivel 1 S.A.S., «Fecha de la orden *» de hoy y «Adjuntar soporte» con el PDF. | “El sistema ya no emite su propia orden: registramos la que envía la agencia de aduanas o el importador, con su soporte.” |
| 3 | En «Depósitos de la Orden», «Criterio de búsqueda» «Nro depósito», «Valor a buscar» 2026BA00001. Elige Cebolla cabezona («Nacionalizado disponible: 600»), escribe «Cantidad a cargar *» 200 («Máximo: 600 Bulto (lo nacionalizado disponible)») y pulsa «Agregar a la orden». | “En importación solo sale lo nacionalizado: un depósito sin levante aparece Sin levante y no se puede elegir.” |
| 4 | Busca 2026BA00002, elige la unidad TQD9001 en «Seleccione la unidad de carga *», escribe «Cantidad a despachar *» 5.000 y pulsa «Agregar a la orden». **Verás:** los dos ítems y, por cliente, «Cliente al Día». | “Una orden puede mezclar depósitos de varios clientes, y de una unidad de carga puede salir solo una parte. Cada cliente muestra su estado financiero: uno bloqueado impide crear la orden.” |
| 5 | En «Vehículo y Conductor» elige «Vehículo *» VID108. En «Conductor *» pulsa «Agregar Nuevo» y registra a Jaime Demo Revelo, 1000000108 [verificar en pantalla los campos]. **Verás:** «Conductor agregado». | “Si el conductor no existe, se crea aquí mismo.” |
| 6 | En «Destino y Programación»: «Ciudad de destino *» PASTO («Tránsito: 1 días»), «Fecha y Hora Programada *», «Cuadrilla que carga» Cuadrilla B y «Dirección de Destino». Pulsa «Crear Orden de Cargue». **Verás:** «Orden creada» — «Orden 2026OC00001 creada exitosamente» y el detalle. | “Los días de tránsito de la ciudad calcularán el vencimiento de la guía. Al crear la orden se reserva la mercancía. No se descarga ningún PDF.” |

**Cierre:** Orden lista. Veamos cómo modificarla, cancelarla o revertirla.

### 7.11 · Modificar, cancelar y revertir una orden de cargue
**Duración:** 0:46 min · **Rol:** Comercio exterior

**OBJETIVO** · Ajustar o cancelar una orden pendiente y conocer la reversión de una salida.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · La orden 2026OC00002 pendiente (PREP-11) y 2026OC00001 despachada con su guía (orden 12 del plan maestro).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Órdenes de Cargue › Listado`. **Verás:** «Órdenes de Cargue», los filtros «Estado» y «Criterio de búsqueda» y la columna «Orden externa». Pulsa «Ver detalle» de 2026OC00002. | “En este video vas a administrar una orden. La lista se filtra por estado o por criterios como el número externo, el documento o la placa.” |
| 2 | Pulsa «Modificar ítems». En «Modificar la orden 2026OC00002» cambia la «Cantidad» de 50 a 30, escribe el «Motivo» y pulsa «Guardar cambios». **Verás:** «Orden modificada». | “Mientras esté pendiente o en cargue, se ajustan los ítems. Bodega recibe el aviso Orden de cargue modificada.” |
| 3 | Pulsa «Cancelar Orden». **Verás:** «Se liberan las reservas de stock. Si la orden ya estaba en cargue, Bodega recibe un aviso.». Escribe el «Motivo» y pulsa «Cancelar orden». **Verás:** «Orden cancelada». | “Si la mercancía ya no sale, se cancela la orden y se liberan las reservas.” |
| 4 | Abre 2026OC00001 y pulsa «Revertir salida». **Verás:** «Revertir la salida de la orden 2026OC00001» con «La mercancía cargada vuelve a su depósito y queda por ubicar. Si la orden tiene una guía vigente, anúlela primero.» y «Motivo». Pulsa «Cancelar». | “Revertir devuelve la mercancía al depósito, por ejemplo si un camión no pudo salir. Primero se anula la guía. No lo confirmamos: esta orden ya salió.” |

**Cierre:** Órdenes bajo control. Veamos la guía de salida y su cobro.

### 7.12 · Cómo generar la guía de salida con su cobro
**Duración:** 0:57 min · **Rol:** Comercio exterior

**OBJETIVO** · Emitir la guía de salida de una orden de importación y cobrarla a cada cliente dueño.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · La orden 2026OC00001 cargada por Bodega (6.6). Precio de GUIA_SALIDA $15.000 (S2). T1 y T2 como clientes dueños.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Guías de Salida › Generar Guía`. **Verás:** «Crear Guía de Salida - Importación» y el aviso «Solo para Depósitos de Importación» — «Las guías de exportación se generan automáticamente al completar el cargue…». | “En este video vas a emitir una guía de salida. La guía acompaña la salida de la mercancía importada y se cobra.” |
| 2 | En «Orden de Cargue *» elige 2026OC00001 · Orden externa DEMO-OC-0001. **Verás:** «Orden externa», «Emisor» y «Fecha de la orden». | “La lista trae las órdenes de importación sin guía vigente.” |
| 3 | En «Datos de la Guía» elige la «Fecha y Hora de Salida *». **Verás:** «Vence el …: 1 días de tránsito a PASTO». En «Firmante *» **verás** «Conductor» y «Con varios clientes dueños la guía la firma el conductor.» | “El vencimiento sale de los días de tránsito de la ciudad. Con varios clientes dueños, firma el conductor.” |
| 4 | Pulsa «Continuar al cobro». **Verás:** «Facturación y Cobro — Guía de Salida» con el destinatario «Clientes», «Se facturará por depósito a cada cliente dueño de la mercancía, aplicando su convenio o precio general.» y la tabla «Cliente», «Depósitos», «Tarifa», «IVA» y «Total», con «Total a cobrar» $30.000. | “La guía se cobra a cada cliente dueño de la mercancía, y el total se ve antes de crearla.” |
| 5 | Elige «Modo de pago» «Pendiente por facturar» y pulsa «Crear Guía de Salida». **Verás:** «Guía de Importación creada» — «Guía 2026S00001 creada. …» y la descarga del PDF. | “Al crear, se asigna el consecutivo anual de guías y se generan las facturas.” |
| 6 | Abre el PDF. **Verás:** «Guía de Salida No. 2026S00001» y, por línea, «Entrada», «Saldo Ante.», «Cant. Sale» y «Nvo. Saldo». | “La guía congela los saldos al emitirse: de 1.000 bultos salen 200 y quedan 800. Con la guía vigente, báscula cierra el repesaje y Vigilancia registra la salida. Después, reimprime la etiqueta con el saldo nuevo.” |

**Cierre:** Guía emitida. Veamos las guías pendientes y el historial.

### 7.13 · Guías pendientes e historial de guías
**Duración:** 0:43 min · **Rol:** Comercio exterior

**OBJETIVO** · Ubicar las órdenes que esperan guía y administrar las guías emitidas.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · La guía 2026S00001 (7.12).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Guías de Salida › Pendientes`. **Verás:** «Órdenes Pendientes de Guía» — «Órdenes de importación activas que requieren guía de salida» y el botón «Generar Guía» por fila (o «No hay órdenes pendientes de guía»). | “En este video vas a revisar las guías. Pendientes muestra las órdenes de importación que aún necesitan guía, también las que ya se cargaron.” |
| 2 | Abre `Comercio Exterior › Guías de Salida › Historial`. **Verás:** «Historial de Guías de Salida», el buscador, el filtro «Tipo» y las columnas «N° Guía», «Cliente», «Placa», «Producto», «Cantidad», «Fecha» y «Modo Pago». | “El historial reúne las guías de importación y de exportación.” |
| 3 | En 2026S00001 pulsa «Descargar PDF de la guía» y luego «Descargar PDF por depósito (ZIP)». **Verás:** «PDF generado» y «ZIP generado». | “El ZIP trae una guía por depósito, y cada impresión queda registrada.” |
| 4 | Señala «Modo Pago» «Pendiente por facturar». «Cambiar modo de pago» aparece mientras Facturación no haya aprobado, numerado ni verificado el pago de ninguna de sus facturas; las que la guía generó al crearse (en borrador) no cuentan. | “Mientras la guía no esté facturada, se puede cambiar su modo de pago.” |
| 5 | Pulsa «Anular guía». **Verás:** «Se anula la guía y su cobro sin aprobar. Las facturas aprobadas o pagadas quedan para revisión de Facturación. …» y «Motivo». Pulsa «Cancelar». | “Anular exige motivo. No lo confirmamos: esta guía es válida.” |

**Cierre:** Guías al día. Veamos cómo anular un depósito.

### 7.14 · Cómo anular un depósito
**Duración:** 0:47 min · **Rol:** Comercio exterior

**OBJETIVO** · Anular un depósito con motivo y entender sus efectos.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · 2026BA00004 en Borrador, con el ciclo de VID106 terminado (PREP-10).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre 2026BA00004 y pulsa «Anular depósito». **Verás:** «Anular el depósito 2026BA00004» con el texto «Se anulan el depósito, sus ítems en órdenes pendientes …». | “En este video vas a anular un depósito, por ejemplo uno creado por error.” |
| 2 | Escribe en «Motivo» Documento registrado por error en báscula; la mercancía no corresponde y pulsa «Anular depósito». **Verás:** «Depósito anulado» con sus listas de resultados. Pulsa «Cerrar». | “El motivo es obligatorio, de 10 a 500 caracteres. El resultado dice qué órdenes, períodos y facturas se afectaron.” |
| 3 | **Verás:** el Kanban con el depósito en «Anulado». Ábrelo: el aviso «Depósito anulado el … Motivo: …» y «Imprimir etiqueta» deshabilitado («El depósito está anulado»). | “Queda en solo lectura: sin edición, levantes ni etiqueta.” |
| 4 | Muestra una diapositiva con los bloqueos y avisos. | “No se anula un depósito con salidas ejecutadas, ni con un camión todavía en báscula. Bodega y Facturación reciben su aviso, y las facturas aprobadas quedan para revisión de Facturación.” |

**Cierre:** Cerramos la serie con los reportes de Comercio Exterior.

### 7.15 · Reportes de Comercio Exterior
**Duración:** 0:54 min · **Rol:** Comercio exterior

**OBJETIVO** · Conocer los nueve reportes de Comercio Exterior y exportarlos.
**GRABA CON** · `video.comext` (C5).
**REQUISITOS** · Datos del recorrido: levantes con FOB, salidas y la ciudad BOGOTA como destino de abandono (K3).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Comercio Exterior › Reportes › Movimientos por Depósito`. **Verás:** «Informe de Movimientos por Depósito». Escribe el «Número de depósito *» 2026BA00001 y consulta. **Verás:** «Datos del depósito» y «Movimientos por producto». Descarga el PDF. | “En este video vas a recorrer los reportes. Movimientos por depósito muestra ingresos, nacionalizado, despachado y existencias de cada producto.” |
| 2 | Abre `Reportes › Mercancías ingresadas (diario)` y `Reportes › Salida de mercancía (diario)`. | “Los diarios listan los depósitos que ingresaron y las salidas de un rango; las salidas sin guía aparecen como Sin guía.” |
| 3 | Abre `Reportes › Mercancía en abandono` y `Reportes › Salidas a destino de abandono`. | “Los de abandono muestran la mercancía con plazo vencido y las salidas a ciudades marcadas como destino de abandono.” |
| 4 | Abre `Reportes › Informe de póliza`. **Verás:** «Valor FOB de los levantes (USD), por mes, para UAP y no UAP.» | “El informe de póliza suma el FOB de los levantes, separando a los usuarios aduaneros permanentes.” |
| 5 | Señala `Reportes › Inventario general`, `Reportes › Ingresos por producto` y `Reportes › Ingresos por agencia de aduanas`, con «Consultar» y «Exportar Excel». | “Y los de inventario, ingresos por producto de un importador e ingresos de una agencia. Todos se exportan a Excel.” |

**Cierre:** Con esto cerramos Comercio Exterior y el recorrido completo de la mercancía, de la portería a la guía de salida.

## Serie 3 · Facturación

13 videos · Rol Facturación. El sistema genera las facturas solo; no se crean a mano. Facturación revisa, asigna el número SIIGO, aprueba, registra los pagos y vigila la cartera. **El WMS no emite la factura electrónica:** la factura legal se hace en SIIGO y su número se copia aquí. Grábala casi al final: necesita las operaciones y los acuerdos. Graba con `video.facturacion` (dataset C6).

### 3.1 · Configuración de facturación del cliente
**Duración:** 1:04 min · **Rol:** Facturación

**OBJETIVO** · Definir el ciclo, el plazo de pago, la preferencia y el límite de crédito de un cliente.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · T1 (1.3). Grábalo antes del recorrido (orden 3 del plan maestro).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Facturación › Configuraciones`. **Verás:** «Configuraciones de Facturación» con «Cliente», «Ciclo», «Días de Pago», «Preferencia», «Límite Crédito» y «Activo». Pulsa «Nueva Configuración». | “En este video vas a configurar cómo se le factura a un cliente. Sin configuración, el almacenamiento usa el ciclo mensual.” |
| 2 | Lee la ayuda «¿Qué significa cada opción?». | “La ayuda explica cada campo antes de llenarlo.” |
| 3 | En «Cliente *» elige Comercializadora Andina Demo S.A.S. Abre «Ciclo de facturación *» y señala las ocho opciones; elige «Mensual (mes calendario)». | “El ciclo es la duración de cada período de almacenamiento, desde semanal hasta anual. Cada período vence tres días después de su fin.” |
| 4 | Escribe «Días de pago *» 30. En «Preferencia de facturación *» señala «Consolidada» y elige «Por servicio». Escribe «Límite de crédito» 50.000.000. | “Los días de pago fijan el vencimiento al aprobar. Consolidada agrupa en una factura por período los depósitos y las guías a crédito; la báscula y el montacargas siempre van en facturas individuales. Por servicio hace una factura por cada tipo de servicio.” |
| 5 | Pulsa «Guardar». **Verás:** «Configuración guardada» — «La configuración de facturación se ha actualizado». | “El límite de crédito decide el bloqueo por mora: si la deuda vencida lo supera, el cliente queda bloqueado. Vacío significa sin límite, y un cliente sin límite nunca se bloquea solo.” |

**Cierre:** El cliente ya tiene sus condiciones. Recorramos el módulo desde su tablero.

### 3.2 · El tablero y el recorrido del módulo
**Duración:** 0:47 min · **Rol:** Facturación

**OBJETIVO** · Ubicarse en el módulo y leer los indicadores de cartera.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · Facturas del recorrido (órdenes 5 a 12 del plan maestro).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Inicia sesión con `video.facturacion`. **Verás:** `Facturación › Dashboard` con «Facturación» — «Panel de control del módulo de facturación» y las tarjetas «Facturado este mes», «Cartera pendiente», «Facturas vencidas», «Borradores» y «Total facturas». | “En este video vas a recorrer Facturación. El tablero resume el mes: lo facturado, lo pendiente de cobro, las vencidas y los borradores por revisar. Cada tarjeta abre su lista.” |
| 2 | Señala «Acciones Rápidas», «Últimas Facturas» y «Clientes con Mora». | “Abajo, las últimas facturas y los clientes con facturas vencidas.” |
| 3 | Recorre el menú: `Facturas`, `Depósitos Pendientes`, `Pagos`, `Configuraciones`, `Clientes`, `Facturación anual`, `Facturación por CPI`, `Inventario general` y `Movimientos por depósito`. | “Facturas es el corazón del módulo. Clientes lleva a los terceros y a sus acuerdos. También hay reportes y consultas de inventario.” |
| 4 | Abre la campana y pulsa «Ver todas las notificaciones». Señala avisos como «Almacenamiento facturado con valor mínimo». | “Facturación recibe avisos del sistema: facturas al valor mínimo, TRM pendiente, facturas recalculadas o anuladas.” |

**Cierre:** Ya ubicados, veamos cómo calcula el sistema cada factura.

### 3.3 · Cómo calcula el sistema una factura
**Duración:** 1:05 min · **Rol:** Facturación

**OBJETIVO** · Leer de dónde sale cada valor de una factura: la tarifa, la base, el IVA y el total.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · La factura de almacenamiento de 2026BA00001 (7.3) y la de 2026EXP00001 (PREP-7).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Facturación › Facturas`, pestaña «Almacenamiento», pulsa «Ver detalle» de la factura de 2026BA00001. **Verás:** «Información del depósito» con «Valor mercancía (USD)», «TRM aplicada» con la etiqueta «DIAN» y «Valor en COP». | “En este video vas a entender el cálculo. El almacenamiento parte del valor de la mercancía convertido a pesos con la TRM.” |
| 2 | En «Items», pasa el cursor sobre «Acuerdo (nivel 1)» en «Método cálculo». **Verás:** «Tarifa resuelta por el acuerdo comercial vigente del cliente». Señala las dos líneas: cebolla y llantas. | “Cada línea dice de dónde salió su tarifa: acuerdo, tarifa base, precio base o valor mínimo. Aquí hay dos cargos, porque el acuerdo tiene una condición especial para llantas.” |
| 3 | Muestra una diapositiva con la jerarquía: «Acuerdo (nivel 1) › Tarifa base (nivel 2) › Precio base (nivel 3) › Valor mínimo». | “El sistema busca la tarifa en ese orden. El valor mínimo solo existe en almacenamiento; si otro servicio no tiene tarifa, no se puede cobrar.” |
| 4 | Abre la factura de 2026EXP00001. **Verás:** la etiqueta «Valor mínimo» y el aviso «Sin acuerdo ni precio establecido». | “Cuando falta la tarifa, el almacenamiento se cobra al valor mínimo de la modalidad, con advertencia. Nunca se queda sin factura.” |
| 5 | Muestra el cálculo de la báscula: base $16.806,72 + IVA 19 % $3.193,28 = $20.000. | “Con la tarifa resuelta, el sistema calcula la cantidad, la base y le suma el IVA. Si la tarifa se pactó con IVA incluido, el sistema lo separa para que el total quede exacto.” |

**Cierre:** Con esta base, veamos las facturas de los cobros del día: báscula, montacargas y guía.

### 3.4 · Facturas de báscula, montacargas y guía
**Duración:** 1:07 min · **Rol:** Facturación

**OBJETIVO** · Gestionar las facturas de contado y las de «por facturar» que generan la báscula, el montacargas y la guía.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · Facturas de VID102 (contado), VID101 («Por facturar»), VID106 (depósito adicional en cero), el montacargas de 6.5 y la guía 2026S00001.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Facturación › Facturas`, pestaña «Báscula». **Verás:** las columnas «N° Factura» («Pendiente de número» o «—»), «Identificación», «Destinatario», «Estado», «Total», «Pendiente» y «Vencimiento». | “En este video vas a gestionar los cobros del día. Cada servicio tiene su pestaña.” |
| 2 | Abre la factura de VID102 («Pagada»). En «Pagos» **verás** el pago en «Recibido». Pulsa «Verificar». **Verás:** «Pago verificado» — «El pago ha sido verificado exitosamente». | “El cobro de contado nace pagado, con el pago recibido en báscula. Facturación lo verifica cuando confirma el dinero.” |
| 3 | Pulsa «Acciones». **Verás:** «Asignar N.º SIIGO» con la ayuda «Factura de contado: asigne el N.º SIIGO una sola vez; después queda fijo.». Escribe DEMO-FE-0002 y pulsa «Guardar número». **Verás:** «Número asignado» — «Se registró el número de factura (SIIGO).» | “A la factura de contado se le asigna el número SIIGO una sola vez. No se aprueba ni se envía: ya está pagada.” |
| 4 | Abre la factura de VID101. **Verás:** «Borrador», «Pendiente de número» y el vencimiento en «—». | “El cobro por facturar nace en Borrador: se le asigna el número, se aprueba y se cobra, como en el video 3.7.” |
| 5 | Abre la factura del depósito adicional de VID106. **Verás:** la línea «Servicio de Báscula — Depósito adicional» y «N° Factura» «—»; en «Acciones», «Factura en cero». | “La factura en cero no lleva número fiscal: no se le asigna número SIIGO.” |
| 6 | Abre las pestañas «Montacargas» y «Guía de salida». En el montacargas **verás** la línea «Servicio de montacargas — Tractomula» con «Impuesto %» 19 y «Método cálculo» «—». | “El IVA del montacargas aparece solo si Bodega lo agregó. Báscula y montacargas siempre son facturas individuales; las guías a crédito se pueden consolidar.” |

**Cierre:** Cobros del día al día. Vamos con la más elaborada: el almacenamiento.

### 3.5 · La factura de almacenamiento y los depósitos pendientes
**Duración:** 0:55 min · **Rol:** Facturación

**OBJETIVO** · Revisar los depósitos con período abierto, sus facturas y las advertencias de valor mínimo.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · 2026BA00001 confirmado (7.3) y 2026EXP00001 con su factura al mínimo (PREP-7).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Facturación › Depósitos Pendientes`. **Verás:** «Depósitos Pendientes de Facturación» — «Listado de depósitos activos con período de almacenamiento abierto». | “En este video vas a revisar el almacenamiento. Estos depósitos ya tienen factura: aquí se ven los que tienen un período abierto.” |
| 2 | Señala los filtros «Cliente», «Nro de Depósito» y «Fecha de Ingreso», y las columnas «Días», «Valor mercancía» y «Por refacturar». | “Días cuenta desde el inicio del período abierto y cambia de color al pasar los 30, 60 y 90.” |
| 3 | Expande 2026BA00001. **Verás:** «Historial de facturas» con «Período», «No. Factura», «Estado» y los botones «Acciones» y «Ver detalle». | “Cada período tiene su factura. El primero empieza en la fecha de ingreso del depósito; un proceso renueva el período mientras quede mercancía.” |
| 4 | Pulsa el ojo «Ver resumen». **Verás:** «Resumen del depósito 2026BA00001» con «Detalle por producto», «Levantes» y «Períodos de almacenamiento». Pulsa «Cerrar». | “El resumen muestra lo recibido, lo nacionalizado, lo despachado y el saldo.” |
| 5 | Abre la factura de 2026EXP00001. **Verás:** el aviso «Sin acuerdo ni precio establecido» y, en «Detalle de factura», «ADVERTENCIA: No existe un precio configurado ni acuerdo vigente…». | “Esta factura salió al valor mínimo porque el cliente no tiene tarifa para exportación. Antes de asignar el número, valida el precio y corrige la línea si hace falta: es el siguiente video.” |

**Cierre:** Ya sabemos leer el almacenamiento. Veamos cómo corregir el valor de una línea.

### 3.6 · Cómo sobrescribir el total de una línea
**Duración:** 0:40 min · **Rol:** Facturación

**OBJETIVO** · Corregir el total de una línea de una factura en Borrador, con IVA incluido y justificación.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · La factura de 2026EXP00001 en Borrador (PREP-7).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En la factura de 2026EXP00001, columna «Acciones» de «Items», pulsa el lápiz «Sobrescribir monto». **Verás:** «Sobrescribir total de la línea» con «Total actual de la línea (IVA incluido): $ 50.000». | “En este video vas a corregir el valor de una línea. Se escribe el total de la línea con IVA incluido.” |
| 2 | Escribe «Nuevo total de la línea (IVA incluido) *» 178.500. **Verás:** «Base $ 150.000 + IVA 19 %: $ 28.500 = Total $ 178.500». | “El sistema separa la base y el IVA en vivo, para que no haya dudas sobre el total.” |
| 3 | Escribe la «Justificación *» Tarifa pactada por correo con el cliente: $150.000 más IVA por período, y pulsa «Guardar sobrescritura». | “La justificación es obligatoria y queda registrada.” |
| 4 | **Verás:** la línea con la etiqueta «Sobrescrito»; pasa el cursor y verás «Total original (IVA incluido): …» y «Motivo: …». | “Una línea se sobrescribe una sola vez y solo en Borrador. Si después la factura se recalcula, el valor sobrescrito se descarta y la notificación lo informa.” |

**Cierre:** Línea corregida. Llevemos ahora una factura de Borrador a enviada.

### 3.7 · Ciclo de vida de la factura: número SIIGO, aprobar y enviar
**Duración:** 0:50 min · **Rol:** Facturación

**OBJETIVO** · Asignar el número SIIGO, aprobar y enviar una factura.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · La factura de almacenamiento de 2026BA00001 en Borrador (7.3) y `DEMO-FE-0002` ya usado (3.4).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre la factura de 2026BA00001 y pulsa «Acciones». **Verás:** «Acciones de la factura» con «Asignar N.º SIIGO», «Estado y cobro» («Aprobar», «Enviar», «Registrar pago»), «Editar detalle», «Notas» y «Anular factura»; las acciones que no aplican dicen por qué. | “En este video vas a llevar una factura de Borrador a enviada. Todo se hace en este diálogo. Aprobar dice: Asigne el N.º SIIGO antes de aprobar.” |
| 2 | Escribe DEMO-FE-0002 en «Número emitido en SIIGO» y pulsa «Guardar número». **Verás:** bajo el campo, «Ya existe una factura con el número 'DEMO-FE-0002'.». Cámbialo por DEMO-FE-0001 y guarda. **Verás:** «Número asignado». | “El número viene de SIIGO, donde se emite la factura legal. Es único: no se repite.” |
| 3 | Pulsa «Aprobar». **Verás:** «Aprobar factura» — «¿Aprobar la factura DEMO-FE-0001? Después no podrá cambiar el número.». Pulsa «Aprobar». **Verás:** «Factura aprobada» y la «Fecha Vencimiento» con 30 días. | “Al aprobar, el número queda fijo y se fija el vencimiento: hoy más los días de pago del cliente.” |
| 4 | Pulsa «Acciones» › «Enviar» y confirma con «Enviar». **Verás:** «Factura enviada» — «La factura ha sido marcada como enviada». | “Enviar marca la factura como entregada al cliente; el sistema no manda correo.” |
| 5 | Pulsa «PDF». **Verás:** «PDF descargado». Señala el «Historial» con «Creada», «Aprobada» y «Enviada». | “El detalle solo se edita en Borrador; las notas, en cualquier estado salvo anulada.” |

**Cierre:** La factura está en firme y enviada. Veamos los pagos.

### 3.8 · Cómo registrar y verificar pagos
**Duración:** 0:58 min · **Rol:** Facturación

**OBJETIVO** · Registrar un pago con su comprobante y entender la verificación y el rechazo.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · La factura `DEMO-FE-0001` enviada (3.7). El comprobante ARCH-2.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Facturación › Pagos`. **Verás:** «Historial de Pagos» — «Registro y verificación de pagos». Pulsa «Registrar Pago» y en «Factura *» busca DEMO-FE-0001. | “En este video vas a registrar un pago. Solo aparecen las facturas emitidas con saldo: aprobadas, enviadas, vencidas o con pago parcial.” |
| 2 | En «Registrar Pago» **verás** «Saldo pendiente». Escribe «Monto *» 50.000, elige «Método de pago *» «Transferencia», deja la «Fecha de pago» y escribe «N° Referencia / Comprobante» DEMO-PAGO-0001. | “El monto no puede superar el saldo.” |
| 3 | En «Adjuntar comprobante» pulsa «Seleccionar archivo» y elige el PDF. **Verás:** la ayuda «JPG, PNG, WEBP o PDF del soporte de pago (máx. 5 MB)». | “El comprobante es opcional; si lo adjuntas, debe ser imagen o PDF de hasta 5 MB.” |
| 4 | Pulsa «Registrar Pago». **Verás:** «Pago registrado» — «El pago se ha registrado exitosamente» y la factura en «Pago Parcial». | “El pago que registra Facturación nace verificado. Con saldo, la factura queda en pago parcial; al completarse, pasa a pagada.” |
| 5 | En la lista, pulsa «Ver comprobante». Señala los íconos «Verificar» y «Rechazar» en un pago «Recibido» de contado. | “Verificar o rechazar aplica a los pagos recibidos en báscula, montacargas o guía. Rechazar pide confirmación y recalcula el saldo; si era el único pago, la factura vuelve a Borrador.” |

**Cierre:** Pagos registrados. Veamos qué hacer cuando falta la TRM.

### 3.9 · TRM pendiente y TRM manual
**Duración:** 1:04 min · **Rol:** Facturación

**OBJETIVO** · Registrar la TRM a mano cuando la DIAN no respondió, para poder numerar y aprobar la factura.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · 2026BA00007 (USD) con TRM pendiente y su factura en Borrador (PREP-9).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre la campana y pulsa «Ver todas las notificaciones». **Verás:** «Almacenamiento con TRM pendiente» — «El depósito 2026BA00007 quedó con TRM pendiente …». | “En este video vas a registrar una TRM. Cuando la mercancía está en dólares, el sistema consulta la TRM a la DIAN al crear la factura del período. Si la DIAN no responde, el depósito queda con TRM pendiente.” |
| 2 | En `Facturación › Depósitos Pendientes` señala la etiqueta «TRM pendiente» de 2026BA00007 y abre su factura. **Verás:** la línea «Valor mínimo», la leyenda «TRM PENDIENTE: …» en el detalle y, en el depósito, «TRM pendiente» con «Registrar TRM». | “La factura se genera igual, con el valor mínimo, mientras se registra la TRM.” |
| 3 | Pulsa «Acciones». **Verás:** «La factura tiene TRM pendiente en el depósito 2026BA00007. Regístrela antes de asignar el número o aprobar.» y «Aprobar» con «Registre primero la TRM del depósito 2026BA00007.» | “Sin TRM no se asigna número ni se aprueba.” |
| 4 | Pulsa «Registrar TRM». En «Registrar TRM manual» **verás** «TRM del … (fecha de ingreso) para …». Escribe «TRM» 4.000,00 y el «Motivo» La DIAN no respondió; TRM tomada del certificado oficial del día. Pulsa «Registrar TRM». **Verás:** «TRM registrada» — «La factura se recalculó con la TRM manual.» | “La TRM es la de la fecha de ingreso del depósito. El motivo queda en la auditoría.” |
| 5 | **Verás:** en el depósito, la TRM con la etiqueta «Manual» y su fecha, y la línea recalculada. | “La DIAN nunca reemplaza una TRM manual, y una TRM de la DIAN no se cambia a mano.” |

**Cierre:** TRM registrada y factura recalculada. Veamos cómo anular y refacturar.

### 3.10 · Cómo anular y refacturar una factura de almacenamiento
**Duración:** 0:52 min · **Rol:** Facturación

**OBJETIVO** · Anular una factura de almacenamiento con motivo y generar su reemplazo.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · La factura de 2026EXP00001 en Borrador y sin pagos (3.6). `DEMO-FE-0001` con un pago (3.8).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre la factura de 2026EXP00001 y pulsa «Acciones». En «Anular factura» escribe el motivo Precio corregido con el cliente; se emite de nuevo. **Verás:** el contador «… / 500 (mínimo 10)». Pulsa «Anular factura» y confirma con «Anular». **Verás:** «Factura anulada» — «La factura ha sido anulada. Sus períodos quedaron por refacturar.» | “En este video vas a anular y refacturar. Anular exige un motivo de al menos 10 caracteres y no se deshace.” |
| 2 | En `Facturación › Depósitos Pendientes` señala «Por refacturar» en rojo para 2026EXP00001. | “Los períodos de la factura anulada quedan por refacturar, y Facturación recibe el aviso.” |
| 3 | Vuelve a la factura anulada, pulsa «Acciones» y, en «Refacturar» («Genera una factura nueva en Borrador, sin número SIIGO, con los mismos períodos de almacenamiento.»), pulsa «Refacturar» y confirma. **Verás:** «Factura nueva creada en Borrador» y la factura nueva con «Refacturación de la factura …». | “La factura nueva nace en Borrador, recalculada y sin número. La anulada muestra Refacturada como.” |
| 4 | Abre DEMO-FE-0001 y pulsa «Acciones». **Verás:** «Anular factura» deshabilitado con «Tiene pagos recibidos o verificados: gestione la devolución o el traslado del dinero antes de anular.» | “Una factura con dinero no se anula: primero se gestiona la devolución o el traslado del pago.” |

**Cierre:** Anulación con trazabilidad. Veamos qué pasa cuando una factura ya emitida cambia.

### 3.11 · Factura recalculada después de emitida
**Duración:** 0:58 min · **Rol:** Facturación

**OBJETIVO** · Entender el aviso de una factura recalculada y qué cambia en ella.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · `DEMO-FE-0001` aprobada (3.7) y el ajuste CE-7 de 7.6 hecho justo antes.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre la campana y pulsa «Ver todas las notificaciones». **Verás:** «Factura de almacenamiento actualizada» — «La factura DEMO-FE-0001 del depósito 2026BA00001 se actualizó por ajuste CE-7 de Llantas para camión. Total anterior …, total nuevo ….» | “En este video vas a ver una factura recalculada. Comercio Exterior ajustó la cantidad del depósito y la factura del período se actualizó sola.” |
| 2 | Abre DEMO-FE-0001. **Verás:** el mismo número, el estado y el total nuevo. | “La factura conserva su número SIIGO y su aprobación; el estado sigue al saldo. Si ya tenía pagos y queda saldo a favor del cliente, el aviso lo dice.” |
| 3 | Muestra una diapositiva con las causas. | “Se recalcula por un camión tardío, una TRM manual, un ajuste CE-7, la corrección del manifiesto o de la fecha de ingreso, la edición de productos, la anulación de un pesaje, la reversión de una salida o una refacturación.” |
| 4 | Muestra en la diapositiva los tres casos según el estado. | “En Borrador se recalcula sin más. Aprobada, enviada o pagada se actualiza la misma factura y se avisa. Anulada no se toca: llega el aviso Cambio de depósito sin facturar.” |

**Cierre:** Las facturas siguen al depósito. Veamos la cartera y el bloqueo por mora.

### 3.12 · Cartera, mora y bloqueo del cliente
**Duración:** 0:57 min · **Rol:** Facturación

**OBJETIVO** · Identificar a los clientes en mora, entender el bloqueo y levantarlo.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · T6 bloqueado con la factura `DEMO-FE-0099` vencida (PREP-8).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En `Facturación › Dashboard` señala «Facturas vencidas» y, en «Clientes con Mora», Cliente Moroso Demo S.A.S. con «1 factura(s) vencida(s)». | “En este video vas a manejar la mora. Cada día un proceso marca como vencidas las facturas que pasaron su vencimiento.” |
| 2 | Abre `Facturación › Clientes`, filtra «Estado Financiero» por «Bloqueado» y abre el cliente. **Verás:** «Estado Financiero» «Bloqueado» y «Monto Vencido». | “Si la deuda vencida supera el límite de crédito, el cliente queda Bloqueado; si no, Vencido. Sin límite, nunca se bloquea solo.” |
| 3 | Muestra una diapositiva con lo que no puede hacer un cliente bloqueado. | “Un cliente bloqueado no puede pagar báscula a su nombre, cerrar un uso de montacargas, recibir sin báscula, generar órdenes de cargue ni emitir guías.” |
| 4 | En `Facturación › Pagos` registra el pago completo de DEMO-FE-0099 (20.000, «Transferencia», DEMO-PAGO-0002). Vuelve a la ficha del cliente. **Verás:** «Estado Financiero» «Activo». | “Al pagar, el estado se recalcula al instante y el cliente queda desbloqueado. También se desbloquea si se le quita el límite de crédito en Configuraciones.” |

**Cierre:** Cartera bajo control. Cerramos con los reportes de Facturación.

### 3.13 · Reportes de Facturación: anual y por CPI
**Duración:** 0:46 min · **Rol:** Facturación

**OBJETIVO** · Consultar la facturación del año y la facturación completa de un depósito.
**GRABA CON** · `video.facturacion` (C6).
**REQUISITOS** · Facturas con número SIIGO en el año; 2026EXP00001 con una factura anulada y otra refacturada (3.10).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre `Facturación › Facturación anual`. **Verás:** «Facturación anual» — «Facturas con número SIIGO y no anuladas, por fecha de emisión.». Escribe «Año» 2026, elige «Servicio» «Almacenamiento» y pulsa «Consultar». | “En este video vas a consultar los reportes. El anual suma por mes las facturas con número SIIGO y no anuladas; las facturas en cero no salen.” |
| 2 | Expande un mes. **Verás:** los días con «Facturas» y «Total», y el pie «Totales». Pulsa «Exportar Excel». | “Cada mes se abre por días.” |
| 3 | Abre `Facturación › Facturación por CPI`. **Verás:** «Facturación por CPI» — «Facturación de un depósito, por su número (CPI).». Escribe 2026EXP00001 en «Depósito *» y pulsa «Consultar». | “El reporte por CPI muestra toda la facturación de un depósito.” |
| 4 | **Verás:** el encabezado con «Depósito:», «Carta porte:», «Fecha de ingreso:» y «TRM de ingreso:», y las secciones «Productos», «Salidas» y «Facturas». En «Facturas», la anulada con «Anulada» y «Refacturada como», y «Total facturado». Pulsa «Exportar Excel». | “Las dos facturas aparecen, la anulada y la nueva, pero el total facturado no cuenta la anulada.” |

**Cierre:** Con esto cerramos Facturación. Sigue la Serie 4: el recorrido de la mercancía empieza en la portería.

## Serie 0 · Introducción

5 videos · Todos los roles. Se graba al final, cuando ya conoces todo el flujo, pero se publica primero en el centro de ayuda: es la puerta de entrada del usuario nuevo.

### 0.1 · Visión general del sistema
**Duración:** 1:16 min · **Rol:** Todos

**OBJETIVO** · Dar el mapa del sistema: para qué sirve, cómo fluye la operación y qué hace cada rol.
**GRABA CON** · Diapositivas y `video.admin` (C1), para mostrar el menú completo.
**REQUISITOS** · Diapositiva del recorrido de la mercancía. Datos del recorrido en el ambiente de grabación.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Muestra una diapositiva de bienvenida. | “Bienvenido al sistema WMS de Bodegas Asociadas. La bodega está en Ipiales, junto al paso de Rumichaca, y es un depósito público aduanero: la mercancía espera aquí su nacionalización, su exportación o su inspección.” |
| 2 | Muestra el recorrido: «Vigilancia → Báscula → Bodega → Comercio Exterior → Facturación». | “Toda la operación sigue a la mercancía: entra por Vigilancia, se registra y se pesa en Báscula, se recibe en Bodega, Comercio Exterior gestiona el depósito y su salida, y Facturación cobra.” |
| 3 | Muestra los servicios que se cobran: báscula, montacargas, guía de salida y almacenamiento. | “La bodega cobra cuatro servicios. Báscula, montacargas y guía se cobran de contado o quedan por facturar; el almacenamiento se cobra por períodos. El WMS no emite la factura electrónica: la factura legal se hace en SIIGO y su número se copia aquí.” |
| 4 | Inicia sesión con `video.admin` y recorre el menú: «Dashboards», «Administración», «Vigilancia», «Báscula», «Bodega», «Comercio Exterior» y «Facturación». | “Hay seis roles: Administrador, Facturación, Comercio exterior, Operario vigilancia, Operario báscula y Operario bodega. Cada usuario ve solo el menú de sus roles y entra directo a su pantalla de inicio.” |
| 5 | Muestra la lista de series del centro de ayuda. | “En estos videos aprenderás paso a paso a operar tu módulo. Empieza por la serie de tu rol.” |

**Cierre:** Ese es el panorama. Empecemos por lo básico: cómo entrar al sistema.

### 0.2 · Iniciar sesión y cambiar la contraseña temporal
**Duración:** 1:03 min · **Rol:** Todos

**OBJETIVO** · Entrar al sistema, cambiar la contraseña temporal y llegar a la pantalla de inicio del rol.
**GRABA CON** · `video.nuevo` (C7), con su contraseña temporal pendiente de cambio (1.2).
**REQUISITOS** · C7 sin ingresos desde el video 1.2.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Abre el sistema. **Verás:** «Iniciar Sesión» — «Completar el formulario para ingresar al sistema», con «Ingrese su usuario», «Ingrese contraseña», «Iniciar sesión» y «Recuperar contraseña». | “En este video vas a entrar al sistema por primera vez.” |
| 2 | Escribe el usuario y una contraseña equivocada; pulsa «Iniciar sesión». **Verás:** «No se pudo completar la acción» — «Credenciales inválidas». | “Si el usuario o la clave no coinciden, el sistema solo dice credenciales inválidas, sin revelar cuál de los dos falló.” |
| 3 | Escribe la contraseña temporal y pulsa «Iniciar sesión». **Verás:** «Cambiar Contraseña» — «Es necesario cambiar su contraseña antes de continuar». | “En el primer ingreso, o después de que el administrador restablece la clave, el sistema pide cambiarla.” |
| 4 | Escribe «Nueva contraseña» y «Confirmar nueva contraseña». **Verás:** el medidor «Débil / Medio / Fuerte». | “Al menos 8 caracteres, con mayúscula, minúscula, número y un carácter especial, como el signo de admiración o la almohadilla; sin espacios.” |
| 5 | Pulsa «Cambiar contraseña». **Verás:** «Contraseña actualizada» — «Su contraseña ha sido cambiada exitosamente.» y, en segundos, la pantalla de inicio del rol (`Facturación › Dashboard`). | “Cada rol entra a su pantalla: Vigilancia al ingreso, Báscula al proceso de pesaje, Bodega y Facturación a su tablero, y el Administrador y Comercio Exterior a la trazabilidad.” |
| 6 | Señala que el menú solo muestra «Notificaciones», «Báscula» y «Facturación». | “El menú muestra solo lo de tus roles. Si abres una página sin permiso, verás Acceso Denegado con el botón Ir a mi inicio. Una cuenta inactiva no puede entrar.” |

**Cierre:** Ya estás dentro. ¿Y si olvidas la contraseña? Lo vemos en el siguiente video.

### 0.3 · Recuperar o restablecer la contraseña
**Duración:** 0:45 min · **Rol:** Administrador y todos

**OBJETIVO** · Recuperar la contraseña del administrador por correo y saber qué hacen los demás usuarios.
**GRABA CON** · `video.admin` (C1), con su correo en la bandeja local.
**REQUISITOS** · Buzón local de pruebas configurado (ambiente, sección 1 del dataset). C1 activo y con correo.

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | En «Iniciar Sesión» pulsa «Recuperar contraseña». **Verás:** «Recuperar Contraseña» — «Si es administrador / Recibirá un correo con las instrucciones / para restablecer su contraseña.» | “En este video vas a recuperar una contraseña. La recuperación por correo es solo para el administrador.” |
| 2 | Escribe el usuario `video.admin` en «Ingrese su nombre de usuario» y pulsa «Enviar solicitud». **Verás:** «Solicitud enviada» — «Si el usuario existe y es administrador, recibirá un correo con las instrucciones para restablecer su contraseña.» | “El mensaje es el mismo para cualquier usuario, exista o no, para no revelar qué cuentas existen.” |
| 3 | Abre el buzón. **Verás:** el correo «Recuperación de Contraseña - WMS» con el botón «Restablecer Contraseña» y «Este enlace expirará en 30 minutos.». Pulsa el botón. | “El enlace vale 30 minutos.” |
| 4 | En «Restablecer Contraseña» escribe «Nueva contraseña» y «Confirmar nueva contraseña» y pulsa «Restablecer contraseña». **Verás:** «Contraseña restablecida» — «Su contraseña ha sido restablecida exitosamente.» y el inicio de sesión. | “Listo: ya puedes entrar con la contraseña nueva.” |
| 5 | Muestra una diapositiva con `Administración › Usuarios › Listado` › usuario › «Resetear Contraseña» (video 1.2). | “Si no eres administrador, no te llegará correo: pídele al administrador que te restablezca la contraseña. En tu siguiente ingreso deberás cambiarla.” |

**Cierre:** Acceso resuelto. Veamos las notificaciones y tu cuenta.

### 0.4 · Notificaciones, Mi cuenta y cerrar sesión
**Duración:** 0:47 min · **Rol:** Todos

**OBJETIVO** · Leer los avisos del sistema, ajustar las preferencias y cerrar la sesión.
**GRABA CON** · `video.comext` (C5); el ingreso del paso 3 lo registra `video.vigilancia` (C2) fuera de cámara.
**REQUISITOS** · Avisos de Comercio Exterior guardados (p. ej. «Nuevo depósito de importación» de la Serie 5). VID109 sin ingreso abierto (4.4).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Pulsa la campana con su contador. **Verás:** el panel «Notificaciones» con el botón «Marcar todas». Pulsa un aviso: se marca como leído. | “En este video vas a revisar tus avisos. La campana muestra cuántos tienes sin leer; cada rol recibe solo los suyos. Vigilancia, por ejemplo, no recibe avisos.” |
| 2 | Pulsa «Ver todas las notificaciones». **Verás:** «Notificaciones» — «Gestiona todas tus notificaciones del sistema», el filtro «Todas / No leídas / Leídas» y «Marcar como leída» en cada aviso. | “En la página completa filtras tus avisos y los marcas como leídos.” |
| 3 | Vigilancia registra el ingreso de VID109 en su puesto (fuera de cámara). **Verás:** en Comercio Exterior el aviso emergente «Trazabilidad» — «Camión VID109 cambió a estado: Ingreso registrado». | “Algunos avisos llegan en tiempo real, como los de trazabilidad: salen en pantalla, pero no se guardan en la campana.” |
| 4 | Pulsa el ícono de usuario («Mi cuenta»). **Verás:** tus roles, «Preferencias» con el interruptor «Tema claro», «Tipo de menú» («Estático» / «Horizontal») y «Atajos de teclado». | “En Mi cuenta cambias el tema y el tipo de menú y consultas los atajos de teclado de tu rol.” |
| 5 | Pulsa «Cerrar sesión». **Verás:** «¿Está seguro que desea cerrar sesión del sistema?». Pulsa «Aceptar». | “Cierra siempre tu sesión al terminar el turno.” |

**Cierre:** Ya conoces lo básico de la pantalla. Cerramos la introducción con la trazabilidad.

### 0.5 · Trazabilidad: seguir un camión por etapas
**Duración:** 0:54 min · **Rol:** Administrador y Comercio exterior

**OBJETIVO** · Seguir en tiempo real cada camión por las etapas de la operación.
**GRABA CON** · `video.comext` (C5) o `video.admin` (C1).
**REQUISITOS** · Camiones de la semana en etapas distintas (Series 4 a 6).

| # | En pantalla (lo que haces) | Narración sugerida (lo que dices) |
|---|---|---|
| 1 | Inicia sesión. **Verás:** `Dashboards › Trazabilidad` con «Trazabilidad» — «Seguimiento en tiempo real de camiones en planta» y «Actualizado justo ahora». | “En este video vas a seguir los camiones. La trazabilidad es la pantalla de inicio del administrador y de Comercio Exterior, y se actualiza sola.” |
| 2 | Pulsa «Esta semana» en el filtro «Hoy / Esta semana / Este mes / Todo el historial». Señala «En sitio», «En báscula», «En bodega» y «Pend. salida». | “Arriba, cuántos camiones hay en cada parte de la operación.” |
| 3 | Señala la lista «Camiones» con la etapa de cada tarjeta («En portería», «Pesado (1er peso)», «En bodega (descarga)», «Completado», «Salida registrada») y usa «Buscar placa, conductor...». | “Cada tarjeta dice en qué etapa va el camión, con su conductor, transportadora y tiempo.” |
| 4 | Pulsa la tarjeta de VID101. **Verás:** el panel con «Información General», «Báscula», «Bodega» y «Progreso» («Ingreso», «Báscula», «Bodega», «Pesaje Final», «Salida»). No acerques los campos de estado [verificar en pantalla: algunos salen en inglés]. | “El detalle muestra los pesos, la bodega y el progreso del camión.” |
| 5 | En la barra superior escribe VID108 en «Buscar por placa...» y pulsa Enter. **Verás:** el filtro en «Todo el historial» y el camión de días anteriores. | “Con la búsqueda por placa ves todo el historial de un camión.” |

**Cierre:** Ese es el recorrido del sistema. Continúa con la serie de tu rol: la Serie 1 empieza por la administración.
