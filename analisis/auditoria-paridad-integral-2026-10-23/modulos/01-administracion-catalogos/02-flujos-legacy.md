# 02 — Flujos legacy · 01-administracion-catalogos

> **Fecha:** 2026-10-23. Reconstruidos leyendo el PHP; no se ejecutó el legacy. Rutas relativas a `code_workspace/`.

## F-01 · Inicio y cierre de sesión (CF-L001, CF-L002, CF-LX01-01)

1. `bodegas-legacy/index.php:18-36` envía `user` y `pass` a `entrada.php`, que incluye `aut_verifica.inc.php`.
2. `aut_verifica.inc.php:27` busca el usuario no eliminado; compara usuario y `md5(pass)`; si falla, vuelve con `error_login` 2, 3 o 4 (`:113`).
3. Crea la sesión (id, nivel, login, hash) e inserta `auditoria` con «ENTRADA» (`:97-99`).
4. Nivel 3 (vigilante) va a `salidapuerta/index.php`; los demás, al marco principal (`:101-105`).
5. `aut_logout.php:10-16` destruye la sesión y vuelve a `index.php`.

**Persistencia:** `auditoria` (una fila por ingreso). **Incertidumbre:** el referidor HTTP vacío redirige al inicio (`:10-13`); no se sabe si se usaba la sesión en paralelo.

## F-02 · Panel y alertas (CF-L003)

1. `inicial.php:78`: solo para nivel ≤ 1 ejecuta `evaluaTasa()` y `evaluaAbandonos()` al cargar.
2. `menus/evaluatasacambio.php:6` busca una `tasa_cambio` vigente hoy; si no hay, el menú muestra «ALERTA! La tasa de cambio está desactualizada» y lleva a tasas (`menus/menuizquierda.php:149-166`, repetido cada segundo).
3. `menus/evaluaabandonos.php:6-14` cuenta depósitos con mercancía sin nacionalizar en 20–30 días (sin prórroga) o 50–60 (con prórroga) y resalta «Prorrogas» (`menuizquierda.php:169-182`).
4. El panel ofrece accesos rápidos a báscula, ingresos, depósitos, levantes, salidas, clientes, tarifas, convenios, usuarios y cambio de contraseña (`inicial.php:92-152`).

**Efectos:** ninguno en base de datos.

## F-03 · CRUD de catálogo simple (patrón común)

Aplica a ciudades, cuadrillas, documentos comerciales, embalajes, modalidades, naturaleza, resoluciones, servicios, tipos de bodega y prefijos.

1. `listar*.php`: verifica `módulo:consultar`, consulta la tabla con `estado='activo'` o `<>'eliminado'` (ciudades no filtra: no tiene estado) y pinta una tabla DataTables en el navegador.
2. `registrar*.php`: Spry valida en el cliente; el POST inserta con `id_usuarioregistra`, IP y fecha. No hay control de duplicados en el servidor.
3. `modificar*.php`: `UPDATE` por id.
4. `eliminar*.php`: muestra la ficha; con el POST hace `UPDATE estado='eliminado'` (baja lógica). Ciudades y colores hacen `DELETE` (RN-011). En cuadrillas, documentos, naturaleza y modalidades, antes valida `ComprobarRelacion()` (error 8).

**Incertidumbres:** las anomalías de permisos y de sentencias (01-inventario-legacy.md §4) hacen dudar de que algunas altas funcionaran en producción (servicios, modalidades).

## F-04 · Clientes, SIA y empresas de transporte (CF-L009…012, 033…036, 061…064, 242, 245)

1. En el alta, al salir del documento, JavaScript consulta `seleccionarcliente.php` (o `consultarempresatransporte.php`) por tipo y número; si existe, avisa «REGISTRO EXISTENTE» y limpia el tipo (`registrarcliente.php:334-343`; `registrarempresatransporte.php:115`). El servidor no lo vuelve a validar.
2. El alta de cliente calcula `MAX(id)+1`, copia la foto desde `tmp/`, inserta el cliente (nombre en mayúsculas, días de facturación, UAP) y sus representantes con porcentaje (`registrarcliente.php:60-123`).
3. La edición reemplaza todos los representantes (`modificarcliente.php:102-112`).
4. La baja es lógica; en cliente y transportadora se bloquea si hay registros asociados (`eliminarcliente.php:20`, `eliminarempresatransporte.php:20`). SIA no tiene bloqueo.

