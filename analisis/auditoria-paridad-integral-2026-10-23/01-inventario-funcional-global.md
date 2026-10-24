# 01 — Inventario funcional global

> **Fecha de la auditoría:** 2026-10-23. Auditoría estática (código y documentación); no se ejecutó nada.
> **Referencia de código (según documentación):** `docs/contexto/estado.md` da como corte BE `develop` `35a61b2` y FE `develop` `c924a8b`. No se consultó Git (§3.1 del encargo): el código auditado es el que estaba en disco el 2026-10-23.

## 1. Cómo se armó

1. **Universo legacy.** Se parte del catálogo `bodegas-legacy/legacy-analysis/LEGACY_FUNCTIONAL_CATALOG.md` (263 funcionalidades `LEGACY-FUNC-001…263`, auditoría del 23-sep-2026). Se contrastó su cobertura con la estructura del checkout: 37 carpetas `modulos/mod_*`, `menus/` (incluye `backup.php`, `evaluaabandonos.php`, `evaluatasacambio.php`), `reportes/`, `reportesweb/`, `salidapuerta/`, `leerexcel/`, `cron.php`, `peso.php`, `consultapesa.php`, `migrarplacas.php`. Cada capacidad legacy recibe el ID estable **`CF-Lnnn`**, con el mismo número que `LEGACY-FUNC-nnn`. Los agentes pueden desglosarla por operación como `CF-Lnnn.a`, `CF-Lnnn.b`… y añadir capacidades no catalogadas como **`CF-Lnnn+`** (p. ej. `CF-L264`, `CF-L265`…) dentro de los rangos que les asigna `02-progreso.md`.
2. **Universo V2.** 51 controladores en `Backend/wms-api/Wms.Api/Controllers/v1/` (355 atributos `[Http*]` contados con grep), 6 jobs en `Wms.Api/BackgroundJobs/`, 94 páginas `.vue` en `Frontend/wms/app/pages/` y 18 carpetas de `app/features/`. Las capacidades sin equivalente legacy reciben **`CF-Vnnn`** (candidatas: el agente confirma en código y clasifica `SOLO_V2`, o las reasigna a una capacidad legacy si sí tienen equivalente).
3. **Asignación a módulos de auditoría.** Por flujo de negocio completo (no por capa). Los selectores AJAX legacy (`LEGACY-FUNC-235…254`) van al módulo cuyo flujo atienden.
4. **Estado previo.** La última columna copia el estado de `bodegas-legacy/docs/legacy_analysis/MIGRATION_MATRIX.md` (corte de código 2026-09-24, BE `b089d2b` / FE `26aed68`, decisiones del 2026-09-29). Es el punto de partida que esta auditoría contrasta; **no es un hallazgo**.

## 2. Alcance y exclusiones heredadas

| Exclusión | Capacidades | Fuente de la decisión | Tratamiento en esta auditoría |
| --- | --- | --- | --- |
| Colmotores (importador 70): VIN, seriales, voltajes, patio externo, lecturas, averías, portal de vehículos | 50 | `plan-backend-paridad-legacy.md` §A.3; `plan-frontend-paridad-legacy.md` §A.3; `MIGRATION_MATRIX.md` «Alcance (decisión del 2026-09-24)» | Se inventarían y se verifica que no haya restos ni dependencias en V2. Paridad integral `NO_APLICA` (excluida por decisión). |
| Acceso, autenticación, autorización, usuarios y roles | 11 | Mismas fuentes; `DEC-030` | Se audita el equivalente V2 como `SOLO_V2`/reemplazo y se registra la diferencia; la paridad integral de la fila legacy es `DIFERENCIA_INTENCIONAL`. |
| Decisiones «aceptado, no se construye» (GAP-004, 012, 018, 020, 022, 023; P16) | varias | `DECISIONES_REVISION.md`; `plan-backend` §A.3/§A.4 | Se verifica que el código respete la decisión; paridad `DIFERENCIA_INTENCIONAL`. |

## 3. Totales

| Concepto | Cantidad |
| --- | ---: |
| Capacidades legacy catalogadas (`CF-L001…263`) | 263 |
| De ellas excluidas por decisión (Colmotores + acceso) | 61 |
| Capacidades legacy evaluables | 202 |
| Capacidades V2 candidatas a `SOLO_V2` (`CF-Vnnn`) | 49 |
| Módulos de auditoría | 8 |

| Módulo | Legacy | Legacy excluidas | V2 candidatas |
| --- | ---: | ---: | ---: |
| 01-administracion-catalogos | 98 | 14 | 11 |
| 02-bascula | 22 | 0 | 6 |
| 03-vigilancia-bodega | 16 | 4 | 6 |
| 04-ce-ingresos-depositos | 24 | 2 | 7 |
| 05-ce-levantes-salidas | 28 | 3 | 4 |
| 06-facturacion | 22 | 0 | 8 |
| 07-reportes-exportaciones | 15 | 1 | 2 |
| 08-procesos-infra-fuera-alcance | 38 | 37 | 5 |

## 4. Áreas transversales (sin módulo propio; las audita el módulo que las usa)

| Área | Dónde se audita |
| --- | --- |
| Autenticación, roles y menú por rol (`WmsPolicyRoles`, `AppMenu.vue`, `usePermissions`) | 01, y cada módulo verifica los permisos de sus endpoints y pantallas |
| Auditoría genérica `IAuditable` → `audit_logs` | 01 |
| Archivos (S3/local), PDF y Excel | 07 (generación común); cada módulo, sus documentos |
| Notificaciones (tiempo real y correo) | 08 (infraestructura); cada módulo, sus eventos |
| Consecutivos (`DEC-012`) | 02 (tiquetes), 04 (depósitos), 05 (guías y órdenes) |
| Fechas `ColombiaTime` | todos |
| Paginación `all=true` | todos |

## 5. Procesos automáticos

| Proceso | Lado | Módulo |
| --- | --- | --- |
| `cron.php` (recalcula períodos de facturación, LEGACY-FUNC-234) | Legacy | 06 |
| `menus/evaluatasacambio.php` (alerta de TRM) | Legacy | 06 |
| `menus/evaluaabandonos.php` (alerta de abandono) | Legacy | 04 |
| `menus/backup.php` (copia de seguridad, LEGACY-FUNC-004) | Legacy | 08 |
| `peso.php`, `consultapesa.php` (lectura del último peso) | Legacy | 02 |
| `StoragePeriodAutoCloseBackgroundService`, `InvoiceDueNotificationBackgroundService`, `InvoicePaymentReconciliationBackgroundService`, `OverdueDetectionBackgroundService` | V2 | 06 |
| `AbandonmentAlertBackgroundService` | V2 | 04 |
| `DatabaseBackupBackgroundService` | V2 | 08 |

## 6. Capacidades legacy por módulo

`Crit.` = criticidad del catálogo legacy. `Estado previo` = `MIGRATION_MATRIX.md` (2026-09-24/29).

