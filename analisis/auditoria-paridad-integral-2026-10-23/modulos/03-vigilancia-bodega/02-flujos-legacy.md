# 03 · Vigilancia y Bodega — Flujos legacy reconstruidos

> Reconstruidos desde el código (`bodegas-legacy/`). Rutas relativas a `code_workspace/`.

## F1. Ingreso del camión (no hay Vigilancia de ingreso)

1. El camión llega y lo registra **Báscula** («Entradas» → «Nueva Entrada», `bodegas-legacy/menus/menuizquierda.php:195-196`; módulo 02).
2. No hay registro previo de portería, motivo de ingreso ni placa en una tabla propia: el esquema solo tiene `salidapuerta` (`bodegas-legacy/bodegas_schema.sql:1379-1389`).

**Incertidumbre:** si en la operación real el vigilante anotaba los ingresos fuera del sistema. No hay rastro en el código.

## F2. Ubicar mercancía en bodega («Asignar Bodega»)

1. El operario abre `modulos/mod_bodegas/asignarbodegaproducto.php`: tabla con **todos** los lotes (`producto_en_bodega`) con saldo > 0 de importadores distintos de Colmotores, ordenados por fecha de ingreso (`:35`). Por lote muestra saldo, «A Ubicar» = saldo − unidades ubicadas y lo ubicado por bodega (`:129-166`).
2. Elige una bodega (`estado='activo' AND uso='bodegas'`) y una cantidad (`:169`) → `registrarbodegacantidad.php?pu={por ubicar}&pb={lote}`.
3. `registrarbodegacantidad.php` valida contra el «por ubicar» que llegó por GET: si la cantidad lo supera o está vacía, muestra «ALERTA!» y oculta «Guardar»; una negativa se vuelve positiva **después** de comparar (`:52-82`, RN-045). Pinta la cuadrícula de secciones de la bodega con casillas y el contenido de cada sección (`:182-256`); las deshabilitadas salen en gris y sin casilla. Prepara como campos ocultos los `productodetalle` (una fila por unidad) aún sin ubicar, hasta la cantidad pedida (`:288-304`).
4. `guardarcantidadseccion.php` recorre las secciones marcadas y, por cada una, inserta **todas** las unidades seleccionadas en `productodetalle_x_seccion` con estado `activo`, usuario e IP (`:87-118`). Con dos secciones marcadas, la misma unidad queda en ambas (RN-047). No valida capacidad, sección deshabilitada ni duplicado.
5. Efecto: solo posiciones. El saldo del lote no cambia (el saldo es entradas − salidas, RN-035).

## F3. Liberar posiciones («Liberar Bodega»)

1. `reportebodegas.php` lista los mismos lotes con saldo (`:35`) y, por lote, bodega + cantidad a liberar → `liberarbodegacantidad.php` (`:166-170`).
2. `liberarbodegacantidad.php` exige cantidad (el tope está comentado, `:58-67`) y prepara las unidades activas de esa bodega (`:289`).
3. `liberarcantidadseccion.php` marca `estado='libre'` en las secciones marcadas para el rango de IDs `[minimo, maximo]`, **sin** comprobar que cada ID esté seleccionado (la condición está comentada, `:94-105`).
4. Liberación automática al emitir la guía: `modulos/mod_salidas/verguia.php:659-676` (con `crear=1`) libera, por cada unidad que sale, la posición activa más reciente del lote. Con serial, libera la posición del detalle (`:465-479`). La anulación de la salida reactiva posiciones (`modulos/mod_salidas/eliminarsalida.php:89-106`, según el plan backend F4-02; no se volvió a abrir aquí).

## F4. Habilitar o deshabilitar una sección

`listarbodegas.php:154` → `versecciones.php` (cuadrícula) → `habilitarseccion.php?accion=0|1` cambia `seccion.ocupacion` a `deshabilitado` o `Libre` y vuelve a `versecciones.php` (`habilitarseccion.php:39-50`, RN-046). Sin `aut_verifica`.

## F5. Observaciones y novedades de mercancía

