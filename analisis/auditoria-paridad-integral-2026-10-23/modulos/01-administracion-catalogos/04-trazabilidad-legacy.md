# 04 — Trazabilidad legacy · 01-administracion-catalogos

> **Fecha:** 2026-10-23. L = lectura, E = escritura. Rutas bajo `bodegas-legacy/modulos/` salvo que se indique otra. Líneas en `06-matriz-paridad.md`.

| Capacidad | Ruta → script | Tablas y campos |
| --- | --- | --- |
| CF-L001 | `index.php` → `entrada.php` → `aut_verifica.inc.php` | L `usuario`(id_usuario, usuario, pass, nivel_acceso, estado); E `auditoria`(id_modulo=1, id_usuarioregistra, ip_registra, fechahora, accion='ENTRADA') |
| CF-L002 | `aut_logout.php` | — (sesión) |
| CF-L003 | `inicial.php`, `menus/menuizquierda.php`, `menus/evaluaabandonos.php`, `menus/evaluatasacambio.php` | L `vista_kardexdepositos`(ingresan, nacionalizados, fecha_deposito, prorroga); L `tasa_cambio`(fecha_inicio, fecha_fin) |
| CF-L005…008 | `mod_ciudades/listarciudades.php`, `registrarciudad.php`, `modificarciudad.php`, `eliminarciudad.php` | L `pais`; L/E `ciudad`(id_ciudad, nom_ciudad, id_pais, distrito, dias); `DELETE` físico |
| CF-L009…012, 242 | `mod_clientes/listarclientes.php`, `registrarcliente.php`, `modificarcliente.php`, `eliminarcliente.php`, `seleccionarcliente.php` | L/E `cliente`(id_tipodocumento, nro_documento, digitoverificacion, id_paisdocumento, nom_cliente, dir_cliente, tel_cliente, tel2_cliente, id_ciudad, contacto_cliente, dias_facturacion, uap, foto, thumb, estado); L/E `representar`(id_cliente, id_persona, participacion); L `tipodocumento`, `ciudad`; L `convenio`, `factura`, `recibo` (bloqueo) |
| CF-L013…016 | `mod_colorvehiculo/*` | L/E `colorvehiculo`(idcolor, nombrecolor); `DELETE` físico |
| CF-L021…024 | `mod_cuadrillas/*` | L/E `cuadrilla`(nom_cuadrilla, estado); L `pesaje`, `cuadrilla_x_modalidad` (bloqueo) |
| CF-L025…028 | `mod_doccomerciales/*` | L/E `documentocomercial`(nom_documentocomercial, estado); L `ingreso`, `docmercial_x_modalidad` (bloqueo) |
| CF-L029…032 | `mod_embalajes/*` | L/E `embalaje`(nom_embalaje, estado) |
| CF-L033…036, 245 | `mod_empresastransporte/*`, `consultarempresatransporte.php` | L/E `empresa_transporte`(nro_documento, id_tipodocumento, id_paisdocumento, nom_empresatransporte, sigla, email, tel, dir, id_ciudad, estado); L `vehiculo_x_empresa` (bloqueo) |
| CF-L037…040, 101 | `mod_modalidad/*`, `asignarrequisitos.php`; consumido por `mod_bascula/consultatipodocumento.php` | L/E `modalidad`(nom_modalidad, numerar_tiket, estado); E `docmercial_x_modalidad`(id_documentocomercial, id_modalidad, requisito, prioridad) con `DELETE` previo; L `pesaje` (bloqueo) |
| CF-L041…044 | `mod_naturaleza/*` | L/E `naturalezamercancia`(nom_naturalezamercancia, estado); L `producto_en_bodega` (bloqueo) |
| CF-L045…048, 243, 253 | `mod_personas/*`, `listarpersonasajax.php`, `consultarpersona.php` | L/E `persona`(documento_persona, id_tipodocumento, id_paisdocumento, nombres, apellidos, licenciaconduccion, email, telefono, direccion, id_ciudadpersona, id_ocupacion, foto, estado); L `ocupacion`, `pais`, `ciudad`; L `pesaje`(id_conductor, id_conductorauxiliar), `representar` (bloqueo) |
| CF-L049…052, 244, 253 | `mod_productos/*`, `selecciongrupo.php`, `includes/tablas/tablas-ajax.php` | L/E `producto`(aliasproducto, descripcionproducto, id_embalaje, estado); E `grupoaliasvehiculos`(alias, grupo) |
| CF-L053…056 | `mod_resoluciones/*`; consumido por `mod_bascula/facturar1.php:356-363` | L/E `resolucion_numeracion`(id_servicio, id_tipofacturacion, nro_inicial, nro_final, fecha_inicio, fecha_fin, desc_resolucion, estado); L `tipofacturacion`, `servicio` |
| CF-L057…060 | `mod_servicios/*` | L/E `servicio`(codigo_servicio, nom_servicio, detalle_servicio, estado) |
| CF-L061…064 | `mod_sias/*` | L/E `sia`(id_tipodocumento, nro_documento, id_paisdocumento, nombre_sia, direccion, telefono, id_ciudad, personacontacto, estado) |
| CF-L073…076 | `mod_tipobodegas/*` | L/E `tipobodega`(nom_tipobodega, sigla_bodega, estado) |
| CF-L077…080, 248 | `mod_unidadesdecarga/*`, `consultarplaca.php`, `seleccionarmarcaunidadcarga.php` | L/E `unidadcarga`(placa, id_pais, nro_chasis, modelo, marca, id_claseunidadcarga, foto, estado); L `claseunidadcarga`; L `pesaje` (bloqueo) |
| CF-L081…084, 097, 098, 246 | `mod_usuarios/*`, `cambiarcontrasena.php`, `consultacontrasena.php` | L/E `usuario`(nomape, identificacion, telefono, tipo_acceso, usuario, pass MD5, nivel_acceso, foto, estado); L/E `permisos`(id_modulo, id_usuario, consultar, registrar, editar, eliminar); L `modulo`, `nivel_acceso` |
| CF-L099 | `reportesweb/mod_usuarios/*` | L/E `usuariocliente`(id_sia, nomape, tipo_acceso, usuario, pass, nivel_acceso, estado); L `sia` |
| CF-L085…088, 247 | `mod_vehiculos/*`, `consultarplaca.php` | L/E `vehiculo`(placa_vehiculo, id_paisplaca, nro_motor, nro_chasis, modelo, id_clasevehiculo, id_tipocarroceria, id_marcavehiculo, id_lineavehiculo, foto, estado); E `vehiculo_x_convenio`(id_convenio=0); L `marcavehiculo`, `lineavehiculo`, `clasevehiculo`, `tipocarroceria`; L `vehiculo_x_empresa`, `pesaje` (bloqueo) |
| CF-L089…092 | `mod_bodegas/listarbodegas.php`, `registrarbodega.php`, `modificarbodega.php`, `eliminarbodega.php` | L/E `bodega`(nom_bodega, id_tipobodega, observaciones, filas, columnas, uso, estado); E `seccion`(nombre '[f][c]', ocupacion='libre', fila, columna, id_bodega, estado); L `tipobodega` |
| CF-L093, 094 | `mod_configuracion/registrartipodocumento.php`, `eliminartipodocumento.php` | L/E `tipodocumento`(id_tipodocumento, nom_tipodocumento, estado) |
| CF-L095, 096 | `mod_prefijos/*`; consumido por `includes/cargaprefijos.php` | L/E `campoprefijo`(nom_campoprefijo, prefijo, estado) |
| CF-L100 | `mod_convenios/vehiculosasignados.php`, `asignarvehiculo.php`, `desasignarvehiculo.php` | L/E `vehiculo_x_convenio`(id_vehiculo, id_convenio); `DELETE` físico; L `convenio`, `vehiculo`, marca, carrocería |
| CF-L241 | `mod_selecciones/seleccionar{carroceria,ciudad,deposito,lineavehiculo,marcavehiculo,ocupacion,pais,placa,tiquete}.php` | L `tipocarroceria`, `ciudad`, `deposito`+`ingreso`+`cliente`, `lineavehiculo`, `marcavehiculo`, `ocupacion`, `pais`, `vehiculo`, `pesaje`+`factura` |
| CF-L253 | `includes/tablas/consultas-ajax.php`, `tablas-ajax.php` (y copias) | L cualquier tabla indicada por GET |
| CF-L256 | `includes/subirfoto.php` | Archivos `tmp/foto_*`, `tmp/thumb_*`; las altas los copian a `fotos/` |
| CF-LX01-01 | `aut_verifica.inc.php:97-99` | E `auditoria` |
| CF-LX01-02 | `verificapermisos.php:49-53` (desde `registrarcliente.php:107`) | E `auditoria` (SQL inválido) |
