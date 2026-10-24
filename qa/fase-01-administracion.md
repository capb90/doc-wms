# Fase 1 — Administración (incluye autenticación y datos maestros)

> Lee antes `00-plan-maestro.md`. Rol principal: **Admin** (`capb90`). Algunas pruebas usan otros roles para verificar el efecto.
> **Objetivo adicional:** dejar creado y verificado el **dataset maestro QA** (§5.2 del plan maestro) que usan las fases 2 a 11.

## 1. Objetivo

Validar a fondo la autenticación y la sesión, la gestión de usuarios y roles, los terceros y sus convenios, todos los catálogos de Administración, los servicios y tarifas, los parámetros, y comprobar que cada catálogo llega correctamente a los módulos que lo consumen.

## 2. Alcance

| Pantalla | Ruta | Bloque |
|---|---|---|
| Login, cambio y recuperación de contraseña | `/auth/*` | AUT |
| Usuarios | `/admin/users` | USR |
| Terceros (Stakeholders) y atajos Clientes / Transportadoras / Agencias | `/admin/stakeholders[?rol=]` | TER |
| Convenios (detalle del tercero) | `/admin/stakeholders/[id]` | CNV |
| Productos | `/admin/products` | PRO |
| Tipos de embalaje | `/admin/packaging-types` | EMB |
| Unidades de medida | `/admin/unit-measures` | UME |
| Tipos de unidad de carga | `/admin/cargo-unit-types` | TUC |
| Ciudades | `/admin/cities` | CIU |
| Cuadrillas | `/admin/crews` | CUA |
| Motivos de ingreso | `/admin/entry-reasons` | MOT |
| Conductores | `/admin/drivers` | CON |
| Vehículos | `/admin/vehicles` | VEH |
| Ubicaciones | `/admin/locations` | UBI |
| Servicios, precios, tarifas base, mínimos, impuestos | `/admin/services` | SRV |
| Tarifas de montacargas | `/admin/forklift-rates` | MTC |
| Parámetros (desde el perfil) | `/admin/parameters` | PAR |
| Efecto en otros módulos | varias | DEP |

**Fuera:** la auditoría (fase 7), la matriz completa de permisos (fase 9), la configuración de facturación por cliente (fase 6), la migración legacy (anexo de la fase 11).

## 3. Criterios de entrada

1. Fase 0 aprobada.
2. Cuenta Admin operativa.
3. Ambiente local preferido (algunos casos de sesión requieren esperar la expiración del token: 60 min en la configuración de desarrollo y staging).

## 4. Reglas que se verifican (resumen del código)

- Contraseña: 8–100 caracteres, mayúscula, minúscula, dígito, especial `!@#$%^&*()+{}:<>?`, sin espacios.
- Usuario: nombre ≥ 3 (backend), username ≥ 3 y único, identificación entera > 100, email válido (no único), teléfono ≥ 5, al menos un rol.
- Tercero: (tipo de identificación, número) único **al crear**; al menos un rol de negocio. Tipos: NIT, RUT, CC, Pasaporte, RUC. Roles: CUSTOMER, IMPORTER, EXPORTER, CUSTOMS_AGENCY, TRANSPORT_COMPANY.
- Producto: nombre o SKU únicos al crear; unidad de medida obligatoria y activa.
- Catálogos con DELETE físico bloqueado si hay dependencias (embalaje, unidad, tipo de unidad de carga, ciudad, cuadrilla, motivo, ubicación).
- Servicio: código `^[A-Z][A-Z0-9_]+$` (3–32), único; no se desactiva con convenios activos; MONTACARGAS no admite impuestos; ALMACENAMIENTO no admite `PER_VEHICLE_TYPE`.
- Tarifa base: única entre activas por (servicio, producto, modalidad).

## 5. Casos

