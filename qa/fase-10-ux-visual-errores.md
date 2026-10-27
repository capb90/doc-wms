# Fase 10 — UX, comportamiento visual y manejo de errores

> Lee antes `00-plan-maestro.md`. Recorre las pantallas de todos los módulos con su rol real. No repite reglas de negocio: mira **cómo** se presentan, **cómo** responde la interfaz ante errores y **cómo** se trabaja con teclado y pantallas reales.

## 1. Objetivo

Validar consistencia visual, legibilidad, retroalimentación al usuario, uso con teclado, responsive en los equipos reales de la bodega, accesibilidad básica, textos en español y la robustez ante errores de red, de validación, de concurrencia y de doble envío.

## 2. Criterios de entrada

1. Fases 1 a 6 aprobadas.
2. Datos QA suficientes para llenar listas (≥ 20 filas en al menos una tabla por módulo).
3. Resoluciones a probar: 1920×1080, 1366×768 (equipo típico de portería/báscula), 1024×768, y tableta 768×1024 si Bodega usa tableta (preguntar al usuario).

## 3. Lista de pantallas a recorrer (una pasada por pantalla)

Login · Trazabilidad · Notificaciones · Usuarios · Terceros (lista, detalle, convenio) · Productos · Servicios · Catálogos simples (uno) · Vigilancia (ingreso, salida, historial, corrección) · Báscula (banco de trabajo, historial, ciclo, recuperar, dashboard, reportes) · Bodega (tablero, pendientes, recepción, detalle, montacargas, inventario, órdenes, novedades) · CE (tablero, kanban, lista IMP con filtros, detalle IMP, OC crear/detalle, guías, levantes, abandono) · Facturación (dashboard, facturas, detalle, acciones, pagos, pendientes, configuración, reportes) · Reportes (dos).

## 4. Casos

### 4.1 Consistencia visual (UI)

| ID | Caso | Verificación por pantalla | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F10-UI-001 | Encabezados y migas | Recorrer las páginas del menú: título, acciones, filtros, tabla y miga. | Patrón uniforme entre módulos. **Actualizado (`DEC-058`, U1–U8):** todas las páginas del menú, salvo el centro de ayuda y los formularios «Crear», abren con la misma tarjeta de encabezado: un solo título, subtítulo y las acciones a la derecha, con el «Nuevo …» primario. Debajo van la tarjeta de filtros (etiquetas, búsqueda con espera y «Limpiar filtros» cuando hay más de un filtro) y la de contenido, con el mismo espacio entre tarjetas. Las tablas comparten el estilo, el aviso de vacío y el paginador («Mostrando {first} a {last} de {totalRecords} registros», 10/25/50 filas). La miga coincide con el título, también en Terceros con `?rol=`. La guardia `test/unit/guards/page-header.spec.ts` del frontend está en verde. | P2 | UI |
| F10-UI-002 | Botones | Primario/secundario/peligro; estados deshabilitado y cargando. | Colores y estilos coherentes; acciones destructivas en rojo con confirmación. | P2 | UI |
| F10-UI-003 | Estados con color | Etiquetas de estado (depósito, factura, OC, ciclo). | Mismos colores para el mismo concepto en todas las pantallas; texto además del color. | P2 | UI |
| F10-UI-004 | Tablas | Columnas, alineación numérica a la derecha, paginación, orden, vacíos («Sin datos»). | Coherente; sin columnas cortadas. | P2 | UI |
| F10-UI-005 | Formatos | Moneda ($ con separador de miles colombiano), pesos (kg), fechas (dd/mm/aaaa hh:mm, hora Colombia), cantidades con unidad. | Uniformes en pantallas, PDF y Excel. | P1 | UI |
| F10-UI-006 | Textos | Revisar textos visibles. | En español, sin «stakeholder» residual donde ya dice «Terceros», sin estados en inglés (R-CE-07), sin errores ortográficos, sin claves de traducción crudas. | P2 | UI |
| F10-UI-007 | Modo claro/oscuro | Si la plantilla ofrece cambio de tema: probarlo en 5 pantallas. | Legible en ambos; sin textos invisibles. | P3 | UI |
| F10-UI-008 | Iconos | Iconos sin texto. | Tienen tooltip o etiqueta. | P3 | UI |