1. `asignarobservaciones.php`: busca por depósito (`BA…` con año o número), manifiesto, carta porte o VIN (`:60-104`); sin filtros muestra una consulta con valores fijos que no devuelve nada (`:96-101`). Por lote, «Gestionar Observaciones» → `registrarobservaciones.php?pu=&pb=` (`:235`).
2. `registrarobservaciones.php` (permiso `bodegas/registrar`, `:39-41`) muestra el formulario y la lista de observaciones activas del lote (`:137`):
   - horas de inicio y salida (prellenadas con ahora), tipo (Rutina por defecto, `:293`), descripción obligatoria (Spry), total (prellenado con `pu`), descargada, buena/dañada/faltante/sobrante (en 0), carpa, remolque, registro fotográfico.
   - INSERT en `observacionesproducto` con usuario, IP, fecha y `estado='activo'`; `descargada = total` si se marca, si no 0 (`:91-124`, RN-068). No valida que el desglose sume el total.
   - Por fila: **Imprimir** (`imprimirobservacion.php`) y **Eliminar** (`eliminarobservacion.php`) (`:390-391`). No hay «Modificar» en esta pantalla.
   - Botón «Imágenes» → diálogo `subirimagenes.php?id=PB_{lote}` (`:360`).
3. `eliminarobservacion.php` pone `estado='eliminado'` con usuario `1` e IP `1.1.1.1` fijos (`:44-60`). `modificarobservacion.php` (solo desde pantallas Colmotores) actualiza descripción, cantidades y descargada, también con usuario e IP fijos (`:38-62`).
4. Efectos: ninguno sobre saldos ni avisos.

## F6. Impresión «Reporte de mercancías»

`imprimirobservacion.php?id=` arma la hoja con los datos del lote, del ingreso, del documento comercial, del vehículo, del conductor, de la primera salida del lote y de la observación (`:39-190`). El cuadro «Total» imprime `descargada` (no `total`, `:150-151`).

## F7. Fotografías

`subirimagenes.php` sube por AJAX a `procesa.php`, que acepta JPEG/GIF/PNG, redimensiona a 900 px y guarda en `fotosobservaciones/{id}/` (`procesa.php:82-118`); lista y elimina por la ruta recibida (`:75-80`). No hay tabla; las fotos son por lote.

## F8. Cargue en Bodega

1. `listarcargues.php` (permiso `bodegas/registrar`) lista las salidas con `ordencargue` no completa (`:84`) y su relación de mercancía con entrada, saldo anterior, cantidad que sale y saldo nuevo (`:488-493`).
2. «Completar Carga» llama por AJAX a `completarcargue.php`, que pone `ordencargue.estado='completo'` para la salida (`completarcargue.php:3-7`). No exige sesión, no valida cantidades ni toca saldos o posiciones: el saldo baja con la salida de Comercio Exterior y las posiciones con la guía (F3.4).

## F9. Portería: entrega por guía

1. El vigilante (nivel 3) entra directo a `salidapuerta/index.php` (`aut_verifica.inc.php:101-103`).
2. Digita o lee `id_vehiculo-nro_guia` (`:40-45`). Si la guía existe:
   - sin entrega previa: `UPDATE salida SET fechahora_fin=ahora` e `INSERT salidapuerta` con vehículo, salida, fecha, IP y usuario (`:49-58`);
   - con entrega previa: «Ya se registró la guia de salida» (`:51-53`).
3. Guía inexistente: «El dato leído no se encontro en la lista de salidas» (`:60-62`).
4. Listado: guía, placa, fecha de autorización, fecha de salida, transportadora, cliente, observaciones (`:77-84,142-169`). El icono «Eliminar» apunta a un script que no existe (`:165`).
5. No compara el vehículo leído con el de la guía ni el estado del cargue (RN-042).

## Incertidumbres

- Uso real de secciones: la migración encontró 9 bodegas activas y solo 6 secciones (`docs/planes/migracion-staging/plan-migracion-legacy-staging.md:65`), lo que sugiere que la ubicación por secciones se usaba poco.
- Si «Liberar Bodega» se usaba con su defecto de rango (F3.3) no es verificable sin datos.
- El efecto de `eliminarsalida.php` sobre posiciones se tomó del plan backend F4-02 sin reabrir el script.