### 5.1 Autenticación y sesión (AUT)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-AUT-001 | Login correcto Admin | Login con Admin. | Entra a `/`. En Red: `auth/login` 200 con access y refresh token y roles en código (Admin…). | P0 | FUN |
| F1-AUT-002 | Usuario sin distinguir mayúsculas | Login con `CAPB90`. | Entra (el username no distingue mayúsculas). | P2 | FUN |
| F1-AUT-003 | Contraseña errada | Contraseña incorrecta. | «Credenciales inválidas». | P0 | ERR |
| F1-AUT-004 | Usuario inexistente | Usuario `qa_noexiste`. | «Credenciales inválidas» (mismo mensaje que F1-AUT-003). | P1 | SEG |
| F1-AUT-005 | Usuario inactivo | Login con `qa_inactivo` (tras F1-USR-013). | Rechazo. Anotar el texto: el código responde «Usuario inactivo», que revela la existencia del usuario (OBSERVACIÓN de seguridad). | P1 | SEG |
| F1-AUT-006 | Campos vacíos | Enviar sin usuario o sin contraseña. | Validación en el formulario; no se envía la petición. | P2 | VAL |
| F1-AUT-007 | Intentos fallidos repetidos | 10 logins fallidos seguidos con un usuario de prueba. | Anotar: el código no tiene bloqueo por intentos ni límite de peticiones (OBSERVACIÓN de seguridad, no BLOCKER). | P2 | SEG |
| F1-AUT-008 | Refresh automático | Con sesión, esperar a que el access token expire (o, en local, borrar el access token del `localStorage` dejando el refresh) y navegar. | Una sola llamada a `auth/refresh-token` 200; la petición original se reintenta y la página carga sin pedir login. | P1 | PER |
| F1-AUT-009 | Refresh inválido | Borrar ambos tokens de `localStorage` y navegar. | Redirige a `/auth/login`. | P1 | ERR |
| F1-AUT-010 | Debe cambiar contraseña | Crear un usuario o resetear su contraseña (F1-USR-011) y entrar con él. | Va a `/auth/change-password`; no puede navegar a otra ruta hasta cambiarla. | P0 | FUN |
| F1-AUT-011 | Política de contraseña en el cambio | En change-password, probar: 7 caracteres; sin mayúscula; sin dígito; sin especial; con espacio; con un especial no permitido (p. ej. `-`); 101 caracteres. | Cada una rechazada con mensaje claro; una válida se acepta y lleva a la ruta del rol. | P1 | VAL |
| F1-AUT-012 | Cambio voluntario de contraseña | Con un usuario sin «debe cambiar», buscar en el perfil una opción de cambiar contraseña; abrir `/auth/change-password`. | Anotar: según el código no existe pantalla voluntaria y la página expulsa al usuario (R-ADM-14). Registrar como OBSERVACIÓN/MAJOR según criterio del usuario. | P1 | FUN |
| F1-AUT-013 | Cambio sin contraseña actual | En change-password. | Anotar si pide la contraseña actual (el código no la pide). OBSERVACIÓN de seguridad. | P2 | SEG |
| F1-AUT-014 | Recuperación para Admin | `/auth/request-password-reset` con un Admin con correo. | Mensaje de éxito; en local/staging el correo va a Mailtrap (verificar si hay acceso). El enlace lleva a `/auth/reset-password?token=…`. | P2 | FUN |
| F1-AUT-015 | Recuperación para no Admin | La misma pantalla con `bascula`. | Anotar el mensaje: el código responde 401 «Solo los administradores…» y además redirige al login. Revela existencia y rol (R-ADM-13). | P2 | SEG |
| F1-AUT-016 | Token de reset inválido o vencido | Abrir `/auth/reset-password?token=abc`. | «El token es inválido o ha expirado»; no se cambia nada. | P2 | ERR |
| F1-AUT-017 | Logout revoca refresh | Logout; reutilizar por API el refresh token anterior en `auth/refresh-token`. | Rechazado. | P1 | SEG |
| F1-AUT-018 | Access token tras logout | Tras logout, usar por API el access token anterior en `GET user/me`. | Anotar: sigue válido hasta expirar (autenticación sin estado) (R-ADM-05). OBSERVACIÓN. | P2 | SEG |
| F1-AUT-019 | Dos pestañas | Abrir la app en dos pestañas; forzar refresh en una (F1-AUT-008); navegar en la otra. | Anotar si la otra pestaña pierde la sesión por la rotación del refresh token. | P2 | PER |