### 01-administracion-catalogos — Administración, catálogos, acceso y selectores

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L001 | LEGACY-FUNC-001 | Acceso interno | Iniciar sesión de operador | `index.php` (+2) | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L002 | LEGACY-FUNC-002 | Acceso interno | Cerrar sesión de operador | `aut_logout.php` | MEDIA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L003 | LEGACY-FUNC-003 | Navegación | Consultar panel, menú y alertas | `inicial.php` (+3) | MEDIA | PARCIAL |
| CF-L005 | LEGACY-FUNC-005 | Ciudades/destinos | Consultar ciudades/destinos | `modulos/mod_ciudades/listarciudades.php` | MEDIA | NO ENCONTRADA |
| CF-L006 | LEGACY-FUNC-006 | Ciudades/destinos | Registrar ciudades/destinos | `modulos/mod_ciudades/registrarciudad.php` | MEDIA | NO ENCONTRADA |
| CF-L007 | LEGACY-FUNC-007 | Ciudades/destinos | Modificar ciudades/destinos | `modulos/mod_ciudades/modificarciudad.php` | MEDIA | NO ENCONTRADA |
| CF-L008 | LEGACY-FUNC-008 | Ciudades/destinos | Eliminar ciudades/destinos | `modulos/mod_ciudades/eliminarciudad.php` | MEDIA | NO ENCONTRADA |
| CF-L009 | LEGACY-FUNC-009 | Clientes | Consultar clientes | `modulos/mod_clientes/listarclientes.php` | ALTA | CUBIERTA |
| CF-L010 | LEGACY-FUNC-010 | Clientes | Registrar clientes | `modulos/mod_clientes/registrarcliente.php` | ALTA | PARCIAL |
| CF-L011 | LEGACY-FUNC-011 | Clientes | Modificar clientes | `modulos/mod_clientes/modificarcliente.php` | ALTA | PARCIAL |
| CF-L012 | LEGACY-FUNC-012 | Clientes | Eliminar clientes | `modulos/mod_clientes/eliminarcliente.php` | ALTA | CUBIERTA |
| CF-L013 | LEGACY-FUNC-013 | Color de vehículo | Consultar color de vehículo | `modulos/mod_colorvehiculo/listarcolorvehiculo.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L014 | LEGACY-FUNC-014 | Color de vehículo | Registrar color de vehículo | `modulos/mod_colorvehiculo/registrarcolorvehiculo.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L015 | LEGACY-FUNC-015 | Color de vehículo | Modificar color de vehículo | `modulos/mod_colorvehiculo/modificarcolorvehiculo.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L016 | LEGACY-FUNC-016 | Color de vehículo | Eliminar color de vehículo | `modulos/mod_colorvehiculo/eliminarcolorvehiculo.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L021 | LEGACY-FUNC-021 | Cuadrillas | Consultar cuadrillas | `modulos/mod_cuadrillas/listarcuadrillas.php` | MEDIA | NO ENCONTRADA |
| CF-L022 | LEGACY-FUNC-022 | Cuadrillas | Registrar cuadrillas | `modulos/mod_cuadrillas/registrarcuadrilla.php` | MEDIA | NO ENCONTRADA |
| CF-L023 | LEGACY-FUNC-023 | Cuadrillas | Modificar cuadrillas | `modulos/mod_cuadrillas/modificarcuadrillas.php` | MEDIA | NO ENCONTRADA |
| CF-L024 | LEGACY-FUNC-024 | Cuadrillas | Eliminar cuadrillas | `modulos/mod_cuadrillas/eliminarcuadrilla.php` | MEDIA | NO ENCONTRADA |
| CF-L025 | LEGACY-FUNC-025 | Documentos comerciales | Consultar documentos comerciales | `modulos/mod_doccomerciales/listardoccomerciales.php` | MEDIA | PARCIAL |
| CF-L026 | LEGACY-FUNC-026 | Documentos comerciales | Registrar documentos comerciales | `modulos/mod_doccomerciales/registrardoccomercial.php` | MEDIA | NO ENCONTRADA |
| CF-L027 | LEGACY-FUNC-027 | Documentos comerciales | Modificar documentos comerciales | `modulos/mod_doccomerciales/modificardoccomercial.php` | MEDIA | NO ENCONTRADA |
| CF-L028 | LEGACY-FUNC-028 | Documentos comerciales | Eliminar documentos comerciales | `modulos/mod_doccomerciales/eliminardoccomercial.php` | MEDIA | NO ENCONTRADA |
| CF-L029 | LEGACY-FUNC-029 | Embalajes | Consultar embalajes | `modulos/mod_embalajes/listarembalajes.php` | MEDIA | CUBIERTA |
| CF-L030 | LEGACY-FUNC-030 | Embalajes | Registrar embalajes | `modulos/mod_embalajes/registrarembalaje.php` | MEDIA | CUBIERTA |
| CF-L031 | LEGACY-FUNC-031 | Embalajes | Modificar embalajes | `modulos/mod_embalajes/modificarembalaje.php` | MEDIA | CUBIERTA |
| CF-L032 | LEGACY-FUNC-032 | Embalajes | Eliminar embalajes | `modulos/mod_embalajes/eliminarembalaje.php` | MEDIA | COMPORTAMIENTO DIFERENTE |
| CF-L033 | LEGACY-FUNC-033 | Empresas de transporte | Consultar empresas de transporte | `modulos/mod_empresastransporte/listarempresastransporte.php` | MEDIA | CUBIERTA |
| CF-L034 | LEGACY-FUNC-034 | Empresas de transporte | Registrar empresas de transporte | `modulos/mod_empresastransporte/registrarempresatransporte.php` | MEDIA | CUBIERTA |
| CF-L035 | LEGACY-FUNC-035 | Empresas de transporte | Modificar empresas de transporte | `modulos/mod_empresastransporte/modificarempresatransporte.php` | MEDIA | CUBIERTA |
| CF-L036 | LEGACY-FUNC-036 | Empresas de transporte | Eliminar empresas de transporte | `modulos/mod_empresastransporte/eliminarempresatransporte.php` | MEDIA | CUBIERTA |
| CF-L037 | LEGACY-FUNC-037 | Modalidades | Consultar modalidades | `modulos/mod_modalidad/listarmodalidades.php` | MEDIA | PARCIAL |
| CF-L038 | LEGACY-FUNC-038 | Modalidades | Registrar modalidades | `modulos/mod_modalidad/registrarmodalidad.php` | MEDIA | NO ENCONTRADA |
| CF-L039 | LEGACY-FUNC-039 | Modalidades | Modificar modalidades | `modulos/mod_modalidad/modificarmodalidad.php` | MEDIA | NO ENCONTRADA |
| CF-L040 | LEGACY-FUNC-040 | Modalidades | Eliminar modalidades | `modulos/mod_modalidad/eliminarmodalidad.php` | MEDIA | NO ENCONTRADA |
| CF-L041 | LEGACY-FUNC-041 | Naturaleza de mercancía | Consultar naturaleza de mercancía | `modulos/mod_naturaleza/listarnaturalezas.php` | MEDIA | NO ENCONTRADA |
| CF-L042 | LEGACY-FUNC-042 | Naturaleza de mercancía | Registrar naturaleza de mercancía | `modulos/mod_naturaleza/registrarnaturaleza.php` | MEDIA | NO ENCONTRADA |
| CF-L043 | LEGACY-FUNC-043 | Naturaleza de mercancía | Modificar naturaleza de mercancía | `modulos/mod_naturaleza/modificarnaturaleza.php` | MEDIA | NO ENCONTRADA |
| CF-L044 | LEGACY-FUNC-044 | Naturaleza de mercancía | Eliminar naturaleza de mercancía | `modulos/mod_naturaleza/eliminarnaturaleza.php` | MEDIA | NO ENCONTRADA |
| CF-L045 | LEGACY-FUNC-045 | Personas | Consultar personas | `modulos/mod_personas/listarpersonas.php` | MEDIA | PARCIAL |
| CF-L046 | LEGACY-FUNC-046 | Personas | Registrar personas | `modulos/mod_personas/registrarpersona.php` | MEDIA | PARCIAL |
| CF-L047 | LEGACY-FUNC-047 | Personas | Modificar personas | `modulos/mod_personas/modificarpersona.php` | MEDIA | PARCIAL |
| CF-L048 | LEGACY-FUNC-048 | Personas | Eliminar personas | `modulos/mod_personas/eliminarpersona.php` | MEDIA | CUBIERTA |
| CF-L049 | LEGACY-FUNC-049 | Productos | Consultar productos | `modulos/mod_productos/listarproductos.php` | MEDIA | CUBIERTA |
| CF-L050 | LEGACY-FUNC-050 | Productos | Registrar productos | `modulos/mod_productos/registrarproducto.php` | MEDIA | CUBIERTA |
| CF-L051 | LEGACY-FUNC-051 | Productos | Modificar productos | `modulos/mod_productos/modificarproducto.php` | MEDIA | CUBIERTA |
| CF-L052 | LEGACY-FUNC-052 | Productos | Eliminar productos | `modulos/mod_productos/eliminarproducto.php` | MEDIA | CUBIERTA |
| CF-L053 | LEGACY-FUNC-053 | Resoluciones | Consultar resoluciones | `modulos/mod_resoluciones/listarresoluciones.php` | MEDIA | REEMPLAZADA |
| CF-L054 | LEGACY-FUNC-054 | Resoluciones | Registrar resoluciones | `modulos/mod_resoluciones/registrarresolucion.php` | MEDIA | REEMPLAZADA |
| CF-L055 | LEGACY-FUNC-055 | Resoluciones | Modificar resoluciones | `modulos/mod_resoluciones/modificarresolucion.php` | MEDIA | REEMPLAZADA |
| CF-L056 | LEGACY-FUNC-056 | Resoluciones | Eliminar resoluciones | `modulos/mod_resoluciones/eliminarresolucion.php` | MEDIA | REEMPLAZADA |
| CF-L057 | LEGACY-FUNC-057 | Servicios | Consultar servicios | `modulos/mod_servicios/listarservicios.php` | MEDIA | CUBIERTA |
| CF-L058 | LEGACY-FUNC-058 | Servicios | Registrar servicios | `modulos/mod_servicios/registrarservicio.php` | MEDIA | CUBIERTA |
| CF-L059 | LEGACY-FUNC-059 | Servicios | Modificar servicios | `modulos/mod_servicios/modificarservicio.php` | MEDIA | CUBIERTA |
| CF-L060 | LEGACY-FUNC-060 | Servicios | Eliminar servicios | `modulos/mod_servicios/eliminarservicio.php` | MEDIA | CUBIERTA |
| CF-L061 | LEGACY-FUNC-061 | SIA | Consultar sia | `modulos/mod_sias/listarsias.php` | MEDIA | CUBIERTA |
| CF-L062 | LEGACY-FUNC-062 | SIA | Registrar sia | `modulos/mod_sias/registrarsia.php` | MEDIA | CUBIERTA |
| CF-L063 | LEGACY-FUNC-063 | SIA | Modificar sia | `modulos/mod_sias/modificarsia.php` | MEDIA | CUBIERTA |
| CF-L064 | LEGACY-FUNC-064 | SIA | Eliminar sia | `modulos/mod_sias/eliminarsia.php` | MEDIA | CUBIERTA |
| CF-L073 | LEGACY-FUNC-073 | Tipos de bodega | Consultar tipos de bodega | `modulos/mod_tipobodegas/listartiposbodega.php` | MEDIA | NO ENCONTRADA |
| CF-L074 | LEGACY-FUNC-074 | Tipos de bodega | Registrar tipos de bodega | `modulos/mod_tipobodegas/registrartipobodega.php` | MEDIA | NO ENCONTRADA |
| CF-L075 | LEGACY-FUNC-075 | Tipos de bodega | Modificar tipos de bodega | `modulos/mod_tipobodegas/modificartipobodega.php` | MEDIA | NO ENCONTRADA |
| CF-L076 | LEGACY-FUNC-076 | Tipos de bodega | Eliminar tipos de bodega | `modulos/mod_tipobodegas/eliminartipobodega.php` | MEDIA | NO ENCONTRADA |
| CF-L077 | LEGACY-FUNC-077 | Unidades de carga | Consultar unidades de carga | `modulos/mod_unidadesdecarga/listarunidadesdecarga.php` | MEDIA | REEMPLAZADA |
| CF-L078 | LEGACY-FUNC-078 | Unidades de carga | Registrar unidades de carga | `modulos/mod_unidadesdecarga/registrarunidadcarga.php` | MEDIA | REEMPLAZADA |
| CF-L079 | LEGACY-FUNC-079 | Unidades de carga | Modificar unidades de carga | `modulos/mod_unidadesdecarga/modificarunidadcarga.php` | MEDIA | REEMPLAZADA |
| CF-L080 | LEGACY-FUNC-080 | Unidades de carga | Eliminar unidades de carga | `modulos/mod_unidadesdecarga/eliminarunidadcarga.php` | MEDIA | REEMPLAZADA |
| CF-L081 | LEGACY-FUNC-081 | Usuarios internos | Consultar usuarios internos | `modulos/mod_usuarios/listarusuarios.php` | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L082 | LEGACY-FUNC-082 | Usuarios internos | Registrar usuarios internos | `modulos/mod_usuarios/registrarusuario.php` | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L083 | LEGACY-FUNC-083 | Usuarios internos | Modificar usuarios internos | `modulos/mod_usuarios/modificarusuario.php` | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L084 | LEGACY-FUNC-084 | Usuarios internos | Eliminar usuarios internos | `modulos/mod_usuarios/eliminarusuario.php` | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L085 | LEGACY-FUNC-085 | Vehículos | Consultar vehículos | `modulos/mod_vehiculos/listarvehiculos.php` | MEDIA | CUBIERTA |
| CF-L086 | LEGACY-FUNC-086 | Vehículos | Registrar vehículos | `modulos/mod_vehiculos/registrarvehiculo.php` | MEDIA | PARCIAL |
| CF-L087 | LEGACY-FUNC-087 | Vehículos | Modificar vehículos | `modulos/mod_vehiculos/modificarvehiculo.php` | MEDIA | PARCIAL |
| CF-L088 | LEGACY-FUNC-088 | Vehículos | Eliminar vehículos | `modulos/mod_vehiculos/eliminarvehiculo.php` | MEDIA | CUBIERTA |
| CF-L089 | LEGACY-FUNC-089 | Bodegas | Consultar bodegas | `modulos/mod_bodegas/listarbodegas.php` | ALTA | PARCIAL |
| CF-L090 | LEGACY-FUNC-090 | Bodegas | Registrar bodegas | `modulos/mod_bodegas/registrarbodega.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L091 | LEGACY-FUNC-091 | Bodegas | Modificar bodegas | `modulos/mod_bodegas/modificarbodega.php` | ALTA | PARCIAL |
| CF-L092 | LEGACY-FUNC-092 | Bodegas | Eliminar bodegas | `modulos/mod_bodegas/eliminarbodega.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L093 | LEGACY-FUNC-093 | Documentos identidad | Registrar tipo de documento | `modulos/mod_configuracion/registrartipodocumento.php` | MEDIA | NO ENCONTRADA |
| CF-L094 | LEGACY-FUNC-094 | Documentos identidad | Eliminar tipo de documento | `modulos/mod_configuracion/eliminartipodocumento.php` | MEDIA | NO ENCONTRADA |
| CF-L095 | LEGACY-FUNC-095 | Prefijos | Consultar prefijos | `modulos/mod_prefijos/listarprefijos.php` | MEDIA | REEMPLAZADA |
| CF-L096 | LEGACY-FUNC-096 | Prefijos | Modificar prefijo | `modulos/mod_prefijos/modificarprefijo.php` | MEDIA | REEMPLAZADA |
| CF-L097 | LEGACY-FUNC-097 | Usuarios internos | Cambiar contraseña propia | `modulos/mod_usuarios/cambiarcontrasena.php` (+1) | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L098 | LEGACY-FUNC-098 | Usuarios internos | Gestionar permisos de usuario | `modulos/mod_usuarios/registrarusuario.php` (+1) | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L099 | LEGACY-FUNC-099 | Usuarios web | Gestionar usuarios del portal | `reportesweb/mod_usuarios/listarusuarios.php` (+5) | ALTA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L100 | LEGACY-FUNC-100 | Convenios | Asignar y desasignar vehículos a convenio | `modulos/mod_convenios/vehiculosasignados.php` (+2) | ALTA | NO ENCONTRADA |
| CF-L101 | LEGACY-FUNC-101 | Modalidades | Configurar requisitos de modalidad | `modulos/mod_modalidad/asignarrequisitos.php` | ALTA | PARCIAL |
| CF-L241 | LEGACY-FUNC-241 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de selecciones | `modulos/mod_selecciones/seleccionarcarroceria.php` (+8) | MEDIA | PARCIAL |
| CF-L242 | LEGACY-FUNC-242 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de clientes | `modulos/mod_clientes/seleccionarcliente.php` | MEDIA | CUBIERTA |
| CF-L243 | LEGACY-FUNC-243 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de personas | `modulos/mod_personas/consultarpersona.php` (+1) | MEDIA | CUBIERTA |
| CF-L244 | LEGACY-FUNC-244 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de productos | `modulos/mod_productos/selecciongrupo.php` | MEDIA | CUBIERTA |
| CF-L245 | LEGACY-FUNC-245 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de empresastransporte | `modulos/mod_empresastransporte/consultarempresatransporte.php` | MEDIA | CUBIERTA |
| CF-L246 | LEGACY-FUNC-246 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de usuarios | `modulos/mod_usuarios/consultacontrasena.php` | MEDIA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L247 | LEGACY-FUNC-247 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de vehiculos | `modulos/mod_vehiculos/consultarplaca.php` | MEDIA | CUBIERTA |
| CF-L248 | LEGACY-FUNC-248 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de unidadesdecarga | `modulos/mod_unidadesdecarga/consultarplaca.php` (+1) | MEDIA | PARCIAL |
| CF-L253 | LEGACY-FUNC-253 | Selectores y consultas auxiliares | Servir tablas paginadas AJAX | `includes/tablas/consultas-ajax.php` (+8) | MEDIA | CUBIERTA |
| CF-L256 | LEGACY-FUNC-256 | Imágenes de fichas | Cargar fotografía de ficha | `includes/subirfoto.php` | MEDIA | NO ENCONTRADA |

