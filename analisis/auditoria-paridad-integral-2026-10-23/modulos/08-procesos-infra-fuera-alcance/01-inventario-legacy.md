# 08-procesos-infra-fuera-alcance — 01 Inventario legacy

> AG-08 · 2026-10-23 · Auditoría estática (sin ejecución, sin Git, sin abrir `Connections/`, `.env*` ni `db_legacy/`).
> **Prefijos:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `D/` = `docs/`. En el CSV las rutas van completas.
> Capacidades asignadas: 38 legacy (`CF-L004`, `CF-L181…200`, `CF-L217…228`, `CF-L240`, `CF-L250`, `CF-L257`, `CF-L262`, `CF-L263`) y 5 candidatas V2 (`CF-V080…083`, `CF-V085`). Altas de este agente: `CF-LX08-01`, desgloses `CF-L217.a/.b`, `CF-V080.a…e`, `CF-V081.a…e`, y `CF-V086`, `CF-V087`.

## 1. Parte A — procesos e infraestructura

| ID | Capacidad | Pantalla / script | Tablas | Permiso legacy | Observaciones |
| --- | --- | --- | --- | --- | --- |
| CF-L004 | Generar copia de seguridad | `L/menus/backup.php` (menú «Administrar Datos → Copia Seguridad», `L/menus/menuizquierda.php:279`) | Todas (`SHOW TABLES`, `backup.php:70-78`) | Ninguno: el script no incluye `aut_verifica.inc.php` (líneas 1-12) ni `verificapermisos`; el menú «Administrar Datos» no filtra por nivel (solo «Configuraciones» lo hace, `menuizquierda.php:287`) | Volcado SQL por PHP (`backup.php:66-138`), guardado en `../tmp` y comprimido en ZIP con enlace de descarga (`:188-200`). Antes borra todo lo que haya en `../tmp` (`:22-31`): solo queda una copia. Solo base de datos, sin archivos subidos. **Las credenciales de la base están escritas en el script (`:15-16`); no se copian aquí.** |
| CF-LX08-01 | Procesos periódicos del legacy (no catalogado como capacidad propia) | `L/cron.php` (sin planificador en el checkout: se infiere un cron externo por el nombre; excluye el importador 70, `cron.php:6`; lógica del módulo 06), `L/menus/evaluatasacambio.php` y `L/menus/evaluaabandonos.php` (AJAX al abrir `L/inicial.php:37-76`, invocadas en el `onload` solo si `usuario_nivel ≤ 1`, `:78`; y `menuizquierda.php:149-180`, `onload` solo de `evaluaAbandonos`, `:184`) | `tasa_cambio`, `vista_kardexdepositos` | Sesión | El legacy no tiene planificador propio: un cron del sistema operativo y alertas que se evalúan en el navegador al abrir el panel. `evaluaTasa()` del menú está definida con un `setTimeout` de 1 s pero no se invoca en el `onload` del menú. Las reglas (TRM, abandono) las auditan 06 y 04. |

Capacidades V2 de la parte A (sin equivalente legacy o reemplazo ampliado): respaldos con destinos (`CF-V080`), importación legacy (`CF-V081`), notificaciones en tiempo real (`CF-V082`), centro de ayuda (`CF-V083`), `SystemController` (`CF-V085`), infraestructura de jobs (`CF-V086`, nueva) y correo SMTP de avisos (`CF-V087`, nueva). Ver `05-analisis-v2.md`.

**Búsqueda de equivalentes legacy de `CF-V082` y `CF-V083`:** `grep -rli "ayuda|manual de usuario|tutorial|websocket|notificacion"` en `L/**/*.php`: una sola coincidencia irrelevante (`L/modulos/mod_bodegas/asignarseleccionadosseccioncolmotores.php`). El legacy no tenía centro de ayuda ni notificaciones persistidas; sus «alertas» son los avisos rojos del panel (`CF-LX08-01`).

## 2. Parte B — exclusiones (Colmotores y portal)

Fuente de la exclusión en todas las filas: `D/planes/paridad-legacy/plan-backend-paridad-legacy.md:32` (§A.3), `D/planes/paridad-legacy/plan-frontend-paridad-legacy.md:34` (§A.3), `L/docs/legacy_analysis/MIGRATION_MATRIX.md:14` («Alcance, decisión del 2026-09-24») y la fila de cada capacidad en §«Excluidas del alcance» (`:221-285`). `CF-L217` está excluida como «Acceso, autenticación y roles» (`MIGRATION_MATRIX.md:265`).