### 5.2 Usuarios (USR)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-USR-001 | Listado y filtros | `/admin/users`: filtrar por nombre, usuario, correo, identificación y estado. | Cada filtro reduce la lista correctamente; limpiar filtros restaura. | P1 | FUN |
| F1-USR-002 | Crear usuario válido | Crear `qa_bascula2` con rol Operario báscula, datos válidos. | Se crea; aparece en la lista; detalle muestra roles. Al entrar, pide cambiar contraseña (anotar si no). | P0 | FUN |
| F1-USR-003 | Crear las cuentas faltantes del §4 | Crear los usuarios del README que no existan, con sus roles exactos. | Quedan activos. Anotar en el registro de datos (sin contraseñas). | P0 | FUN |
| F1-USR-004 | Username duplicado | Crear otro usuario con username `bascula`. | Error claro de duplicado; no se crea. | P1 | VAL |
| F1-USR-005 | Validaciones de campos | Nombre de 2 caracteres; identificación 50; email inválido; teléfono de 4; sin roles. | Cada uno rechazado. Anotar si el frontend acepta nombre de 1 carácter y el backend lo rechaza (mensaje mostrado). | P1 | VAL |
| F1-USR-006 | Confirmación de contraseña | En el alta, escribir contraseña y confirmación distintas. | Esperado: el formulario impide guardar («las contraseñas no coinciden»). Riesgo R-ADM-04: puede guardarse. | P1 | VAL |
| F1-USR-007 | Email repetido | Crear un usuario con el email de otro. | Anotar: el backend permite emails repetidos. OBSERVACIÓN (afecta a la recuperación). | P3 | RN |
| F1-USR-008 | Editar perfil | Editar nombre, teléfono, email de `qa_bascula2`. | Se guarda; el detalle refleja el cambio tras recargar. | P1 | PER |
| F1-USR-009 | Asignar rol | A `qa_bascula2` agregar Operario bodega. | Tras **nuevo login** del usuario, ve menús de Báscula y Bodega. Anotar si se refleja sin re-login (el código dice que no). | P1 | ROL |
| F1-USR-010 | Quitar rol | Quitar Operario bodega. | Tras re-login ya no accede a `/warehouse`. Probar quitar todos los roles: anotar si lo permite. | P1 | ROL |
| F1-USR-011 | Reset de contraseña por Admin | Resetear la contraseña de `qa_bascula2`. | El usuario debe cambiarla al entrar (F1-AUT-010). Confirmación coincidente validada aquí. | P1 | FUN |
| F1-USR-012 | Admin se quita su rol Admin | Con `v_montenegro` (Admin + Facturación) quitarse Admin a sí mismo (en una cuenta de prueba, no la principal). | Anotar si lo impide. Si lo permite, OBSERVACIÓN/MAJOR (riesgo de quedarse sin administradores). | P2 | RN |
| F1-USR-013 | Desactivar usuario | Crear `qa_inactivo` y desactivarlo sin fecha. | Estado Inactivo; no puede iniciar sesión (F1-AUT-005). | P0 | FUN |
| F1-USR-014 | Desactivar con fecha de bloqueo | Desactivar un usuario con fecha de bloqueo = mañana. | Anotar el comportamiento: según el código la fecha no reactiva sola al usuario (R-ADM-05). Verificar la UI: ¿qué promete la fecha? | P2 | RN |
| F1-USR-015 | Usuario desactivado con sesión abierta | Iniciar sesión con `qa_bascula2` en otra ventana; desactivarlo desde Admin; seguir navegando con él. | Anotar cuánto tiempo sigue operando (esperado según el código: hasta que vence el access token; el refresh se rechaza). | P1 | SEG |
| F1-USR-016 | Reactivar | Reactivar `qa_bascula2`. | Puede iniciar sesión otra vez. | P1 | FUN |
| F1-USR-017 | Admin se desactiva a sí mismo | Con una cuenta Admin de prueba, desactivarse. | Anotar si lo permite. | P2 | RN |
| F1-USR-018 | No hay borrado | Buscar opción de eliminar usuario. | No existe (por diseño). | P3 | FUN |

