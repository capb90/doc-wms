# 01 — Inventario legacy · 01-administracion-catalogos

> **Fecha:** 2026-10-23. Lectura estática de `bodegas-legacy/` (no se abrió `Connections/` ni `db_legacy/`). Rutas relativas a `code_workspace/`.
> **Alcance:** 98 capacidades asignadas más 2 no catalogadas (`CF-LX01-01`, `CF-LX01-02`). La evidencia por línea está en `06-matriz-paridad.md`; aquí va la estructura.

## 1. Mecanismos comunes del legacy

| Mecanismo | Qué hace | Evidencia |
| --- | --- | --- |
| Sesión | Toda página interna incluye `aut_verifica.inc.php`: con `user`/`pass` autentica (MD5, `usuario.estado<>'eliminado'`); sin ellos exige las claves de sesión | `bodegas-legacy/aut_verifica.inc.php:16-27,97-130` |
| Permiso por usuario | `$modulo` + `$accion` al inicio de cada página y `evaluaPermiso()` contra la tabla `permisos`; sin permiso redirige con error 5 (sin `exit`) | `bodegas-legacy/verificapermisos.php:33-48`; p. ej. `bodegas-legacy/modulos/mod_ciudades/listarciudades.php:6-8` |
| Menú por nivel | «Configuraciones» (usuarios, cuadrillas, documentos, servicios, modalidades, naturaleza, resoluciones, tipos de bodega, bodegas, productos, ciudades, prefijos) solo para nivel ≤ 1 | `bodegas-legacy/menus/menuizquierda.php:283-302` |
| Baja lógica | `UPDATE … estado='eliminado'` y listados con `estado='activo'` o `<>'eliminado'` (RN-010) | p. ej. `bodegas-legacy/modulos/mod_clientes/eliminarcliente.php:56` |
| Bloqueo por registros asociados | `ComprobarRelacion()` cuenta filas no eliminadas en tablas hijas; si hay, redirige con error 8 «No puede eliminar el registro porque tiene otros registros asociados» (sin `exit`) | `bodegas-legacy/includes/funciones.php:18-34`; `bodegas-legacy/aut_mensaje_error.inc.php:17`; usos en `eliminarcliente.php:20`, `eliminarpersona.php:20`, `eliminarvehiculo.php:20`, `eliminarempresatransporte.php:20`, `eliminarcuadrilla.php:19`, `eliminarunidadcarga.php:20`, `eliminardoccomercial.php:19`, `eliminarnaturaleza.php:20`, `eliminarmodalidad.php:19` |
| Duplicados | Solo en JavaScript: al digitar el documento o la placa se consulta por AJAX y se alerta; el esquema no tiene índices únicos en maestros (solo `usuario.usuario`, `modulo.nom_modulo`) | `bodegas-legacy/modulos/mod_clientes/registrarcliente.php:334-343`; `bodegas-legacy/modulos/mod_vehiculos/registrarvehiculo.php:159-176`; `bodegas-legacy/bodegas_schema.sql:1674,1698,728` |
| Validación de formulario | Spry (requeridos, enteros, longitudes) | p. ej. `bodegas-legacy/modulos/mod_ciudades/registrarciudad.php:230-233` |
| Autoría | `id_usuarioregistra`, `ip_registra`, `fechahora_registra` en la fila | p. ej. `bodegas-legacy/modulos/mod_cuadrillas/registrarcuadrilla.php:57` |

## 2. Capacidades por catálogo