### 02-bascula — Báscula (pesajes, repesaje, cobros de báscula, tiquetes)

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L102 | LEGACY-FUNC-102 | Báscula | Consultar y filtrar entradas de báscula | `modulos/mod_bascula/listarentradasbascula.php` (+1) | ALTA | CUBIERTA |
| CF-L103 | LEGACY-FUNC-103 | Báscula | Registrar entrada y pesaje | `modulos/mod_bascula/registrarentradabascula.php` (+2) | ALTA | CUBIERTA |
| CF-L104 | LEGACY-FUNC-104 | Báscula | Modificar entrada y pesaje | `modulos/mod_bascula/modificarentrada.php` (+1) | ALTA | PARCIAL |
| CF-L105 | LEGACY-FUNC-105 | Báscula | Anular entrada | `modulos/mod_bascula/eliminarentrada.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L106 | LEGACY-FUNC-106 | Báscula | Consultar y filtrar salidas de báscula | `modulos/mod_bascula/listarsalidas.php` | ALTA | CUBIERTA |
| CF-L107 | LEGACY-FUNC-107 | Báscula | Registrar salida de báscula | `modulos/mod_bascula/registrarsalida.php` | ALTA | CUBIERTA |
| CF-L108 | LEGACY-FUNC-108 | Báscula | Modificar salida de báscula | `modulos/mod_bascula/modificarsalida.php` | ALTA | PARCIAL |
| CF-L109 | LEGACY-FUNC-109 | Báscula | Anular salida de báscula | `modulos/mod_bascula/eliminarsalida.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L110 | LEGACY-FUNC-110 | Báscula | Consultar solo pesajes | `modulos/mod_bascula/listarsolopesajes.php` | ALTA | CUBIERTA |
| CF-L111 | LEGACY-FUNC-111 | Báscula | Registrar solo pesaje | `modulos/mod_bascula/registrarsolopeso.php` | ALTA | CUBIERTA |
| CF-L112 | LEGACY-FUNC-112 | Báscula | Modificar solo pesaje | `modulos/mod_bascula/modificarsolopeso.php` | ALTA | PARCIAL |
| CF-L113 | LEGACY-FUNC-113 | Báscula | Anular solo pesaje | `modulos/mod_bascula/eliminarsolopeso.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L114 | LEGACY-FUNC-114 | Báscula | Registrar repesaje | `modulos/mod_bascula/repesarentrada.php` (+2) | ALTA | CUBIERTA |
| CF-L115 | LEGACY-FUNC-115 | Báscula | Ver tiquete y repesaje | `modulos/mod_bascula/vertiquete.php` (+1) | ALTA | CUBIERTA |
| CF-L116 | LEGACY-FUNC-116 | Báscula | Facturar servicios de báscula | `modulos/mod_bascula/facturar.php` (+1) | ALTA | REEMPLAZADA |
| CF-L117 | LEGACY-FUNC-117 | Báscula | Registrar factura SIIGO de tiquete | `modulos/mod_bascula/factusiigoticket.php` | ALTA | CUBIERTA |
| CF-L118 | LEGACY-FUNC-118 | Báscula | Cobrar cartera pendiente | `modulos/mod_bascula/cobrarcartera.php` (+1) | ALTA | CUBIERTA |
| CF-L119 | LEGACY-FUNC-119 | Báscula | Duplicar recibo | `modulos/mod_bascula/duplicarrecibo.php` | ALTA | NO ENCONTRADA |
| CF-L120 | LEGACY-FUNC-120 | Báscula | Usar tiquete existente | `modulos/mod_bascula/usartiquete.php` | ALTA | NO ENCONTRADA |
| CF-L121 | LEGACY-FUNC-121 | Báscula | Consultar reportes de báscula | `modulos/mod_bascula/inicioreportes.php` (+2) | MEDIA | PARCIAL |
| CF-L235 | LEGACY-FUNC-235 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de bascula | `modulos/mod_bascula/consultaentroplaca.php` (+10) | MEDIA | CUBIERTA |
| CF-L255 | LEGACY-FUNC-255 | Báscula | Consultar último peso | `peso.php` (+1) | MEDIA | CUBIERTA |

### 03-vigilancia-bodega — Vigilancia, portería y Bodega (ubicaciones, novedades, cargue, montacargas)

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L168 | LEGACY-FUNC-168 | Bodegas | Asignar productos a bodega | `modulos/mod_bodegas/asignarbodegaproducto.php` (+1) | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L169 | LEGACY-FUNC-169 | Bodegas | Asignar cantidades a bodega | `modulos/mod_bodegas/registrarbodegacantidad.php` (+2) | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L170 | LEGACY-FUNC-170 | Bodegas | Asignar vehículos a bodega | `modulos/mod_bodegas/asignarbodegacolmotores.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L171 | LEGACY-FUNC-171 | Bodegas | Gestionar secciones y posiciones | `modulos/mod_bodegas/seleccionarsecciones.php` (+12) | ALTA | PARCIAL |
| CF-L172 | LEGACY-FUNC-172 | Bodegas | Consultar ubicación y ocupación de bodega | `modulos/mod_bodegas/verbodega.php` (+4) | ALTA | PARCIAL |
| CF-L173 | LEGACY-FUNC-173 | Bodegas | Registrar observaciones y novedades | `modulos/mod_bodegas/asignarobservaciones.php` (+4) | ALTA | PARCIAL |
| CF-L174 | LEGACY-FUNC-174 | Bodegas | Modificar o eliminar observación/novedad | `modulos/mod_bodegas/modificarobservacion.php` (+3) | ALTA | NO ENCONTRADA |
| CF-L175 | LEGACY-FUNC-175 | Bodegas | Registrar avería de vehículo | `modulos/mod_bodegas/asignaraveriascolmotores.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L176 | LEGACY-FUNC-176 | Bodegas | Modificar o eliminar avería | `modulos/mod_bodegas/modificarveria.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L177 | LEGACY-FUNC-177 | Bodegas | Consultar e imprimir observación | `modulos/mod_bodegas/imprimirobservacion.php` | MEDIA | NO ENCONTRADA |
| CF-L178 | LEGACY-FUNC-178 | Bodegas | Gestionar fotografías de observación | `modulos/mod_bodegas/subirimagenes.php` (+1) | ALTA | PARCIAL |
| CF-L179 | LEGACY-FUNC-179 | Bodegas | Consultar órdenes de cargue | `modulos/mod_bodegas/listarcargues.php` | MEDIA | CUBIERTA |
| CF-L180 | LEGACY-FUNC-180 | Bodegas | Completar cargue | `modulos/mod_bodegas/completarcargue.php` | ALTA | CUBIERTA |
| CF-L230 | LEGACY-FUNC-230 | Portería | Registrar entrega por guía | `salidapuerta/index.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L236 | LEGACY-FUNC-236 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de bodegas | `modulos/mod_bodegas/seleccionarvin.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L254 | LEGACY-FUNC-254 | Selectores y consultas auxiliares | Cargar listas de bodega por filtro | `modulos/mod_bodegas/listadebodegas.php` (+1) | MEDIA | CUBIERTA |