### 5.3 Terceros (TER)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-TER-001 | Crear cliente | Crear `QA Cliente Uno SAS`, NIT, rol CUSTOMER, con un contacto y una cuenta bancaria. | Se crea; detalle con contacto y cuenta; estado financiero Activo. | P0 | FUN |
| F1-TER-002 | Crear el resto del dataset | Crear los terceros del §5.2 del plan maestro (Mora, Consolidado, Importador, Exportador, Agencia SIA, Transportes, ecuatoriano con RUC). | Todos creados con sus roles. Registrar IDs. | P0 | FUN |
| F1-TER-003 | Varios roles en un tercero | Crear `QA Multirol` con CUSTOMER + IMPORTER. | Aparece al filtrar por cada rol y en los selectores de cliente e importador en báscula y CE. | P1 | RN |
| F1-TER-004 | Sin rol | Crear un tercero sin roles. | Rechazado («al menos un rol»). | P1 | VAL |
| F1-TER-005 | Identificación duplicada al crear | Crear otro con el mismo NIT y tipo de `QA Cliente Uno`. | 409 «Ya existe un stakeholder…» mostrado de forma legible. | P0 | VAL |
| F1-TER-006 | Mismo número, otro tipo | Mismo número con tipo CC. | Se permite (la unicidad es por tipo + número). | P2 | RN |
| F1-TER-007 | Nombre corto | Nombre de 2 caracteres. | Rechazado; anotar si el frontend lo deja pasar y qué mensaje muestra el backend. | P2 | VAL |
| F1-TER-008 | Duplicado al editar | Editar `QA Importador` y ponerle el NIT de `QA Cliente Uno`. | Esperado: mensaje claro de duplicado. Riesgo R-ADM-06: 409 con texto crudo de Postgres. | P1 | ERR |
| F1-TER-009 | Editar datos y persistencia | Cambiar nombre, contacto, cuenta; recargar. | Cambios persistidos. | P1 | PER |
| F1-TER-010 | Quitar/agregar rol | Quitar IMPORTER a `QA Multirol`; volver a agregarlo. | Se refleja en los filtros y en los selectores de báscula. | P1 | RN |
| F1-TER-011 | Desactivar tercero | Desactivar `QA Exportador` temporalmente. | No aparece en selectores de báscula/CE (verificar en F1-DEP-003); reactivar al final. | P1 | INT |
| F1-TER-012 | Borrar contacto y cuenta | Eliminar un contacto y una cuenta bancaria. | Se eliminan (borrado físico). | P2 | FUN |
| F1-TER-013 | Búsqueda global (WMS-7) | Buscar por: parte del nombre sin tildes («Importacion» para «Importación»), parte de la identificación, email de un contacto, teléfono de un contacto. | Encuentra el tercero en cada caso, sin distinguir mayúsculas ni tildes. | P1 | FUN |
| F1-TER-014 | Filtro por identificación parcial (WMS-22) | Filtrar por los 4 dígitos centrales del NIT. | Encuentra el tercero. | P1 | FUN |
| F1-TER-015 | Filtros por rol y estado financiero | Filtrar por CUSTOMS_AGENCY; por estado Activo/Bloqueado; por activo/inactivo. | Resultados coherentes. | P1 | FUN |
| F1-TER-016 | Atajos del menú (UI-23) | Menú → Clientes / Transportadoras / Agencias de aduanas. | Abren la lista con `?rol=` y el filtro de rol visible coincide con la URL. | P1 | UX |
| F1-TER-017 | Tercero ecuatoriano | Crear con RUC y contacto con país Ecuador. | Se guarda; aparece con tipo RUC en listados. | P2 | FUN |
| F1-TER-018 | Paginación | Con > 10 terceros, recorrer páginas y cambiar tamaño. | Sin duplicados ni saltos; el total coincide. | P2 | FUN |
| F1-TER-019 | Bloquear y desbloquear salidas | Con `c_exterior` (o Facturación o Admin), en el detalle del tercero → «Bloquear salidas» con un motivo de 10 a 500 caracteres. Intentar crear una orden de cargue, agregar ítems a una orden, emitir la guía y ejecutar el cargue (Bodega) con un depósito de ese cliente. Después «Desbloquear salidas» con motivo y repetir. | El tercero muestra la etiqueta «Salidas bloqueadas» con motivo, fecha y autor. Las cuatro operaciones responden 400 «El cliente '…' tiene las salidas bloqueadas: …». Los ingresos, la báscula y los cobros siguen. Al desbloquear, pasan. Bloquear dos veces o con motivo corto responde 400; quedan dos filas en auditoría (con el motivo). Receiving, Scale y Warehouse no ven el botón y el API responde 403 (DEC-052, D8, D9). | P1 | RN |

