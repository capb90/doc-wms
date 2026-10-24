# 08-procesos-infra-fuera-alcance — 02 Flujos legacy

> AG-08 · 2026-10-23 · Estático. **Prefijos:** `L/` = `bodegas-legacy/`; `D/` = `docs/`.

## F-01 · Copia de seguridad (CF-L004)

1. Cualquier usuario con sesión ve «Administrar Datos → Copia Seguridad» (`L/menus/menuizquierda.php:266,279`). El grupo no filtra por nivel; solo «Configuraciones» lo hace (`:287`).
2. `L/menus/backup.php` no exige sesión: no incluye `aut_verifica.inc.php` ni comprueba permisos (líneas 1-12). Una URL directa lo ejecuta.
3. Borra todos los archivos de `../tmp` (`:22-31`).
4. Recorre `SHOW TABLES` y arma en memoria un SQL con `DROP TABLE`, `SHOW CREATE TABLE` e `INSERT` fila por fila (`:66-138`). Escapa con `addslashes` y `ereg_replace`: los nulos salen como `""`.
5. Escribe `../tmp/db-backup-bodegas-AAAAMMDD.sql` con una cabecera ASCII (`:140-183`), lo comprime en ZIP, borra el SQL y muestra un botón de descarga que apunta al ZIP dentro del sitio web (`:188-200`).
6. **Efectos:** una sola copia en el servidor, que se reemplaza en la siguiente ejecución. Sin retención, programación, registro, aviso de fallo ni copia de los archivos subidos. La descarga queda en una carpeta pública mientras no se vuelva a ejecutar.
7. **Seguridad:** las credenciales de MySQL están escritas en el script (`:15-16`). No se reproducen en esta auditoría.

**Incertidumbres:** no se sabe con qué frecuencia lo usaban ni si había otro respaldo del servidor. `DECISIONES_REVISION.md` §2.E.16 pide una política «similar a la del legacy» (`L/docs/legacy_analysis/DECISIONES_REVISION.md:44`).

## F-02 · Procesos periódicos (CF-LX08-01)

- **`L/cron.php`:** recalcula y emite los períodos de facturación de los depósitos activos, sin el importador 70 (`:6`). No hay `crontab` en el checkout: se supone un cron del servidor. La lógica la audita el módulo 06.
- **Alertas al abrir el panel:** `L/inicial.php:78` ejecuta `evaluaTasa()` y `evaluaAbandonos()` solo para `usuario_nivel ≤ 1`. Las dos hacen `POST` AJAX a `menus/evaluatasacambio.php` (¿hay tasa vigente hoy?) y `menus/evaluaabandonos.php` (¿hay depósitos en la ventana 20–30 sin prórroga o 50–60 con prórroga?). El menú lateral repite `evaluaAbandonos()` en su `onload` (`menuizquierda.php:184`) y colorea «Prorrogas». Las reglas están en los módulos 04 y 06.
- **Modelo:** sin planificador propio, sin registro de ejecuciones y sin aviso a quien no abra el panel.

## F-03 · Portal `reportesweb` (CF-L217)

1. El usuario entra por `L/reportesweb/index.php`. `aut_verifica.inc.php:60-125` busca el usuario en `usuariocliente` (`aut_config.inc.php:10`) y guarda en sesión `colmotores_id`, `colmotores_nivel`, `colmotores_login` y `tipo_acceso`.
2. `entrada.php:3-6` reparte por `tipo_acceso`:
   - **≤ 2, «Colmotores»** (`mod_usuarios/registrarusuario.php:238`): `almacenamiento.php`, con las pestañas vehiculares de `CF-L218…228`.
   - **3, «Intermediarios»** (`:239`): `reportesias.php`. Lista los ingresos activos cuya agencia (`I.id_sia`) es la del usuario (`reportesias.php:37-53`). Desde ahí, `reportesiasdetalle.php` muestra el depósito con productos, pesajes, novedades, guías y salidas de puerta (`:37`, `:310-413`).
3. `usuariocliente` no tiene `id_cliente` (`L/bodegas_schema.sql:1685-1699`): **el portal no tiene clientes genéricos**, solo Colmotores y agencias de aduanas.
4. Los usuarios del portal los gestiona el personal interno (`menuizquierda.php:309-313`, «Gestión Usuarios Web»; CF-L099, módulo 01).

**Consecuencia para la evaluación pedida:** el único dato no Colmotores que un usuario externo consultaba por sí mismo es el listado y el detalle de los ingresos de su agencia (`CF-L217.b`, cuyo contenido es la capacidad `CF-L229` del módulo 07). La v2 lo ofrece como reporte interno para Comercio Exterior (`GET /api/v1/reports/customs-agency-entries`, `ForeignTradeAccess`; `Frontend/wms/app/pages/reports/customs-agency-entries.vue:18`), no como autoservicio de la agencia. Se registra como brecha de alcance (BR-08-008).

## F-04 · Colmotores (CF-L181…200, 240, 250, 262, 263)

Recorridos resumidos. Toda la operación gira alrededor de `productodetalle` (una fila por vehículo con su VIN o serial) y de las vistas filtradas por el importador 70 (`L/bodegas_schema.sql:2526`).

- **Seriales y lista de empaque Colmotores** (`mod_seriales`): se sube un archivo (`archivon`), `leerseriales.php` crea los seriales y el detalle por vehículo con su color (`:107,140`). `cargarlevantescolmotores.php` y `crearlevantescolmotores.php` crean levantes en las tablas **generales** `levante` y `producto_levante` (`:52,103`). `cargarfacturados.php` marca los vehículos facturados (`vinesfacturados`). `eliminar_archivo.php` borra el archivo y sus seriales.
- **Lectura de VIN** (`mod_lecturas`): al ingreso, `leervines.php` registra cada VIN leído contra el vehículo del camión (`vineslectura`); en el cargue, `leervinescargue.php` lo asocia a la orden y puede registrar novedades.
- **Patio externo** (`mod_colmotores`): salidas propias (`salidaexterna`) con número (`numerarsalida.php`), VIN asignados, guía (`verguia.php`), observaciones con impresión y soportes subidos.
- **Voltajes:** registro por vehículo, carga de un plano (`voltajesmigrados` → `voltaje`), consulta, edición y baja.
- **Comparación de archivo:** carga un archivo del cliente a `tmp_vin` y lo compara con existencias, salidas y ubicaciones.
- **Actualización comprimida** (`subiractualizacion.php`): arma `baseGM.txt` con VIN, depósito, levante, salida y ubicación, y lo comprime en `baseGM.gz` para el cliente.
- **`migrarplacas.php`:** script de una vez, sin sesión. Inserta en `vehiculo_x_convenio` cada placa de `placacolmotores` con convenio 1 (`:35-41`).

**Dependencias con el resto del legacy:** los levantes de Colmotores comparten tablas con los de importación. Los depósitos, ingresos y salidas de Colmotores son del importador 70, y la migración v2 los excluye en su consulta (`D/planes/paridad-legacy/plan-backend-paridad-legacy.md:2822`, `NOT IN (0, 70)`; consulta de depósitos con `I.id_importador <> 70`, `:2951-2981`; bodegas con `uso <> 'colmotores'`, `:2853`).