### 04-ce-ingresos-depositos — Comercio Exterior: ingresos, depósitos, listas de empaque, etiquetas, prórroga y abandono

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L122 | LEGACY-FUNC-122 | Ingresos | Consultar y filtrar ingresos | `modulos/mod_ingresos/listaringresos.php` | ALTA | PARCIAL |
| CF-L123 | LEGACY-FUNC-123 | Ingresos | Registrar ingreso | `modulos/mod_ingresos/registraringreso.php` | ALTA | REEMPLAZADA |
| CF-L124 | LEGACY-FUNC-124 | Ingresos | Modificar ingreso | `modulos/mod_ingresos/modificaringreso.php` | ALTA | PARCIAL |
| CF-L125 | LEGACY-FUNC-125 | Ingresos | Anular ingreso | `modulos/mod_ingresos/eliminaringreso.php` | ALTA | PARCIAL |
| CF-L126 | LEGACY-FUNC-126 | Ingresos | Agregar productos amparados al ingreso | `modulos/mod_ingresos/gestionarproductos.php` | ALTA | REEMPLAZADA |
| CF-L127 | LEGACY-FUNC-127 | Ingresos | Modificar producto amparado | `modulos/mod_ingresos/modificargestionarproducto.php` | ALTA | REEMPLAZADA |
| CF-L128 | LEGACY-FUNC-128 | Ingresos | Eliminar producto amparado | `modulos/mod_ingresos/eliminargestionarproducto.php` | ALTA | REEMPLAZADA |
| CF-L129 | LEGACY-FUNC-129 | Listas de empaque | Consultar listas de empaque | `modulos/mod_listasempaque/listarlistas.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L130 | LEGACY-FUNC-130 | Listas de empaque | Importar lista de empaque | `modulos/mod_listasempaque/cargarlistasempaque.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L131 | LEGACY-FUNC-131 | Listas de empaque | Eliminar lista de empaque | `modulos/mod_listasempaque/eliminarlistaempaque.php` | ALTA | NO ENCONTRADA |
| CF-L132 | LEGACY-FUNC-132 | Listas de empaque | Asociar artículos de lista a ingreso | `modulos/mod_listasempaque/listararticulosactivos.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L133 | LEGACY-FUNC-133 | Depósitos | Consultar y filtrar depósitos de importación | `modulos/mod_depositos/listardepositos.php` (+3) | ALTA | CUBIERTA |
| CF-L134 | LEGACY-FUNC-134 | Depósitos | Consultar depósitos de exportación | `modulos/mod_depositos/listardepositosexp.php` | ALTA | CUBIERTA |
| CF-L135 | LEGACY-FUNC-135 | Depósitos | Registrar depósito | `modulos/mod_depositos/registrardeposito.php` (+1) | ALTA | REEMPLAZADA |
| CF-L136 | LEGACY-FUNC-136 | Depósitos | Modificar depósito | `modulos/mod_depositos/modificardeposito.php` | ALTA | PARCIAL |
| CF-L137 | LEGACY-FUNC-137 | Depósitos | Eliminar depósito | `modulos/mod_depositos/eliminardeposito.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L138 | LEGACY-FUNC-138 | Depósitos | Consultar detalle y seriales de producto | `modulos/mod_depositos/detalleproducto.php` | ALTA | PARCIAL |
| CF-L139 | LEGACY-FUNC-139 | Depósitos | Modificar serial de depósito | `modulos/mod_depositos/modificarserial.php` | ALTA | NO ENCONTRADA |
| CF-L140 | LEGACY-FUNC-140 | Depósitos | Consultar y registrar prórroga | `modulos/mod_depositos/listardepositosprorroga.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L141 | LEGACY-FUNC-141 | Depósitos | Generar y consultar adhesivos | `modulos/mod_depositos/adhesivos.php` (+4) | ALTA | PARCIAL |
| CF-L142 | LEGACY-FUNC-142 | Depósitos | Gestionar soportes de depósito | `modulos/mod_depositos/subirsoportes.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L237 | LEGACY-FUNC-237 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de depositos | `modulos/mod_depositos/seleccionarvinnoasociado.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L259 | LEGACY-FUNC-259 | Ingresos/depósitos | Conciliar VIN leídos al consultar listados | `modulos/mod_ingresos/listaringresos.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L260 | LEGACY-FUNC-260 | Depósitos | Reactivar depósito con saldo pendiente | `modulos/mod_depositos/listardepositos.php` | ALTA | REEMPLAZADA |