| Catálogo | IDs | Pantallas / scripts | Tablas | Permiso (`módulo`) | Baja |
| --- | --- | --- | --- | --- | --- |
| Acceso | CF-L001, 002 | `index.php`, `entrada.php`, `aut_verifica.inc.php`, `aut_logout.php` | `usuario`, `auditoria` | sesión | — |
| Panel y alertas | CF-L003 | `inicial.php`, `menus/menuizquierda.php`, `menus/evaluaabandonos.php`, `menus/evaluatasacambio.php` | `vista_kardexdepositos`, `tasa_cambio` | sesión; alertas solo nivel ≤ 1 | — |
| Ciudades/destinos | CF-L005…008 | `modulos/mod_ciudades/{listar,registrar,modificar,eliminar}ciudad(es).php` | `ciudad`, `pais` | `ciudades` | **Física** (`DELETE`) |
| Clientes | CF-L009…012 | `modulos/mod_clientes/*` | `cliente`, `representar`, `tipodocumento`, `ciudad` | `clientes` | Lógica + bloqueo (convenio, factura, recibo, representar) |
| Color de vehículo | CF-L013…016 | `modulos/mod_colorvehiculo/*` (menú Colmotores) | `colorvehiculo` | `seriales` | Física |
| Cuadrillas | CF-L021…024 | `modulos/mod_cuadrillas/*` | `cuadrilla` | `cuadrillas` (alta y edición piden `eliminar`) | Lógica + bloqueo (pesaje, cuadrilla_x_modalidad) |
| Documentos comerciales | CF-L025…028 | `modulos/mod_doccomerciales/*` | `documentocomercial` | `doccomerciales` (alta y edición piden `eliminar`) | Lógica + bloqueo (ingreso, docmercial_x_modalidad) |
| Embalajes | CF-L029…032 | `modulos/mod_embalajes/*` | `embalaje` | `embalajes` | Lógica |
| Empresas de transporte | CF-L033…036 | `modulos/mod_empresastransporte/*` | `empresa_transporte`, `tipodocumento`, `ciudad` | `empresastransporte` | Lógica + bloqueo (vehiculo_x_empresa) |
| Modalidades | CF-L037…040, 101 | `modulos/mod_modalidad/*`, `asignarrequisitos.php` | `modalidad`, `docmercial_x_modalidad` | `modalidades` | Lógica + bloqueo (pesaje) |
| Naturaleza de mercancía | CF-L041…044 | `modulos/mod_naturaleza/*` | `naturalezamercancia` | `naturalezas` (edición pide `servicios`) | Lógica + bloqueo (producto_en_bodega) |
| Personas | CF-L045…048 | `modulos/mod_personas/*`, `listarpersonasajax.php` | `persona`, `ocupacion` | `personas` | Lógica + bloqueo (pesaje conductor/auxiliar, representar) |
| Productos | CF-L049…052 | `modulos/mod_productos/*` | `producto`, `embalaje`, `grupoaliasvehiculos` | `productos` | Lógica |
| Resoluciones | CF-L053…056 | `modulos/mod_resoluciones/*` | `resolucion_numeracion`, `tipofacturacion` | `resoluciones` (edición y baja piden `consultar`) | Lógica |
| Servicios | CF-L057…060 | `modulos/mod_servicios/*` | `servicio` | `servicios` | Lógica |
| SIA (agencia de aduanas) | CF-L061…064 | `modulos/mod_sias/*` | `sia` | `sias` | Lógica |
| Tipos de bodega | CF-L073…076 | `modulos/mod_tipobodegas/*` | `tipobodega` | `tiposbodega` | Lógica |
| Unidades de carga | CF-L077…080 | `modulos/mod_unidadesdecarga/*` | `unidadcarga`, `claseunidadcarga` | `unidadesdecarga` (edición pide `registrar`) | Lógica + bloqueo (pesaje) |
| Usuarios internos | CF-L081…084, 097, 098 | `modulos/mod_usuarios/*` | `usuario`, `permisos`, `modulo`, `nivel_acceso` | `usuarios` | Lógica |
| Usuarios del portal | CF-L099 | `reportesweb/mod_usuarios/*` | `usuariocliente`, `sia` | `usuarios` | Lógica |
| Vehículos | CF-L085…088 | `modulos/mod_vehiculos/*` | `vehiculo`, `vehiculo_x_convenio`, `vehiculo_x_empresa`, marca/línea/clase/carrocería | `vehiculos` | Lógica + bloqueo (convenio, empresa, pesaje) |
| Bodegas | CF-L089…092 | `modulos/mod_bodegas/{listar,registrar,modificar,eliminar}bodega(s).php` | `bodega`, `seccion`, `tipobodega` | `bodegas` | Lógica de bodega y secciones, sin bloqueo |
| Tipos de documento | CF-L093, 094 | `modulos/mod_configuracion/*` | `tipodocumento` | `configuraciones` | Lógica |
| Prefijos | CF-L095, 096 | `modulos/mod_prefijos/*`, `includes/cargaprefijos.php` | `campoprefijo` | `prefijos` (edición pide `eliminar`) | — |
| Vehículos a convenio | CF-L100 | `modulos/mod_convenios/{vehiculosasignados,asignarvehiculo,desasignarvehiculo}.php` | `vehiculo_x_convenio` | `convenios` | Física (`DELETE`) |
| Selectores | CF-L241…248 | `mod_selecciones/*`, `mod_clientes/seleccionarcliente.php`, `mod_personas/consultarpersona.php`, `mod_productos/selecciongrupo.php`, `mod_empresastransporte/consultarempresatransporte.php`, `mod_usuarios/consultacontrasena.php`, `mod_vehiculos/consultarplaca.php`, `mod_unidadesdecarga/{consultarplaca,seleccionarmarcaunidadcarga}.php` | varias | **sin** `evaluaPermiso` (solo conexión) | — |
| Tablas AJAX | CF-L253 | `includes/tablas/{consultas,tablas}-ajax.php` (y copias en `mod_bodegas/tablas`, `reportesweb/tablas`), `mod_personas/listarpersonasajax.php` | la que llegue por GET | **ninguno**: no incluyen `aut_verifica` | — |
| Foto de ficha | CF-L256 | `includes/subirfoto.php` | archivos en `tmp/` y `fotos/` | — | — |