### 5.4 Convenios (CNV)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-CNV-001 | Crear convenio | En `QA Cliente Uno`, crear convenio con referencia y nombre válidos, activo. | Se crea y aparece en el detalle. | P0 | FUN |
| F1-CNV-002 | Servicio ALMACENAMIENTO `PERCENTAGE_OF_VALUE` | Agregar ALMACENAMIENTO, modalidad IMP, fórmula `PERCENTAGE_OF_VALUE` con `percentage`, `minimum`, `minimumThreshold`. | Se guarda; la vista previa de la fórmula muestra un valor (anotar; ver R-FAC-09). | P0 | FUN |
| F1-CNV-003 | Servicios BASCULA, MONTACARGAS, GUIA_SALIDA | Agregarlos con `FIXED` (montacargas: anotar si ofrece tarifa por tipo de vehículo). | Se guardan. Registrar valores en el registro de datos (se usan en fase 3/4/5/6). | P0 | FUN |
| F1-CNV-004 | Parámetros obligatorios | Guardar `PER_UOM` sin `uom`; `FIXED` sin `rate`. | Rechazado con mensaje del parámetro faltante. | P1 | VAL |
| F1-CNV-005 | Tipo de parámetro | `rate` con texto; entero con decimales. | Rechazado. | P2 | VAL |
| F1-CNV-006 | Porcentaje fuera de rango | `PERCENTAGE_OF_VALUE` con `percentage` 150. | Esperado: rechazo (0–100). Riesgo R-FAC-15 (MAF-07): puede guardarse y caer al mínimo al facturar. | P1 | VAL |
| F1-CNV-007 | Fórmula prohibida | ALMACENAMIENTO con `PER_VEHICLE_TYPE`. | Rechazado. | P1 | RN |
| F1-CNV-008 | Producto o modalidad inactivos | Asociar un producto inactivo. | Rechazado. | P2 | VAL |
| F1-CNV-009 | Activación programada pasada | Fecha de activación ayer. | Rechazado. «Hoy» sí es válido: la fecha es de día, sin hora, en hora de Colombia (plan P1, fase 7). | P2 | VAL |
| F1-CNV-010 | Desactivar / quitar servicio del convenio | Desactivar MONTACARGAS del convenio; luego reactivar. | Cambia el estado. (El efecto en la tarifa se prueba en fase 6.) | P1 | FUN |
| F1-CNV-011 | Servicio complementario | Agregar a ALMACENAMIENTO un servicio complementario (p. ej. PAPELERIA) **sin** tarifa configurada. | Se guarda. Anotar: prepara la prueba de R-FAC-08 en fase 6 (dejar desactivado tras anotar, para no bloquear otras fases). | P2 | INT |
| F1-CNV-012 | Acceso por menú Convenios / Tarifas | Menú Terceros → Convenios / Tarifas. | Abren la vista correspondiente. | P2 | UX |
| F1-CNV-013 | Programado se activa en su fecha y archiva el anterior | Convenio activo en un cliente. Crear otro «Programado» con la fecha de hoy (o llevar su fecha a hoy). Reiniciar el API (el job corre a los 30 s del arranque y a las 00:00:30 de Colombia). | El programado queda `Active` y el anterior `Archived`; Facturación recibe el aviso «Convenio programado activado» y las facturas existentes **no** se recalculan. Antes de que corra el job, el resolutor ya aplica la tarifa del programado desde las 00:00 de su fecha. Dos activos del mismo cliente son imposibles (índice único corregido). Sin vigencia final (D20, D21). | P1 | RN |
| F1-CNV-014 | Programado sin fecha | Crear un convenio con estado «Programado» sin fecha de activación. | 400 «Un convenio programado necesita la fecha de activación.». En el formulario, la fecha ya no dice «(Opcional)». | P2 | VAL |

### 5.5 Productos (PRO)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-PRO-001 | Crear producto | Crear `QA Cebolla` (unidad bulto o kg). El SKU lo propone el sistema. | Se crea; aparece en el listado y en el detalle. | P0 | FUN |
| F1-PRO-002 | Crear dataset | `QA Aceite` (litro), `QA Repuestos` (unidad). | Creados. | P0 | FUN |
| F1-PRO-003 | Unidad obligatoria y activa | Sin unidad; con unidad inactiva (desactivarla antes en UME). | Rechazado. | P1 | VAL |
| F1-PRO-004 | Nombre o SKU duplicado al crear | Crear otro `QA Cebolla`; otro con el SKU de `QA Aceite`. | 409 legible. | P1 | VAL |
| F1-PRO-005 | Duplicado al editar | Editar `QA Aceite` con el SKU de `QA Cebolla`; con el nombre de otro producto. | SKU: esperado mensaje legible (R-ADM-06: puede ser texto crudo de Postgres). Nombre: anotar si permite repetir. | P1 | ERR |
| F1-PRO-006 | Embalaje al vuelo | En el formulario, crear un tipo de embalaje rápido. | Se crea y queda seleccionado. | P2 | FUN |
| F1-PRO-007 | Desactivar producto | Desactivar `QA Repuestos`. | No aparece en el selector de mercancía de báscula (F1-DEP-002). Reactivar al final. | P1 | INT |
| F1-PRO-008 | Perecedero | Marcar `QA Cebolla` como perecedero si existe el campo (WMS-32). | Se guarda; se usa en tarifas con dimensión perecedero (fase 6). | P2 | RN |