### 05-ce-levantes-salidas — Comercio Exterior: levantes, órdenes de cargue, salidas y guías

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L143 | LEGACY-FUNC-143 | Levantes | Consultar y filtrar levantes | `modulos/mod_levantes/listarlevantes.php` (+1) | ALTA | PARCIAL |
| CF-L144 | LEGACY-FUNC-144 | Levantes | Registrar levante | `modulos/mod_levantes/registrarlevante.php` (+1) | ALTA | PARCIAL |
| CF-L145 | LEGACY-FUNC-145 | Levantes | Modificar levante | `modulos/mod_levantes/modificarlevante.php` (+1) | ALTA | PARCIAL |
| CF-L146 | LEGACY-FUNC-146 | Levantes | Eliminar levante | `modulos/mod_levantes/eliminarlevante.php` | ALTA | NO ENCONTRADA |
| CF-L147 | LEGACY-FUNC-147 | Levantes | Asignar productos a levante | `modulos/mod_levantes/asignarproductos.php` (+2) | ALTA | REEMPLAZADA |
| CF-L148 | LEGACY-FUNC-148 | Levantes | Asignar VIN a levante | `modulos/mod_levantes/asignarvines.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L149 | LEGACY-FUNC-149 | Levantes | Quitar producto o VIN de levante | `modulos/mod_levantes/eliminarproductolevante.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L150 | LEGACY-FUNC-150 | Levantes | Gestionar soportes de levante | `modulos/mod_levantes/subirsoportes.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L151 | LEGACY-FUNC-151 | Salidas | Consultar y filtrar salidas de importación | `modulos/mod_salidas/listarsalidas.php` | ALTA | REEMPLAZADA |
| CF-L152 | LEGACY-FUNC-152 | Salidas | Consultar y filtrar salidas de exportación | `modulos/mod_salidas/listarsalidasexp.php` | ALTA | REEMPLAZADA |
| CF-L153 | LEGACY-FUNC-153 | Salidas | Elegir modalidad de nueva salida | `modulos/mod_salidas/nuevasalida.php` (+10) | BAJA | REEMPLAZADA |
| CF-L154 | LEGACY-FUNC-154 | Salidas | Registrar salida de importación | `modulos/mod_salidas/registrarsalida.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L155 | LEGACY-FUNC-155 | Salidas | Registrar salida de exportación | `modulos/mod_salidas/registrarsalidaexp.php` | ALTA | REEMPLAZADA |
| CF-L156 | LEGACY-FUNC-156 | Salidas | Registrar salida consolidada | `modulos/mod_salidas/registrarsalidaconsolidada.php` (+1) | ALTA | CUBIERTA |
| CF-L157 | LEGACY-FUNC-157 | Salidas | Registrar salida Colmotores | `modulos/mod_salidas/registrarsalidacolmotores.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L158 | LEGACY-FUNC-158 | Salidas | Modificar salida | `modulos/mod_salidas/modificarsalida.php` (+2) | ALTA | NO ENCONTRADA |
| CF-L159 | LEGACY-FUNC-159 | Salidas | Anular salida | `modulos/mod_salidas/eliminarsalida.php` | ALTA | PARCIAL |
| CF-L160 | LEGACY-FUNC-160 | Salidas | Asignar productos a salida | `modulos/mod_salidas/asignarproductos.php` (+2) | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L161 | LEGACY-FUNC-161 | Salidas | Asignar VIN a salida | `modulos/mod_salidas/asignarvines.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L162 | LEGACY-FUNC-162 | Salidas | Quitar producto o VIN de salida | `modulos/mod_salidas/eliminarproductosalida.php` (+1) | ALTA | NO ENCONTRADA |
| CF-L163 | LEGACY-FUNC-163 | Salidas | Generar y consultar guía de salida | `modulos/mod_salidas/verguia.php` (+1) | ALTA | PARCIAL |
| CF-L164 | LEGACY-FUNC-164 | Salidas | Autorizar orden de cargue | `modulos/mod_salidas/autorizarcargue.php` (+1) | ALTA | REEMPLAZADA |
| CF-L165 | LEGACY-FUNC-165 | Salidas | Consultar tiquete de salida | `modulos/mod_salidas/vertiquete.php` | ALTA | CUBIERTA |
| CF-L166 | LEGACY-FUNC-166 | Salidas | Consultar pesajes globales | `modulos/mod_salidas/listarpesajesglobal.php` | MEDIA | NO ENCONTRADA |
| CF-L167 | LEGACY-FUNC-167 | Salidas | Gestionar soportes de salida | `modulos/mod_salidas/subirsoportes.php` (+3) | ALTA | PARCIAL |
| CF-L238 | LEGACY-FUNC-238 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de levantes | `modulos/mod_levantes/seleccionardeposito.php` (+2) | MEDIA | CUBIERTA |
| CF-L239 | LEGACY-FUNC-239 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de salidas | `modulos/mod_salidas/seleccionarciudad.php` (+9) | MEDIA | CUBIERTA |
| CF-L261 | LEGACY-FUNC-261 | Salidas | Marcar salida sin mercancía como incompleta | `modulos/mod_salidas/listarsalidas.php` | ALTA | REEMPLAZADA |