## 3. Capacidades no catalogadas

| ID | Capacidad | Evidencia | Nota |
| --- | --- | --- | --- |
| CF-LX01-01 | Registrar auditoría de inicio de sesión (`auditoria`, acción «ENTRADA») | `bodegas-legacy/aut_verifica.inc.php:97-99`; `bodegas-legacy/bodegas_schema.sql:60-71` | El catálogo la menciona dentro de LEGACY-FUNC-001, sin ficha propia |
| CF-LX01-02 | Registrar auditoría de acciones sobre maestros (`InsertAuditoria`) | `bodegas-legacy/verificapermisos.php:49-53`; único llamador `bodegas-legacy/modulos/mod_clientes/registrarcliente.php:107` | El SQL (`INSERT INTO auditoria AS A, modulo AS M … WHERE`) no es válido; el resultado no se comprueba. No hay pantalla de consulta |

No se encontraron otras: `mod_configuracion` solo tiene tipos de documento; países (`pais`), clases de unidad (`claseunidadcarga`) y ocupaciones (`ocupacion`) se leen pero no tienen pantalla de administración.

## 4. Anomalías observadas (no son requisitos)

- Permisos mal asignados: `mod_cuadrillas/registrarcuadrilla.php:8-9` y `modificarcuadrillas.php:8-9` piden `eliminar`; `mod_doccomerciales/registrardoccomercial.php:8-9` y `modificardoccomercial.php:8-9`, también; `mod_naturaleza/modificarnaturaleza.php:8` usa el módulo `servicios`; `mod_resoluciones/modificarresolucion.php:9` y `eliminarresolucion.php:9` piden `consultar`; `mod_prefijos/modificarprefijo.php:9` pide `eliminar`; `mod_unidadesdecarga/modificarunidadcarga.php:9` pide `registrar`.
- Sentencias con menos valores que columnas: `mod_servicios/registrarservicio.php:59` (7 columnas, 6 `%s`) y `mod_modalidad/registrarmodalidad.php:57` (6 y 5): fallarían al ejecutarse.
- Redirecciones sin `exit` en `evaluaPermiso` y en el bloqueo de error 8: la página sigue y un POST directo ejecuta la acción.
- Los endpoints de tablas AJAX construyen SQL con tabla, columnas y `where` del GET y sin sesión (`includes/tablas/consultas-ajax.php:5-13`).
- La auditoría por acción (`InsertAuditoria`) no funciona (§3).