### 5.6 Catálogos simples (EMB, UME, TUC, CIU, CUA, MOT, CON, VEH, UBI)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-EMB-001 | Crear embalaje | Código `QA-CAJA` (≤ 20), nombre (≤ 100). | Se crea. | P1 | FUN |
| F1-EMB-002 | Código duplicado / largo | Repetir `QA-CAJA`; código de 21 caracteres. | Rechazados. | P2 | VAL |
| F1-EMB-003 | Borrar en uso | Borrar un embalaje usado por un producto de depósito (tras fase 3) o por un producto. | Bloqueado con mensaje legible; anotar si aparece error de clave foránea crudo. | P2 | ERR |
| F1-EMB-004 | Activar/desactivar | Buscar la opción. | Anotar: no existe (solo código y nombre). | P3 | FUN |
| F1-UME-001 | Crear unidad | Código único (≤ 30), nombre, activa. | Se crea; el código no se puede editar después. | P1 | FUN |
| F1-UME-002 | Borrar en uso | Borrar la unidad de `QA Cebolla`. | Bloqueado: «…desactívela». | P1 | RN |
| F1-UME-003 | Desactivar | Desactivar una unidad sin uso. | No aparece para productos nuevos ni líneas libres de báscula. | P2 | INT |
| F1-TUC-001 | Tipos de unidad de carga | Ver Contenedor, Tanquero, Remolque; crear `QA-ISOTANQUE`. | Se crea; aparece en el editor de unidades de carga de báscula. | P1 | FUN |
| F1-TUC-002 | Borrar en uso | Tras fase 3, borrar Contenedor. | Bloqueado. | P2 | RN |
| F1-CIU-001 | Crear ciudad | `QA QUITO`, país `ECU`, distrito, 3 días de tránsito. | Se crea en mayúsculas. | P1 | FUN |
| F1-CIU-002 | Ciudad destino de abandono | Crear `QA BOGOTA` (COL) marcada como destino de abandono, 0 días. | Se crea. Se usa en el reporte de salidas a abandono (fase 7). | P1 | FUN |
| F1-CIU-003 | Duplicado | Repetir nombre + país + distrito (con otra capitalización). | 409 «Ya existe la ciudad…». | P1 | VAL |
| F1-CIU-004 | Validaciones | Nombre de 36; país de 2 letras; días 100. | Rechazados. | P2 | VAL |
| F1-CIU-005 | Borrar en uso | Tras fase 5, borrar la ciudad destino de una orden. | 409. | P2 | RN |
| F1-CIU-006 | Importación CSV (simulación) | Importar un CSV `id_ciudad;nom_ciudad;id_pais;distrito;dias` con `dryRun`. | Muestra el resultado sin crear; con error por fila si hay líneas malas. Archivo > 2 MB rechazado. | P3 | FUN |
| F1-CUA-001 | Crear cuadrilla | `QA Cuadrilla 1`. | Se crea; aparece en recepción y órdenes de cargue. | P1 | FUN |
| F1-CUA-002 | Duplicado normalizado | ` qa cuadrilla 1 ` (espacios y minúsculas). | Rechazado como duplicado. | P2 | VAL |
| F1-CUA-003 | Borrar en uso | Tras fase 4, borrar la cuadrilla usada. | 409. | P2 | RN |
| F1-MOT-001 | Motivos sembrados | Ver la lista. | 7 motivos; «requiere pesaje» en los 5 de cargue/descargue y Solo báscula; no en Solo bodega ni Otro. | P0 | RN |
| F1-MOT-002 | Crear motivo | `QA Motivo pesaje`, requiere pesaje. | Se crea y aparece en el ingreso de Vigilancia. | P2 | FUN |
| F1-MOT-003 | Borrar en uso | Tras fase 2, borrar un motivo con ingresos. | Bloqueado. | P2 | RN |
| F1-MOT-004 | Cambiar «requiere pesaje» | Desmarcar en `QA Motivo pesaje`. | Un ingreso nuevo con ese motivo no entra a la cola de báscula (verificar en fase 2). **No modificar los motivos sembrados.** | P2 | INT |
| F1-CON-001 | Crear conductor | Colombiano CC y ecuatoriano (pasaporte o cédula), nombres y apellidos ≤ 150. | Creados. | P1 | FUN |
| F1-CON-002 | Duplicado | Mismo tipo y número. | 409. | P1 | VAL |
| F1-CON-003 | Desactivar | Desactivar uno. | Anotar si la búsqueda por documento en báscula lo sigue encontrando. | P2 | INT |
| F1-VEH-001 | Crear vehículo | Tractomula `QAA101` con `QA Transportes`; Sencillo `QAA102`; otro `QAA103`. | Creados. | P1 | FUN |
| F1-VEH-002 | Transportadora inexistente o sin rol | Asignar un tercero sin rol TRANSPORT_COMPANY. | Anotar si lo permite. | P2 | VAL |
| F1-VEH-003 | Placa duplicada | Crear otra vez `QAA101`. | 409 «La placa QAA101 ya existe.». | P1 | VAL |
| F1-VEH-004 | Placa duplicada con otra capitalización | Crear `qaa101`. | Esperado: rechazo o normalización a `QAA101`. Riesgo R-ADM-16: puede crearse un duplicado. | P1 | PER |
| F1-VEH-005 | Formato de placa | Placa con espacios o símbolos (`QA A-1#`). | Anotar si se normaliza o se rechaza (Vigilancia normaliza; el alta del catálogo no valida formato). | P2 | VAL |
| F1-UBI-001 | Ubicaciones sembradas | Ver lista. | 20 ubicaciones (A/B/C, patios, recepción, despacho, tránsito, cuarentena). | P1 | FUN |
| F1-UBI-002 | Crear con datos inválidos | Código vacío; capacidad negativa. | Esperado: rechazo. Riesgo R-ADM-16: el alta no tiene validador. | P2 | VAL |
| F1-UBI-003 | Código duplicado | Repetir `A01-R01-N01`. | 409. | P2 | VAL |
| F1-UBI-004 | Deshabilitar | Marcar una ubicación no disponible. | No se puede ubicar mercancía en ella (fase 4). | P2 | INT |
| F1-UBI-005 | Borrar en uso | Tras fase 4, borrar una ubicación con mercancía. | Bloqueado (anotar si solo mira depósitos y no asignaciones). | P2 | RN |