**Persistencia:** `cliente`, `representar`, `empresa_transporte`, `sia`.

## F-05 · Personas y vehículos (CF-L045…048, 085…088, 243, 247)

1. Persona: alta con tipo de documento distinto de NIT (`registrarpersona.php:106`), apellidos opcionales, licencia, email, dirección, ciudad, ocupación y foto; aviso de existente por AJAX (`:162`).
2. Vehículo: placa + país + datos técnicos + foto; al digitar la placa, `consultarplaca.php` busca por placa y país y, si existe, deshabilita «Registrar» (`registrarvehiculo.php:159-176`). Inserta además `vehiculo_x_convenio` con convenio 0 (`:101`).
3. La transportadora del vehículo se registra desde báscula en `vehiculo_x_empresa` (`mod_bascula/registrarentradabascula.php:86-98`), no desde el maestro.
4. Bajas lógicas con bloqueo por pesajes, representación, convenio o empresa (`eliminarpersona.php:20`, `eliminarvehiculo.php:20`).

## F-06 · Productos (CF-L049…052, 244, 253)

1. Listado por `includes/tablas/tablas-ajax.php` (tabla y columnas por GET, sin sesión: `listarproductos.php:37`).
2. Alta: alias, descripción, embalaje; si hay alias y grupo, inserta `grupoaliasvehiculos` (Colmotores) (`registrarproducto.php:57-73`).
3. Baja lógica sin bloqueo.

## F-07 · Bodegas (CF-L089…092)

1. Alta: nombre, tipo, observaciones, filas, columnas, uso; crea `filas × columnas` secciones `[f][c]` libres (RN-043, `registrarbodega.php:87-133`).
2. Edición de nombre, tipo, observaciones y uso; no cambia la cuadrícula.
3. Baja: marca la bodega y todas sus secciones como eliminadas, sin mirar si tienen mercancía (`eliminarbodega.php:88-104`).

## F-08 · Usuarios, permisos y contraseña (CF-L081…084, 097…099, 246)

1. Alta: `MAX(id)+1`, MD5 de la contraseña, nivel, foto y una fila de `permisos` por módulo con cuatro banderas (`registrarusuario.php:65-122`).
2. Edición: contraseña opcional, nivel y permisos (actualiza o inserta) (`modificarusuario.php:83-131`).
3. Cambio de contraseña propia: AJAX verifica la anterior (`consultacontrasena.php:11`) y el POST la vuelve a comparar antes de guardar (`cambiarcontrasena.php:45-66`, RN-076).
4. Usuarios del portal: el mismo patrón sobre `usuariocliente`, con SIA asociada (`reportesweb/mod_usuarios/registrarusuario.php:84-105`).

## F-09 · Modalidades y requisitos (CF-L037…040, 101)

1. `asignarrequisitos.php?id=&tipo=` borra los documentos de la modalidad para ese tipo de requisito, inserta los marcados y pone `prioridad=1` al predeterminado (`:75-118`).
2. Báscula lee el predeterminado para preseleccionar el documento (`mod_bascula/consultatipodocumento.php:7`) y filtra los documentos por modalidad (`mod_bascula/registrarsalida.php:216`).

## F-10 · Vehículos de un convenio (CF-L100)

`vehiculosasignados.php:54` lista la relación; `asignarvehiculo.php:25` inserta y `desasignarvehiculo.php:25` borra físicamente. Báscula usa esta relación para precargar cliente y tarifa por placa (FUNCTIONAL_GAPS GAP-018).

## F-11 · Selectores y foto (CF-L241, 248, 256)

- `mod_selecciones/*` devuelven `<li>` con coincidencias `LIKE` (máximo 10) de carrocería, ciudad, marca, línea, ocupación, país, placa, depósito o tiquete.
- `includes/subirfoto.php:3-16` redimensiona la imagen en dos tamaños en `tmp/`; el alta la copia a `fotos/`.
