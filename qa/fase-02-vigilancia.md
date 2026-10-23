# Fase 2 — Vigilancia

> Lee antes `00-plan-maestro.md`. Rol principal: **Operario vigilancia** (`vigilancia`). Verificaciones cruzadas con `bascula` y `bodega`.

## 1. Objetivo

Validar el registro de ingreso y salida de vehículos, el historial, la corrección de ingresos (WMS-5) y, sobre todo, que cada ingreso llegue al lugar correcto: la **cola de Báscula** si el motivo requiere pesaje, la **recepción directa de Bodega** si no.

## 2. Alcance

| Pantalla | Ruta | Bloque |
|---|---|---|
| Ingreso | `/operations/entries` | ING |
| Salida | `/operations/entries/exits` | SAL |
| Historial | `/operations/entries/history` | HIS |
| Corrección de ingreso (desde Historial) | diálogo `CorrectEntryLogDialog` | COR |
| Entrega a Báscula y Bodega | `/operations/weighbridge`, `/warehouse/receptions` | INT |

**Fuera:** la operación en báscula (fase 3) y la recepción (fase 4). Aquí solo se comprueba que el ingreso aparece donde debe.

## 3. Criterios de entrada

1. Fase 1 aprobada; vehículos `QAA101..103` y motivos sembrados disponibles.
2. Cuentas `vigilancia`, `bascula` y `bodega` activas.

## 4. Reglas que se verifican

- La placa se normaliza (sin espacios, mayúsculas). Si el vehículo no existe se crea solo con la placa.
- **Un vehículo no puede tener dos ingresos abiertos** (409 «La placa ya tiene un ingreso abierto.»).
- Motivo obligatorio. Observaciones opcionales. La UI no captura conductor, país ni fecha (el backend usa la hora del servidor).
- Motivos con pesaje → cola de báscula. «Solo bodega» y «Otro» → pendientes de recepción directa.
- La salida solo se bloquea si ya tiene salida. **No** se bloquea con operaciones abiertas (riesgo R-VIG-03).
- Corrección: placa 3–20 `[A-Z0-9-]`; fecha no futura, no posterior a la salida ni al primer pesaje; motivo de corrección 10–500; el motivo de ingreso no se cambia si ya hay operación de báscula o bodega.

## 5. Datos que esta fase deja para las siguientes

Al terminar deben quedar **abiertos** (sin salida) estos ingresos, anotados en el registro de datos:

| Placa | Motivo | Para |
|---|---|---|
| `QAA101` | Descargue importación | F3 ingreso IMP |
| `QAA102` | Descargue exportación | F3 ingreso EXP |
| `QAA103` | Solo báscula | F3 solo báscula |
| `QAB201` (nuevo) | Descargue importación | F3 segundo camión mismo documento |
| `QAB202` (nuevo) | Descargue importación | F3 unidades de carga / tanquero |
| `QAB203` (nuevo) | Descargue importación | F3 INSP (cambiar modalidad en báscula) |
| `QAB204` (nuevo) | Solo bodega | F4 recepción sin báscula |
| `QAB205` (nuevo) | Cargue importación | F3/F5 salida de mercancía |

## 6. Casos

### 6.1 Ingreso (ING)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F2-ING-001 | Ingreso de vehículo existente | Placa `QAA101` + Enter → «Vehículo encontrado» → motivo Descargue importación → Registrar. | Éxito; aparece en «Camiones en planta» (contador +1). | P0 | FUN |
| F2-ING-002 | Ingreso de vehículo nuevo | Placa `QAB201` + Enter → «No existe, se creará al registrar» → motivo → Registrar. | Se crea el vehículo y el ingreso. Admin → Vehículos muestra `QAB201` sin tipo ni transportadora. | P0 | FUN |
| F2-ING-003 | Normalización de placa | Escribir ` qab 202 ` (minúsculas y espacios). | Se busca y registra como `QAB202`. | P1 | VAL |
| F2-ING-004 | Ingreso duplicado | Con `QAA101` abierto, intentar otro ingreso. | Botón deshabilitado o aviso «Ingreso duplicado — Este vehiculo ya tiene un ingreso abierto.»; por API, 409. | P0 | RN |
| F2-ING-005 | Motivo obligatorio | Placa sin motivo. | «Motivo requerido»; botón deshabilitado. | P1 | VAL |
| F2-ING-006 | Búsqueda solo con Enter | Escribir la placa sin Enter y registrar. | Anotar el comportamiento (el botón Buscar está oculto; el manual lo menciona: documentación desactualizada). | P2 | UX |
| F2-ING-007 | Coincidencia parcial de placa | Con `QAB201` existente, escribir `QAB20` + Enter. | Esperado: «No existe, se creará» (es otra placa). Riesgo R-VIG-01: puede encontrar `QAB201` (o `QAB202`) y registrar el ingreso al vehículo equivocado o bloquearlo como duplicado. | P0 | RN |
| F2-ING-008 | Observaciones | Registrar `QAB203` con observación larga (≥ 500 caracteres). | Se guarda; se ve en el detalle del historial. Anotar el límite. | P2 | VAL |
| F2-ING-009 | Crear el resto de ingresos del §5 | Registrar los ingresos de la tabla del §5. | Todos abiertos y anotados con su hora. | P0 | FUN |
| F2-ING-010 | Placa inválida | Placa `AB` o con símbolos `AB#12`. | Anotar si se rechaza o se crea un vehículo con placa inválida (el alta rápida solo exige no vacía). | P1 | VAL |
| F2-ING-011 | Vehículo inactivo | Desactivar (Admin) `QAA103` antes de su ingreso; ingresar. | Anotar el comportamiento (¿lo encuentra, lo reactiva, crea otro?). Reactivar después. | P2 | RN |
| F2-ING-012 | Fecha de ingreso | Revisar si la UI permite indicar fecha/hora. | No la permite; el ingreso queda con la hora del servidor (hora Colombia en pantalla). R-VIG-05. | P2 | FUN |
| F2-ING-013 | Persistencia | Recargar tras registrar. | El ingreso sigue en «Camiones en planta» y en el historial. | P1 | PER |