### 5.7 Servicios y tarifas (SRV, MTC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-SRV-001 | Servicios sembrados | `/admin/services`. | BASCULA, ALMACENAMIENTO, MONTACARGAS, PAPELERIA, GUIA_SALIDA, activos. | P0 | FUN |
| F1-SRV-002 | Precio base BASCULA | En BASCULA, registrar `ServicePrice` vigente desde hoy (p. ej. $23.000). | Se guarda; queda como vigente. | P0 | FUN |
| F1-SRV-003 | Precio con vigencia futura | Inicio mañana. | Rechazado. | P2 | VAL |
| F1-SRV-004 | Fin antes que inicio | Fecha final anterior. | Rechazado. | P2 | VAL |
| F1-SRV-005 | Nuevo precio reemplaza al vigente | Registrar un segundo precio en BASCULA. | Anotar qué pasa con el anterior (el código expira el vigente, MAF-08). | P2 | RN |
| F1-SRV-006 | Precio GUIA_SALIDA | Registrar precio vigente. | Se guarda (sin esto falla la guía para clientes sin convenio). | P0 | FUN |
| F1-SRV-007 | Tarifa base ALMACENAMIENTO IMP | Regla `PER_UOM` con `uom` = código de la unidad de `QA Cebolla`, `rate`. | Se guarda. | P0 | FUN |
| F1-SRV-008 | Tarifa base ALMACENAMIENTO EXP | Regla `FIXED`. | Se guarda. | P0 | FUN |
| F1-SRV-009 | Tarifa base duplicada | Otra regla activa con el mismo servicio, producto y modalidad. | 409. | P1 | VAL |
| F1-SRV-010 | `uom` inválida | `uom` con espacios o 31 caracteres. | Rechazado (regex `^[A-Za-z0-9_]{1,30}$`). | P2 | VAL |
| F1-SRV-011 | Mínimos de almacenamiento | Editar `ServiceMinimumValue` de IMP a un valor > 0 (p. ej. $184.000). | Se guarda; EXP e INSP quedan en $0 o el valor que el usuario indique. | P0 | FUN |
| F1-SRV-012 | Mínimo negativo | Valor −1. | Rechazado. | P2 | VAL |
| F1-SRV-013 | Impuesto en ALMACENAMIENTO | Verificar ALMACENAMIENTO con IVA (sembrado). | IVA 19 % asociado. | P1 | RN |
| F1-SRV-014 | Impuesto en MONTACARGAS | Intentar asociar IVA a MONTACARGAS. | Rechazado: «el IVA se decide en cada cobro» (WMS-28). | P1 | RN |
| F1-SRV-015 | IVA en BASCULA | Anotar si BASCULA tiene ServiceTax. Decidir con el usuario si se asocia (cambia el desglose del cobro en fase 3). | Configuración registrada. | P1 | RN |
| F1-SRV-016 | Crear servicio | Código `QA_SERVICIO`, nombre. | Se crea. Código inválido (`qa servicio`, 2 caracteres, 33 caracteres) rechazado. | P2 | VAL |
| F1-SRV-017 | Desactivar servicio con convenio activo | Desactivar GUIA_SALIDA (está en el convenio de `QA Cliente Uno`). | 409. **No desactivar servicios sembrados en otros casos.** | P1 | RN |
| F1-SRV-018 | Fórmula prohibida en tarifa base | ALMACENAMIENTO con `PER_VEHICLE_TYPE`. | Rechazado. | P1 | RN |
| F1-SRV-019 | Tarifas mínimas y dimensión perecedero (WMS-32) | Crear regla de almacenamiento con perecedero = sí y otra genérica. | Se guardan. Su efecto se valida en la fase 6. | P2 | RN |
| F1-SRV-020 | Previsualización de tarifas | Usar la vista previa en una regla. | Muestra un cálculo. Anotar valores para comparar con la fase 6 (R-FAC-09). | P2 | FUN |
| F1-MTC-001 | Tarifas de montacargas | `/admin/forklift-rates`: valor para Tractomula, DobleTroque, Sencillo, Turbo, GuacalEstiba. | Se guardan (upsert). | P0 | FUN |
| F1-MTC-002 | Monto negativo | −1. | Rechazado. | P2 | VAL |