### 06-facturacion — Facturación: convenios, tarifas, TRM, facturas, pagos, períodos (cron)

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L017 | LEGACY-FUNC-017 | Convenios | Consultar convenios | `modulos/mod_convenios/listarconvenios.php` | MEDIA | REEMPLAZADA |
| CF-L018 | LEGACY-FUNC-018 | Convenios | Registrar convenios | `modulos/mod_convenios/registrarconvenio.php` | MEDIA | REEMPLAZADA |
| CF-L019 | LEGACY-FUNC-019 | Convenios | Modificar convenios | `modulos/mod_convenios/modificarconvenio.php` | MEDIA | REEMPLAZADA |
| CF-L020 | LEGACY-FUNC-020 | Convenios | Eliminar convenios | `modulos/mod_convenios/eliminarconvenio.php` | MEDIA | REEMPLAZADA |
| CF-L065 | LEGACY-FUNC-065 | Tarifas | Consultar tarifas | `modulos/mod_tarifas/listartarifas.php` | MEDIA | REEMPLAZADA |
| CF-L066 | LEGACY-FUNC-066 | Tarifas | Registrar tarifas | `modulos/mod_tarifas/registrartarifa.php` | MEDIA | REEMPLAZADA |
| CF-L067 | LEGACY-FUNC-067 | Tarifas | Modificar tarifas | `modulos/mod_tarifas/modificartarifa.php` | MEDIA | REEMPLAZADA |
| CF-L068 | LEGACY-FUNC-068 | Tarifas | Eliminar tarifas | `modulos/mod_tarifas/eliminartarifa.php` | MEDIA | REEMPLAZADA |
| CF-L069 | LEGACY-FUNC-069 | Tasas de cambio | Consultar tasas de cambio | `modulos/mod_tasascambio/listartasascambio.php` | MEDIA | REEMPLAZADA |
| CF-L070 | LEGACY-FUNC-070 | Tasas de cambio | Registrar tasas de cambio | `modulos/mod_tasascambio/registrartasacambio.php` | MEDIA | REEMPLAZADA |
| CF-L071 | LEGACY-FUNC-071 | Tasas de cambio | Modificar tasas de cambio | `modulos/mod_tasascambio/modificartasacambio.php` | MEDIA | REEMPLAZADA |
| CF-L072 | LEGACY-FUNC-072 | Tasas de cambio | Eliminar tasas de cambio | `modulos/mod_tasascambio/eliminartasacambio.php` | MEDIA | REEMPLAZADA |
| CF-L201 | LEGACY-FUNC-201 | Facturación | Consultar depósitos por facturar | `modulos/mod_facturacion/listardepositosfacturar.php` (+1) | ALTA | PARCIAL |
| CF-L202 | LEGACY-FUNC-202 | Facturación | Facturar período en CIIGO | `modulos/mod_facturacion/facturarciigo.php` | ALTA | PARCIAL |
| CF-L203 | LEGACY-FUNC-203 | Facturación | Consultar facturas emitidas | `modulos/mod_facturacion/listarfacturas.php` | ALTA | CUBIERTA |
| CF-L204 | LEGACY-FUNC-204 | Facturación | Modificar factura | `modulos/mod_facturacion/modificarfactura.php` | ALTA | CUBIERTA |
| CF-L205 | LEGACY-FUNC-205 | Facturación | Anular factura | `modulos/mod_facturacion/eliminarfactura.php` | ALTA | COMPORTAMIENTO DIFERENTE |
| CF-L206 | LEGACY-FUNC-206 | Facturación | Consultar informe de facturación | `modulos/mod_facturacion/informefacturacion.php` | MEDIA | PARCIAL |
| CF-L207 | LEGACY-FUNC-207 | Facturación | Consultar informe por CPI | `modulos/mod_facturacion/informecpi.php` | MEDIA | PARCIAL |
| CF-L234 | LEGACY-FUNC-234 | Facturación programada | Recalcular períodos de facturación | `cron.php` | ALTA | PARCIAL |
| CF-L249 | LEGACY-FUNC-249 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de tasascambio | `modulos/mod_tasascambio/consultatasacambio.php` | MEDIA | REEMPLAZADA |
| CF-L251 | LEGACY-FUNC-251 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de facturacion | `modulos/mod_facturacion/seleccionardeposito.php` | MEDIA | CUBIERTA |

### 07-reportes-exportaciones — Reportes, kardex, inventarios, PDF y Excel

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L208 | LEGACY-FUNC-208 | Inventario y reportes | Abrir reportes de importación y exportación | `modulos/mod_inventario/inicioreportes.php` (+1) | BAJA | CUBIERTA |
| CF-L209 | LEGACY-FUNC-209 | Inventario y reportes | Consultar kardex de depósito | `modulos/mod_inventario/kardex.php` (+1) | MEDIA | PARCIAL |
| CF-L210 | LEGACY-FUNC-210 | Inventario y reportes | Consultar diarios de ingreso y salida | `modulos/mod_inventario/diario.php` (+4) | MEDIA | CUBIERTA |
| CF-L211 | LEGACY-FUNC-211 | Inventario y reportes | Consultar inventario general | `modulos/mod_inventario/reportegeneral.php` (+1) | MEDIA | PARCIAL |
| CF-L212 | LEGACY-FUNC-212 | Inventario y reportes | Consultar inventario de vehículos | `modulos/mod_inventario/reportegeneralvehiculos.php` (+4) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L213 | LEGACY-FUNC-213 | Inventario y reportes | Consultar mercancía nacionalizada y pendiente | `modulos/mod_inventario/reportenacionalizados.php` (+1) | MEDIA | COMPORTAMIENTO DIFERENTE |
| CF-L214 | LEGACY-FUNC-214 | Inventario y reportes | Consultar abandonos y prórrogas | `modulos/mod_inventario/reporteabandonos.php` (+1) | MEDIA | NO ENCONTRADA |
| CF-L215 | LEGACY-FUNC-215 | Inventario y reportes | Consultar pólizas | `modulos/mod_inventario/reportepoliza.php` (+1) | MEDIA | NO ENCONTRADA |
| CF-L216 | LEGACY-FUNC-216 | Inventario y reportes | Consultar ingresos por producto y cliente | `modulos/mod_inventario/reporteingresoproductocliente.php` | MEDIA | PARCIAL |
| CF-L229 | LEGACY-FUNC-229 | Portal de clientes | Consultar reportes SIA e ingreso | `reportesweb/reportesias.php` (+2) | MEDIA | NO ENCONTRADA |
| CF-L231 | LEGACY-FUNC-231 | Reportes y exportación | Generar PDF de reporte o etiqueta | `reportes/crearpdf.php` (+1) | BAJA | CUBIERTA |
| CF-L232 | LEGACY-FUNC-232 | Reportes y exportación | Descargar Excel de reporte | `reportes/reporteexcel.php` | BAJA | PARCIAL |
| CF-L233 | LEGACY-FUNC-233 | Reportes y exportación | Imprimir documentos y adhesivos | `reportes/imprimirdocumentos.php` (+1) | BAJA | PARCIAL |
| CF-L252 | LEGACY-FUNC-252 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de inventario | `modulos/mod_inventario/listarbodegas.php` | MEDIA | CUBIERTA |
| CF-L258 | LEGACY-FUNC-258 | Reportes y exportación | Generar código de barras de documentos | `includes/barcode/code128.php` (+1) | BAJA | CUBIERTA |