### 6.2 Salida (SAL)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F2-SAL-001 | Lista de ingresos abiertos | Abrir Salida. | Tarjetas de ingresos abiertos con tiempo en planta, paginadas de 12 en 12. | P1 | FUN |
| F2-SAL-002 | Búsqueda por placa | Buscar `QAB2`. | Filtra por coincidencia parcial (tras ~400 ms). | P1 | FUN |
| F2-SAL-003 | Registrar salida | Crear un ingreso de prueba `QAC301` (motivo Otro) → Salida → «Registrar salida» → confirmar. | Desaparece de la lista; en el historial muestra la hora de salida; el contador de planta baja. | P0 | FUN |
| F2-SAL-004 | Doble salida | Por API, `POST entry-logs/{id}/departure` sobre `QAC301` otra vez. | 409 «El ingreso ya tiene una salida registrada.». | P1 | RN |
| F2-SAL-005 | Salida con ciclo de báscula abierto | (Ejecutar al final de la fase 3 o con un camión de prueba con primer pesaje.) Registrar salida de un camión con ciclo «Por repesar». | Esperado de negocio: impedir o advertir. Riesgo R-VIG-03: se permite; luego el repesaje falla por fecha posterior a la salida. Documentar el resultado y el impacto. | P0 | INT |
| F2-SAL-006 | Salida con recepción en progreso | Camión con recepción iniciada en Bodega (fase 4). | Igual que F2-SAL-005: anotar si se permite y qué queda en las listas de Bodega. | P1 | INT |
| F2-SAL-007 | Salida con orden de cargue pendiente | Camión de salida con OC en Pending (fase 5). | Igual: anotar. | P1 | INT |
| F2-SAL-008 | Tiempo en planta | Observar una tarjeta con > 24 h (si hay datos) o la de mayor tiempo. | Se marca en amarillo desde 24 h; el contador se refresca cada 30 s. | P3 | UI |
| F2-SAL-009 | Datos de la salida por API | Revisar la petición de salida en Red. | Anotar que `DateTimeDeparture` y `DepartureAuthorizedById` los envía el cliente (R-BOD-08 / seguridad: fase 9). | P3 | SEG |

### 6.3 Historial (HIS)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F2-HIS-001 | Listado | Abrir Historial. | Columnas placa, motivo, estado (Registrado/Completado), ingreso, salida o «Abierto», marca «Corregido». | P1 | FUN |
| F2-HIS-002 | Filtro por motivo | Filtrar por «Solo bodega». | Solo esos ingresos. | P1 | FUN |
| F2-HIS-003 | Filtro por placa parcial | Filtrar por `QAB20`. | Esperado: todos los ingresos cuyas placas contienen `QAB20`. Riesgo R-VIG-01: el filtro toma un solo vehículo (el primero que coincide) y oculta los demás. | P1 | FUN |
| F2-HIS-004 | Ver detalle | «Ver» en un ingreso. | Muestra los datos del ingreso y observaciones. | P2 | FUN |
| F2-HIS-005 | Paginación y orden | Recorrer páginas. | Orden descendente por fecha; sin duplicados. | P2 | FUN |
| F2-HIS-006 | Acciones ocultas | Buscar «Autorización de salida» o «Crear manifiesto». | No hay botones (diálogos sin uso en el código). Anotar si aparece alguno. | P3 | FUN |

### 6.4 Corrección de ingreso — WMS-5 (COR)