### 5.8 Parámetros (PAR)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F1-PAR-001 | Acceso | Perfil → Parámetros (solo Admin). | Abre `/admin/parameters`. | P1 | FUN |
| F1-PAR-002 | Correo de ajustes | Editar `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` con un correo de prueba. | Se guarda. (Requisito del ajuste CE-7.) | P0 | FUN |
| F1-PAR-003 | Parámetros de empresa | Buscar `COMPANY_NAME`, `COMPANY_NIT`, `COMPANY_ADDRESS`, `COMPANY_PHONE`, `COMPANY_CITY`. | Anotar: según el código no están sembrados ni se pueden crear (R-ADM-10); los PDF salen con valores por defecto. | P1 | FUN |
| F1-PAR-004 | Valor inválido | Poner un texto no-correo en el parámetro de correo. | Anotar: el backend no valida (R-ADM-10). Restaurar el valor correcto. | P2 | VAL |

### 5.9 Efecto en otros módulos (DEP)

Verificación cruzada: el catálogo configurado aquí llega al módulo que lo usa. Solo se abre la pantalla consumidora y se mira el selector; no se completa la operación.

| ID | Caso | Rol | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|---|
| F1-DEP-001 | Motivos en Vigilancia | Vigilancia | Abrir Ingreso → selector de motivo. | Muestra los motivos (incluido `QA Motivo pesaje`). | P1 | INT |
| F1-DEP-002 | Productos y unidades en báscula | Báscula | Con un camión en la cola (si hay), abrir el registro → líneas de mercancía. | Ofrece productos activos; no ofrece `QA Repuestos` mientras esté inactivo; las líneas libres ofrecen unidades activas. | P1 | INT |
| F1-DEP-003 | Terceros por rol en báscula | Báscula | Panel «Datos para Comercio Exterior»: Cliente, Importador, Agencia, Exportador. | Cada selector muestra solo terceros activos con ese rol. | P1 | INT |
| F1-DEP-004 | Transportadoras y vehículos | Báscula | Card «Camión y conductor». | Transportadora lista solo TRANSPORT_COMPANY; buscar `QAA101` completa tipo y transportadora. | P1 | INT |
| F1-DEP-005 | Ciudades y cuadrillas en CE | CE | Nueva orden de cargue → ciudad destino y cuadrilla. | Muestra las ciudades activas y cuadrillas activas. | P2 | INT |
| F1-DEP-006 | Tarifa de montacargas en Bodega | Bodega | Abrir el diálogo de montacargas (sin completar) si hay un servicio. | Tarifa precargada por tipo de vehículo. (Si no hay servicio, verificar en fase 4.) | P2 | INT |

### 5.10 Cierre del dataset maestro (DAT)

| ID | Caso | Resultado esperado | P | Tipo |
|---|---|---|---|---|
| F1-DAT-001 | Dataset completo | Todos los elementos del §5.2 del plan maestro existen, activos (reactivar lo desactivado en pruebas) y anotados en `registro-datos-qa.md`. | P0 | PER |
| F1-DAT-002 | Estado de terceros | `QA Cliente Mora` con límite de crédito bajo queda configurado en la fase 6 (anotar como pendiente si la configuración de facturación no se hizo aquí). | P1 | PER |

## 6. Criterios de salida específicos

- Todos los P0 de AUT, USR, TER, CNV, PRO, SRV, MTC, PAR y DAT ejecutados.
- Dataset maestro completo (F1-DAT-001 `PASA`). **Sin dataset no se empieza la fase 2.**
- Riesgos verificados: R-ADM-04, 05, 06, 10, 13, 14, 16; R-FAC-15 (parcial).

## 7. Entregables

Informe de fase, fichas de defecto, `registro-datos-qa.md` con el dataset maestro. Detenerse.