### 08-procesos-infra-fuera-alcance — Respaldos, migración legacy, notificaciones, ayuda y funciones excluidas (Colmotores, portal)

| ID | Legacy | Módulo legacy | Funcionalidad | Ruta legacy | Crit. | Estado previo |
| --- | --- | --- | --- | --- | --- | --- |
| CF-L004 | LEGACY-FUNC-004 | Navegación | Generar copia de seguridad | `menus/backup.php` | BAJA | REQUIERE VALIDACIÓN |
| CF-L181 | LEGACY-FUNC-181 | Colmotores | Consultar salidas de patio externo | `modulos/mod_colmotores/listarsalidas.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L182 | LEGACY-FUNC-182 | Colmotores | Registrar salida de patio externo | `modulos/mod_colmotores/registrarsalida.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L183 | LEGACY-FUNC-183 | Colmotores | Modificar salida de patio externo | `modulos/mod_colmotores/modificarsalida.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L184 | LEGACY-FUNC-184 | Colmotores | Asignar y quitar VIN de salida externa | `modulos/mod_colmotores/asignarvines.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L185 | LEGACY-FUNC-185 | Colmotores | Generar guía de patio externo | `modulos/mod_colmotores/verguia.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L186 | LEGACY-FUNC-186 | Colmotores | Importar y comparar archivo Colmotores | `modulos/mod_colmotores/comparacionarchivo.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L187 | LEGACY-FUNC-187 | Colmotores | Importar plano de voltajes | `modulos/mod_colmotores/subirvoltajes.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L188 | LEGACY-FUNC-188 | Colmotores | Registrar voltaje de vehículo | `modulos/mod_colmotores/registrarvoltaje.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L189 | LEGACY-FUNC-189 | Colmotores | Consultar y modificar voltajes | `modulos/mod_colmotores/listarvoltajescolmotores.php` (+5) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L190 | LEGACY-FUNC-190 | Colmotores | Gestionar observaciones externas | `modulos/mod_colmotores/modificarobservacion.php` (+2) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L191 | LEGACY-FUNC-191 | Colmotores | Gestionar soportes de salida externa | `modulos/mod_colmotores/subirsoportes.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L192 | LEGACY-FUNC-192 | Lectura de VIN | Leer VIN al ingreso | `modulos/mod_lecturas/inicio.php` (+2) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L193 | LEGACY-FUNC-193 | Lectura de VIN | Eliminar lectura de VIN | `modulos/mod_lecturas/eliminarvinlectura.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L194 | LEGACY-FUNC-194 | Lectura de VIN | Leer VIN en cargue | `modulos/mod_lecturas/leervinescargue.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L195 | LEGACY-FUNC-195 | Lectura de VIN | Quitar VIN de cargue | `modulos/mod_lecturas/eliminarvincargue.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L196 | LEGACY-FUNC-196 | Seriales Colmotores | Consultar menú y archivos de seriales | `modulos/mod_seriales/menucolmotores.php` (+2) | BAJA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L197 | LEGACY-FUNC-197 | Seriales Colmotores | Importar seriales de lista de empaque | `modulos/mod_seriales/leerseriales.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L198 | LEGACY-FUNC-198 | Seriales Colmotores | Cargar levantes Colmotores | `modulos/mod_seriales/cargarlevantescolmotores.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L199 | LEGACY-FUNC-199 | Seriales Colmotores | Cargar facturados Colmotores | `modulos/mod_seriales/cargarfacturados.php` (+1) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L200 | LEGACY-FUNC-200 | Seriales Colmotores | Eliminar archivo importado | `modulos/mod_seriales/eliminar_archivo.php` | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L217 | LEGACY-FUNC-217 | Portal de clientes | Iniciar y cerrar sesión de cliente | `reportesweb/index.php` (+3) | MEDIA | EXCLUIDA (Acceso, autenticación y roles (funcionalidad nueva de la v2)) |
| CF-L218 | LEGACY-FUNC-218 | Portal de clientes | Consultar almacenamiento | `reportesweb/almacenamiento.php` | BAJA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L219 | LEGACY-FUNC-219 | Portal de clientes | Consultar control de inventario | `reportesweb/controlinventario.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L220 | LEGACY-FUNC-220 | Portal de clientes | Consultar control y cumplimiento de entregas | `reportesweb/controlentregas.php` (+1) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L221 | LEGACY-FUNC-221 | Portal de clientes | Consultar inventario y desglose | `reportesweb/inventario.php` (+3) | ALTA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L222 | LEGACY-FUNC-222 | Portal de clientes | Consultar antigüedad de vehículos | `reportesweb/antiguedadvehiculos.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L223 | LEGACY-FUNC-223 | Portal de clientes | Consultar resumen de facturados | `reportesweb/resumenfacturados.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L224 | LEGACY-FUNC-224 | Portal de clientes | Consultar novedades y voltajes | `reportesweb/novedades.php` (+1) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L225 | LEGACY-FUNC-225 | Portal de clientes | Consultar promedio de almacenamiento | `reportesweb/promedioalmacenamiento.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L226 | LEGACY-FUNC-226 | Portal de clientes | Consultar ocupación y ubicación de vehículos | `reportesweb/reporteocupacionbodegas.php` (+4) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L227 | LEGACY-FUNC-227 | Portal de clientes | Consultar reporte por VIN | `reportesweb/reportevin.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L228 | LEGACY-FUNC-228 | Portal de clientes | Consultar reporte diario y descargue | `reportesweb/daily.php` (+1) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L240 | LEGACY-FUNC-240 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de colmotores | `modulos/mod_colmotores/consultarconductor.php` (+3) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L250 | LEGACY-FUNC-250 | Selectores y consultas auxiliares | Autocompletar y seleccionar datos de lecturas | `modulos/mod_lecturas/seleccionarplaca.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L257 | LEGACY-FUNC-257 | Portal de clientes | Autocompletar modelos, salidas y VIN | `reportesweb/consultamodelo.php` (+3) | MEDIA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L262 | LEGACY-FUNC-262 | Operación histórica | Migrar placas Colmotores a convenios | `migrarplacas.php` | BAJA | EXCLUIDA (Colmotores inhabilitado) |
| CF-L263 | LEGACY-FUNC-263 | Colmotores / exportación | Generar base comprimida de actualización Colmotores | `modulos/mod_colmotores/subiractualizacion.php` | MEDIA | EXCLUIDA (Colmotores inhabilitado) |

## 7. Capacidades V2 candidatas a `SOLO_V2`

Lista inicial del orquestador a partir de controladores, jobs y páginas. **Sin verificar**: cada agente la confirma o la corrige.