### 4.2 Responsive y equipos reales (RES)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F10-RES-001 | Báscula a 1366×768 | Banco de trabajo: la cola y el panel de proceso abierto. | Sin solapamientos; sin scroll horizontal; botones de paso visibles. **Actualizado (`DEC-058`, B4):** la cola ocupa todo el ancho. El panel queda encima de la cola y de la barra superior, su cuerpo se desplaza por dentro y el encabezado deja visibles «Guardar», «Soltar camión» y «Volver a la cola». F2 abre «Captura de peso» encima del panel. Ver F3-UX-006. | P0 | UI |
| F10-RES-002 | Vigilancia a 1366×768 | Ingreso y salida. | Usable sin scroll horizontal. | P1 | UI |
| F10-RES-003 | 1024×768 | Pantallas principales de cada módulo. | Menú colapsable; tablas con scroll interno, no de página. | P2 | UI |
| F10-RES-004 | Tableta | Recepción, firma y fotos de Bodega en 768×1024 (si aplica). | Firma con el dedo; cámara/galería para fotos; botones alcanzables. | P2 | UI |
| F10-RES-005 | Zoom 125–150 % | Báscula y Facturación. | Usable. | P3 | UI |
| F10-RES-006 | Diálogos | Diálogos largos (acciones de factura, OC, recepción) en 1366×768. | Con scroll interno y botones visibles. | P2 | UI |

### 4.3 Usabilidad y retroalimentación (UX)

| ID | Caso | Verificación | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F10-UX-001 | Confirmación de éxito | Tras cada guardado. | Aviso de éxito breve; la pantalla refleja el cambio sin recargar (invalidación de consultas). | P1 | UX |
| F10-UX-002 | Indicador de carga | Acciones lentas (reportes, PDF, confirmar). | Spinner o botón «cargando»; botón deshabilitado mientras tanto. | P1 | UX |
| F10-UX-003 | Confirmación de acciones destructivas | Anular, descartar, cancelar, revertir, eliminar. | Diálogo de confirmación con el objeto afectado; motivo cuando aplica. | P0 | UX |
| F10-UX-004 | Errores de validación en el campo | Formularios principales. | El error aparece junto al campo, en español, y el foco va al primero. | P1 | UX |
| F10-UX-005 | Preservar lo digitado ante error | Provocar un error del backend al guardar en: tercero, cobro de báscula, OC, pago. | Lo digitado se conserva (R-FAC-16 en pagos). | P1 | UX |
| F10-UX-006 | Filtros persistentes | Volver atrás tras abrir un detalle desde una lista filtrada. | Anotar si se conservan filtros y página (CE usa la URL). | P2 | UX |
| F10-UX-007 | Búsquedas con retardo | Campos de búsqueda. | No dispara una petición por tecla (debounce). | P3 | UX |
| F10-UX-008 | Selectores con muchos datos | Selector de terceros con > 50 registros. | Permite buscar; trae todos (no se corta a 50). | P1 | UX |
| F10-UX-009 | Teclado en formularios largos | Tab en el registro de báscula, la OC y el ingreso. | Orden de tabulación lógico; Enter no envía formularios por accidente (salvo el diseño de báscula). | P2 | UX |
| F10-UX-010 | Callejones sin salida | Access-denied, 404, error de carga. | Siempre hay una forma de volver (R-ADM-08). | P2 | UX |
| F10-UX-011 | Ayudas y textos de campo | Campos con reglas (placa, motivo ≥ 10, montos). | Texto de ayuda o placeholder que anticipa la regla. | P3 | UX |
| F10-UX-012 | Coherencia de nombres | «Carta porte» vs «documento», «Terceros» vs «Stakeholders», «Depósito» vs «CPI». | Términos del glosario del negocio. | P3 | UX |

### 4.4 Accesibilidad básica (ACC)