Usar ingresos de prueba propios (`QAC3xx`) para no estropear los del §5, salvo donde se indique.

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F2-COR-001 | Acceso | Historial → «Editar» en un ingreso abierto. | Diálogo de dos pasos (editar → confirmar con «anterior → nuevo»). Solo Admin y Vigilancia ven «Editar». | P1 | FUN |
| F2-COR-002 | Corregir placa a una nueva | Ingreso `QAC302` → placa `QAC392`, motivo de corrección de 10+ caracteres. | Se reasigna a un vehículo nuevo `QAC392`; marca «Corregido»; aviso «Vehículo desactivado» si el vehículo viejo queda sin uso. | P0 | FUN |
| F2-COR-003 | Corregir placa a una con ingreso abierto | Corregir `QAC303` a `QAA101` (abierto). | 409 «La placa QAA101 ya tiene un ingreso abierto.». | P0 | RN |
| F2-COR-004 | Placa inválida | `AB`, `ABC#1`, 21 caracteres. | Rechazado en UI (3–20 `[A-Z0-9-]`); normaliza mayúsculas al escribir. | P1 | VAL |
| F2-COR-005 | Motivo de corrección | 9 caracteres; 501 caracteres. | «El motivo de la corrección debe tener entre 10 y 500 caracteres.». | P1 | VAL |
| F2-COR-006 | Sin cambios | Abrir y confirmar sin cambiar nada. | «No hay cambios para guardar.» o botón deshabilitado. | P2 | VAL |
| F2-COR-007 | Corregir fecha hacia atrás | Fecha 1 h antes. | Se guarda; el historial muestra la nueva hora. | P1 | FUN |
| F2-COR-008 | Fecha futura | Fecha +10 min. | Rechazado (tolerancia 2 min). | P1 | VAL |
| F2-COR-009 | Fecha posterior a la salida | En `QAC301` (con salida), fecha después de la salida. | «La fecha de ingreso no puede ser posterior a la salida registrada (…)». | P1 | RN |
| F2-COR-010 | Fecha posterior al primer pesaje | (Tras fase 3) en un ingreso con primer pesaje, fecha posterior a ese pesaje. | «…posterior al primer pesaje del ingreso (…)». Si hay depósitos: aviso «Fecha del depósito sin cambios». | P1 | INT |
| F2-COR-011 | Cambiar motivo sin operación | `QAC304` (Otro) → Descargue importación. | Se guarda; el ingreso **entra** en la cola de báscula (verificar con `bascula`). Riesgo R-VIG-02: verificar que no quede «Completado» y fuera de la cola. | P0 | INT |
| F2-COR-012 | Cambiar motivo con operación | (Tras fase 3) en un ingreso con servicio de báscula. | Motivo deshabilitado; por API 409 «No se puede cambiar el motivo de ingreso: el ingreso ya tiene una operación de báscula o de bodega…». | P1 | RN |
| F2-COR-013 | Persistencia y marca | Recargar el historial. | Correcciones persistidas; marca «Corregido» visible. | P1 | PER |
| F2-COR-014 | Rol Bodega por API | Con `bodega`, `PUT entry-logs/{id}/correction`. | 403 (EntryCorrectionAccess = Admin, Receiving). | P2 | ROL |

### 6.5 Integración con Báscula y Bodega (INT)

| ID | Caso | Rol | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|---|
| F2-INT-001 | Cola de báscula | Báscula | Abrir `/operations/weighbridge`. | Aparecen `QAA101`, `QAA102`, `QAA103`, `QAB201`, `QAB202`, `QAB203`, `QAB205` como «Sin iniciar» (refresco cada 15 s). | P0 | INT |
| F2-INT-002 | Motivos sin pesaje fuera de la cola | Báscula | Buscar `QAB204` (Solo bodega) y los de motivo Otro. | No aparecen en la cola. | P0 | INT |
| F2-INT-003 | Preselección por motivo | Báscula | Seleccionar `QAA101` y `QAB205`. | `QAA101` preselecciona «Ingreso con depósito» + IMP; `QAB205` «Salida de mercancía»; `QAA103` «Solo báscula». (Solo mirar; no guardar.) | P1 | INT |
| F2-INT-004 | Recepción directa en Bodega | Bodega | `/warehouse/receptions` → «Recepción directa». | `QAB204` aparece en pendientes directos. | P0 | INT |
| F2-INT-005 | Salida retira de la cola | Báscula | Tras registrar salida de un ingreso de prueba sin operación. | Desaparece de la cola. | P1 | INT |
| F2-INT-006 | Motivo sin pesaje creado en F1 | Vigilancia/Báscula | Ingreso con `QA Motivo pesaje` desmarcado (F1-MOT-004). | No entra a la cola. | P2 | INT |
| F2-INT-007 | Trazabilidad | Admin | Dashboard `/` con filtro Hoy. | Los ingresos aparecen en la etapa de portería; un ingreso nuevo refresca el tablero en vivo. | P2 | INT |

## 7. Criterios de salida específicos

- P0 de ING, SAL, COR e INT ejecutados; F2-INT-001, 002 y 004 en `PASA` (sin ellos no hay fase 3 ni fase 4).
- Ingresos del §5 abiertos y anotados.
- Riesgos verificados: R-VIG-01, 02, 05; R-VIG-03 queda pendiente de F2-SAL-005 (se completa al final de la fase 3) — anotarlo en el informe.

## 8. Entregables

Informe de fase, defectos, registro de datos. Detenerse.