| ID | Módulo | Capacidad | Evidencia inicial |
| --- | --- | --- | --- |
| CF-V001 | 01 | Autenticación (login refresh logout) con JWT | `Backend/wms-api/Wms.Api/Controllers/v1/AuthController.cs; Frontend/wms/app/pages/auth/login.vue` |
| CF-V002 | 01 | Recuperación y cambio de contraseña | `Frontend/wms/app/pages/auth/request-password-reset.vue; reset-password.vue; change-password.vue` |
| CF-V003 | 01 | Usuarios con 6 roles y matriz de políticas | `Backend/wms-api/Wms.Api/Controllers/v1/UserController.cs; Wms.Domain/Security/WmsPolicyRoles.cs; Frontend/wms/app/pages/admin/users/` |
| CF-V004 | 01 | Auditoría genérica (audit_logs) y su consulta | `Frontend/wms/app/pages/admin/audit/index.vue` |
| CF-V005 | 01 | Parámetros del sistema | `Frontend/wms/app/pages/admin/parameters/index.vue` |
| CF-V006 | 01 | Catálogo de unidades de medida (DEC-015) | `Frontend/wms/app/pages/admin/unit-measures/index.vue` |
| CF-V007 | 01 | Catálogo de tipos de unidad de carga (DEC-014) | `Frontend/wms/app/pages/admin/cargo-unit-types/index.vue` |
| CF-V008 | 01 | Motivos de ingreso | `Backend/wms-api/Wms.Api/Controllers/v1/EntryReasonController.cs; Frontend/wms/app/pages/admin/entry-reasons/index.vue` |
| CF-V009 | 01 | Conductores con selector paginado y edición (DEC-017) | `Backend/wms-api/Wms.Api/Controllers/v1/DriverController.cs; Frontend/wms/app/pages/admin/drivers/index.vue` |
| CF-V010 | 01 | Terceros con varios roles y alta rápida | `Backend/wms-api/Wms.Api/Controllers/v1/StakeholderController.cs; Frontend/wms/app/pages/admin/stakeholders/` |
| CF-V011 | 01 | Panel de inicio por rol | `Frontend/wms/app/pages/index.vue; app/components/layout/AppMenu.vue` |
| CF-V020 | 02 | Cola de camiones de báscula | `Frontend/wms/app/pages/operations/weighbridge/index.vue` |
| CF-V021 | 02 | Recuperar operaciones de báscula a medias | `Frontend/wms/app/pages/operations/weighbridge/recover.vue` |
| CF-V022 | 02 | Pendientes de repesar y en proceso | `Frontend/wms/app/pages/operations/weighbridge/pending-reweigh.vue; in-process.vue` |
| CF-V023 | 02 | Tablero de báscula | `Frontend/wms/app/pages/operations/weighbridge/dashboard.vue` |
| CF-V024 | 02 | Corrección de ciclo de báscula | `Backend/wms-api/Wms.Api/Controllers/v1/WeighbridgeCorrectionController.cs` |
| CF-V025 | 02 | Flujo perecedero y depósito adicional en el mismo camión | `Backend/wms-api/Wms.Application/Weighbridge/` |
| CF-V030 | 03 | Vigilancia: registro de entrada y salida de vehículos | `Backend/wms-api/Wms.Api/Controllers/v1/EntryLogController.cs; Frontend/wms/app/pages/operations/entries/` |
| CF-V031 | 03 | Corrección de registros de Vigilancia | `Backend/wms-api/Wms.Api/Controllers/v1/EntryLogCorrectionController.cs` |
| CF-V032 | 03 | Recepción informativa en Bodega | `Frontend/wms/app/pages/warehouse/receptions/` |
| CF-V033 | 03 | Montacargas: uso y cobro con IVA opcional (DEC-018) | `Frontend/wms/app/pages/warehouse/forklift/; Backend/wms-api/Wms.Api/Controllers/v1/ForkliftRateController.cs` |
| CF-V034 | 03 | Trazabilidad por placa | `Frontend/wms/app/features/traceability/` |
| CF-V035 | 03 | Inventario de bodega | `Frontend/wms/app/pages/warehouse/inventory/index.vue` |
| CF-V040 | 04 | Unidades de carga en el depósito (DEC-014) | `Backend/wms-api/Wms.Application/ForeignTrade/` |
| CF-V041 | 04 | Inspecciones (INSP) | `Frontend/wms/app/pages/foreign-trade/inspections/` |
| CF-V042 | 04 | Cierre explícito del ingreso de camiones (DEC-013) | `Backend/wms-api/Wms.Api/Controllers/v1/DepositCompletionController.cs` |
| CF-V043 | 04 | Fecha de ingreso editable (DEC-012) | `Backend/wms-api/Wms.Api/Controllers/v1/DepositEntryDateController.cs` |
| CF-V044 | 04 | Ajuste de cantidad CE-7 con kárdex (DEC-019) | `Backend/wms-api/Wms.Api/Controllers/v1/InventoryAdjustmentController.cs` |
| CF-V045 | 04 | Exportaciones (EXP) como operación propia | `Frontend/wms/app/pages/foreign-trade/exports/` |
| CF-V050 | 05 | Autorización de salida | `Backend/wms-api/Wms.Api/Controllers/v1/DepartureAuthorizationController.cs` |
| CF-V051 | 05 | Correcciones de orden de cargue | `Backend/wms-api/Wms.Api/Controllers/v1/LoadingOrderCorrectionsController.cs` |
| CF-V052 | 05 | Guías pendientes | `Frontend/wms/app/pages/foreign-trade/dispatch-guides/pending.vue` |
| CF-V053 | 05 | Salida de la orden de cargue | `Backend/wms-api/Wms.Api/Controllers/v1/LoadingOrderExitController.cs` |
| CF-V060 | 06 | Motor de acuerdos y fórmulas de tarifa | `Backend/wms-api/Wms.Application/Billing/; Wms.Application/Agreements/` |
| CF-V061 | 06 | Ciclos de facturación configurables | `Backend/wms-api/Wms.Api/Controllers/v1/BillingCyclesController.cs; Frontend/wms/app/pages/billing/configurations/` |
| CF-V062 | 06 | Pagos y conciliación automática | `Frontend/wms/app/pages/billing/payments/; Wms.Api/BackgroundJobs/InvoicePaymentReconciliationBackgroundService.cs` |
| CF-V063 | 06 | Detección de mora | `Wms.Api/BackgroundJobs/OverdueDetectionBackgroundService.cs` |
| CF-V064 | 06 | Aviso de vencimiento de facturas | `Wms.Api/BackgroundJobs/InvoiceDueNotificationBackgroundService.cs` |
| CF-V065 | 06 | Reexpedición de factura | `Backend/wms-api/Wms.Api/Controllers/v1/InvoiceReissueController.cs` |
| CF-V066 | 06 | TRM desde la DIAN al crear la factura (DEC-023) | `Backend/wms-api/Wms.Application/Billing/` |
| CF-V067 | 06 | Cierre automático de períodos de almacenamiento | `Wms.Api/BackgroundJobs/StoragePeriodAutoCloseBackgroundService.cs` |
| CF-V070 | 07 | Estadísticas | `Frontend/wms/app/pages/reports/statistics.vue` |
| CF-V071 | 07 | Movimientos de bodega | `Backend/wms-api/Wms.Api/Controllers/v1/WarehouseMovementsReportController.cs` |
| CF-V080 | 08 | Respaldos con destinos configurables (P14) | `Backend/wms-api/Wms.Api/Controllers/v1/BackupsController.cs; Wms.Api/BackgroundJobs/DatabaseBackupBackgroundService.cs` |
| CF-V081 | 08 | Importación legacy por CSV con simulación y conciliación | `Backend/wms-api/Wms.Api/Controllers/v1/LegacyImportController.cs` |
| CF-V082 | 08 | Notificaciones en tiempo real | `Frontend/wms/app/pages/notifications/index.vue` |
| CF-V083 | 08 | Centro de ayuda con videos | `Frontend/wms/app/pages/ayuda/` |
| CF-V084 | 04 | Alerta diaria de abandono (job) | `Wms.Api/BackgroundJobs/AbandonmentAlertBackgroundService.cs` |
| CF-V085 | 08 | Estado del sistema | `Backend/wms-api/Wms.Api/Controllers/v1/SystemController.cs` |

El inventario en CSV está en `01-inventario-funcional-global.csv`. Las altas que hagan los agentes (desgloses, capacidades no catalogadas, `SOLO_V2` nuevas) quedan en sus matrices y en `03-matriz-global.md`.