Permisos legacy de los tres módulos (variable `$modulo` antes de `evaluaPermiso`): `seriales` (20 scripts), `salidas` (5) y `bodegas` (4). Varios scripts no exigen sesión (sin `aut_verifica`): `mod_colmotores/{consultarconductor,consultarempresatransporte,eliminarobservacion,imprimirobservacion,listarvoltajescolmotores,modificarobservacion,numerarsalida,seleccionarvin,seleccionarvinexistencia,subiractualizacion,subirsoportes}.php`, `mod_lecturas/{eliminarvincargue,seleccionarplaca}.php`, `L/migrarplacas.php` y varias páginas de `reportesweb/` (`daily.php`, `descargue.php`, `reporteocupacionbodegas.php`, `ubicacionvehiculos.php`…). Es una anomalía del legacy, sin efecto en V2.

| ID | Capacidad | Scripts (línea del SQL principal) | Tablas |
| --- | --- | --- | --- |
| CF-L181 | Consultar salidas de patio externo | `L/modulos/mod_colmotores/listarsalidas.php:88,274`; menú `menuizquierda.php:242` | `salidaexterna`, `vista_vehiculos`, `pesaje`, `ciudad`, `cliente`, `sia` |
| CF-L182 | Registrar salida de patio externo | `registrarsalida.php:58,61`; `numerarsalida.php:9` | `salidaexterna`, `cuadrilla` |
| CF-L183 | Modificar salida de patio externo | `modificarsalida.php:57,84` | `salidaexterna` |
| CF-L184 | Asignar y quitar VIN de salida externa | `asignarvines.php:61,66`; `eliminarvinasignado.php:22` | `productodetalle` |
| CF-L185 | Guía de patio externo | `verguia.php:58,62` | `salidaexterna`, `vista_existenciascolmotores` |
| CF-L186 | Importar y comparar archivo Colmotores | `comparacionarchivo.php:103,114`; `consultacomparacionarchivo.php:83,166`; `procesa.php:47` | `tmp_vin`, `productodetalle`, `productodetalle_x_seccion`, `producto_salida` |
| CF-L187 | Importar plano de voltajes | `subirvoltajes.php:103,114`; `regitrarplanovoltajes.php:83,162` | `voltajesmigrados`, `voltaje` |
| CF-L188 | Registrar voltaje | `registrarvoltaje.php:241,274` | `voltaje`, `productodetalle`, `pesaje` |
| CF-L189 | Consultar y modificar voltajes | `listarvoltajescolmotores.php`; `modificarvoltaje.php:50,81`; `eliminarvoltaje.php:50,77`; menú `:239-240` | `voltaje`, `producto_en_bodega` |
| CF-L190 | Observaciones externas | `modificarobservacion.php:42,72`; `eliminarobservacion.php:44,65`; `imprimirobservacion.php:39` | `observacionesproducto` |
| CF-L191 | Soportes de salida externa | `subirsoportes.php:39` | `salidaexterna` |
| CF-L192 | Leer VIN al ingreso | `L/modulos/mod_lecturas/inicio.php`; `leervines.php:58,66`; `lista.php:21,44`; menú `:226` | `vineslectura`, `productodetalle`, `serial`, `vehiculo` |
| CF-L193 | Eliminar lectura de VIN | `eliminarvinlectura.php:23,28` | `vineslectura`, `productodetalle` |
| CF-L194 | Leer VIN en cargue | `leervinescargue.php:71,95` | `ordencargue`, `productodetalle`, `observacionesproducto` |
| CF-L195 | Quitar VIN de cargue | `eliminarvincargue.php:5,18` | `ordencargue` |
| CF-L196 | Menú y archivos de seriales | `L/modulos/mod_seriales/menucolmotores.php`; `archivo.php:46`; `listarregistros.php:56,86`; menú «Importar Lista Empaque» `:225` | `archivon`, `serial` |
| CF-L197 | Importar seriales de lista de empaque | `leerseriales.php:107,140` | `archivon`, `serial`, `productodetalle`, `colorvehiculo` |
| CF-L198 | Cargar levantes Colmotores | `cargarlevantescolmotores.php:72,83`; `crearlevantescolmotores.php:52,103` | `vineslevantesmigrados`; **escribe en `levante` y `producto_levante` generales** |
| CF-L199 | Cargar facturados Colmotores | `cargarfacturados.php:72,118`; `actualizafacturados.php:52,110` | `vinesfacturados`, `productodetalle` |
| CF-L200 | Eliminar archivo importado | `eliminar_archivo.php:51,59` | `archivon`, `serial` |
| CF-L217 | Sesión del portal (`reportesweb`) | `L/reportesweb/index.php`; `aut_verifica.inc.php:114-125` (tabla `usuariocliente`, `aut_config.inc.php:10`); `entrada.php:3-6` | `usuariocliente` (`L/bodegas_schema.sql:1685-1699`: sin `id_cliente`, con `id_sia` y `tipo_acceso`) |
| CF-L217.a | Usuario «Colmotores» (`tipo_acceso` 2) | `entrada.php:3-4` → `almacenamiento.php`; tipos en `mod_usuarios/registrarusuario.php:237-239` | — |
| CF-L217.b | Usuario «Intermediarios» = agencia de aduanas (`tipo_acceso` 3) | `entrada.php:5-6` → `reportesias.php:37-53` (ingresos con `I.id_sia` de la SIA del usuario), `reportesiasdetalle.php:37,310-413`, `veringreso.php` | `ingreso`, `pesaje`, `producto_en_bodega`, `observacionesproducto`, `guiadesalida`, `salidapuerta` |
| CF-L218 | Almacenamiento (portal) | `almacenamiento.php:91-167` (pestañas en iframe: `descargue`, `cantidadesgrupo`, `reporteocupacionbodegas`, `verbodega`, `ubicacionvehiculos`, `resumenfacturados`) | vistas Colmotores |
| CF-L219 | Control de inventario (portal) | `controlinventario.php` (pestañas Antigüedad, Inventario en Patio, Promedio, Daily, Averías, Voltajes, Consulta por VIN) | vistas Colmotores |
| CF-L220 | Control y cumplimiento de entregas | `controlentregas.php`; `cumplimientoentregas.php` | `vista_salidascolmotores`, `salidaexterna`, `guiadesalida`, `ordencargue` |
| CF-L221 | Inventario y desglose | `inventario.php`; `cantidadesgrupo.php`, `cantidadesmodelo.php`, `cantidadesdetalle.php` | `vista_existenciascolmotores`, `vista_vehiculos`, `grupoaliasvehiculos` |
| CF-L222 | Antigüedad de vehículos | `antiguedadvehiculos.php` | `vista_existenciascolmotores`, `colorvehiculo` |
| CF-L223 | Resumen de facturados | `resumenfacturados.php` | `productodetalle`, `vista_existenciascolmotores` |
| CF-L224 | Novedades y voltajes | `novedades.php`; `reportevoltajes.php` | `observacionesproducto`, `voltaje` |
| CF-L225 | Promedio de almacenamiento | `promedioalmacenamiento.php` | `vista_existenciascolmotores` |
| CF-L226 | Ocupación y ubicación de vehículos | `reporteocupacionbodegas.php`, `ubicacionvehiculos.php`, `verbodega.php`, `verubicacionvehiculo.php`, `verseleccionadosseccioncolmotores.php` | `bodega`, `seccion`, `productodetalle_x_seccion` |
| CF-L227 | Reporte por VIN | `reportevin.php` | `productodetalle`, `levante`, `voltaje`, `salida` |
| CF-L228 | Reporte diario y descargue | `daily.php`; `descargue.php` | `vineslectura`, `pesaje`, `vista_vehiculos` |
| CF-L240 | Selectores de Colmotores | `mod_colmotores/consultarconductor.php:7`, `consultarempresatransporte.php:10`, `seleccionarvin.php:14`, `seleccionarvinexistencia.php` | `productodetalle`, `vista_existenciascolmotores` |
| CF-L250 | Selector de lecturas | `mod_lecturas/seleccionarplaca.php:10` | `vehiculo` |
| CF-L257 | Autocompletar del portal | `reportesweb/consultamodelo.php`, `seleccionarsalida.php`, `seleccionarvin.php`, `consultaposicionseccion.php` | `grupoaliasvehiculos`, `vista_salidascolmotores` |
| CF-L262 | Migrar placas Colmotores a convenios | `L/migrarplacas.php:35-41` | `placacolmotores` → `vehiculo_x_convenio` |
| CF-L263 | Base comprimida de actualización Colmotores | `mod_colmotores/subiractualizacion.php:11-90` (`baseGM.txt` → `baseGM.gz`) | `productodetalle`, `levante`, `guiadesalida`, `productodetalle_x_seccion` |

**Las vistas del portal son de Colmotores por definición:** `vista_vehiculos` filtra `id_importador = 70` (`L/bodegas_schema.sql:2526`), y `vista_existenciascolmotores` (`:2336`) y `vista_salidascolmotores` (`:2507`) parten de `productodetalle`. La variable de sesión se llama `colmotores_id` para todos los usuarios del portal (`aut_verifica.inc.php:114`), también para las agencias: es un nombre heredado, no una marca de Colmotores.

**No catalogados:** `reportesweb/mostrarvines.php` es un esqueleto vacío de 9 líneas (también lo dice `L/legacy-analysis/LEGACY_ROUTES.md:487`); no se da de alta. Los demás scripts de los tres módulos aparecen en el catálogo como «(+n)» de alguna capacidad.