| ID | Caso | Verificación | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F10-ACC-001 | Etiquetas de formulario | Inspeccionar campos principales. | Cada campo con etiqueta asociada. | P3 | UX |
| F10-ACC-002 | Contraste | Herramienta de contraste en textos de estado y botones. | Contraste suficiente (AA aproximado). | P3 | UI |
| F10-ACC-003 | Foco visible | Navegar con Tab. | El foco se ve siempre. | P2 | UX |
| F10-ACC-004 | Solo teclado | Completar un ingreso de Vigilancia y un registro de báscula sin ratón. | Posible. | P2 | UX |

### 4.5 Manejo de errores y robustez (ERR)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F10-ERR-001 | API caída | (Local) detener el API y navegar/guardar. | «Error de conexión con el servidor»; sin pantalla en blanco; al volver el API, la app se recupera. | P1 | ERR |
| F10-ERR-002 | Red lenta | DevTools «Slow 3G» en báscula y facturas. | Indicadores de carga; sin envíos duplicados. | P2 | ERR |
| F10-ERR-003 | Errores de negocio (400/409) | 5 errores de módulos distintos. | Se muestra el mensaje del backend una sola vez, en español; sin texto genérico adicional (§G.3 del plan de paridad). | P1 | ERR |
| F10-ERR-004 | 403 | Ver F9-NAV-003. | Mensaje de permiso, no «Error interno» (R-ADM-02). | P1 | ERR |
| F10-ERR-005 | 404 de entidad | Abrir `/foreign-trade/imports/{id-inexistente}` y `/billing/invoices/{id-inexistente}`. | Mensaje «no existe» y forma de volver. | P2 | ERR |
| F10-ERR-006 | 500 | Provocar un 500 conocido (comprobante de pago, R-FAC-04). | Mensaje genérico controlado sin detalles técnicos en producción. | P2 | ERR |
| F10-ERR-007 | Doble envío | Doble clic en Guardar/Cobrar/Confirmar/Aprobar/Registrar pago/Crear OC/Emitir guía. | Una sola operación. | P0 | PER |
| F10-ERR-008 | Concurrencia de edición | Dos usuarios editan el mismo depósito (CE) o la misma factura. | Anotar: último gana o error de concurrencia; sin datos corruptos. | P2 | PER |
| F10-ERR-009 | Sesión expirada durante un formulario | Dejar un formulario largo abierto > tiempo de token y guardar. | Refresh transparente; lo digitado no se pierde. | P1 | PER |
| F10-ERR-010 | Mensajes con estados en inglés | Reunir los mensajes vistos en las fases 3–6 con «Draft», «Confirmed», etc. | Lista consolidada (R-CE-07). | P3 | UI |
| F10-ERR-011 | Errores de consola | Recorrer las pantallas con la consola abierta. | Sin errores rojos no controlados; lista de advertencias recurrentes. | P2 | ERR |
| F10-ERR-012 | Peticiones fallidas silenciosas | Pestaña Red durante el recorrido. | Ninguna 4xx/5xx sin aviso al usuario (p. ej. métodos inexistentes del §G.4–6 del plan de paridad). | P2 | ERR |
| F10-ERR-013 | Archivos grandes | Subir fotos, soporte de OC, CSV de ciudades en el límite y por encima. | Mensajes claros de límite; sin 500. | P2 | ERR |

### 4.6 Rendimiento percibido (PRF)

| ID | Caso | Medición | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F10-PRF-001 | Carga de pantallas | Tiempo hasta interactiva de las 10 pantallas más usadas. | < 3 s en local; anotar staging. | P2 | UX |
| F10-PRF-002 | Báscula completa | Cronometrar 3 ingresos IMP completos (registro → tiquete) con datos precargados. | Anotar tiempos y comparar con la meta (~30 s legacy hasta el primer peso, DF2). | P1 | UX |
| F10-PRF-003 | Listas grandes | Facturas y movimientos con > 200 filas. | Paginación fluida; filtros < 2 s. | P3 | UX |

## 5. Criterios de salida específicos

- F10-RES-001, F10-UX-003 y F10-ERR-007 ejecutados.
- Lista consolidada de observaciones de UX priorizadas (alta/media/baja) para el usuario.

## 6. Entregables

Informe con capturas por resolución, lista priorizada de observaciones, defectos. Detenerse.
