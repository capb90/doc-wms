# Manual de Operación — Módulo de Facturación

> **Aviso de vigencia (2026-10-23): desactualizado. No lo uses como especificación.**
> - No existe creación manual de facturas: el sistema las genera, y Facturación asigna el N.º SIIGO, aprueba, envía y registra pagos.
> - Los períodos de almacenamiento son `Open` y `Closed`, y se cobran por fórmula y por cargo, no con «tarifa diaria».
> Para las reglas vigentes, lee `contexto/contexto-negocio-wms-para-ia.md` §7 y `contexto/decisiones.md`.

## Tabla de Contenido

1. [Descripción General](#1-descripción-general)
2. [Panel Principal (Dashboard)](#2-panel-principal-dashboard)
3. [Gestión de Facturas](#3-gestión-de-facturas)
   - [Listado de Facturas](#31-listado-de-facturas)
   - [Crear Factura](#32-crear-factura)
   - [Detalle de Factura](#33-detalle-de-factura)
   - [Ciclo de Vida de una Factura](#34-ciclo-de-vida-de-una-factura)
4. [Gestión de Pagos](#4-gestión-de-pagos)
   - [Historial de Pagos](#41-historial-de-pagos)
   - [Registrar un Pago](#42-registrar-un-pago)
   - [Verificar o Rechazar un Pago](#43-verificar-o-rechazar-un-pago)
   - [Ciclo de Vida de un Pago](#44-ciclo-de-vida-de-un-pago)
5. [Períodos de Almacenamiento](#5-períodos-de-almacenamiento)
6. [Configuraciones de Facturación](#6-configuraciones-de-facturación)
7. [Referencia Rápida de Estados](#7-referencia-rápida-de-estados)
8. [Preguntas Frecuentes](#8-preguntas-frecuentes)

---

## 1. Descripción General

El módulo de facturación permite gestionar el ciclo completo de facturación de la bodega: desde la creación de facturas hasta el registro y verificación de pagos, incluyendo la configuración de condiciones comerciales por cliente y el seguimiento de períodos de almacenamiento.

### Acceso

Ingrese al módulo desde el menú principal seleccionando **Facturación**, o navegue directamente a `/billing`.

### Secciones del Módulo

| Sección | Descripción |
|---------|-------------|
| **Dashboard** | Vista general con indicadores, acciones rápidas y alertas |
| **Facturas** | Crear, consultar, aprobar, enviar y anular facturas |
| **Pagos** | Registrar, verificar y rechazar pagos de clientes |
| **Períodos de Almacenamiento** | Consultar y cerrar períodos de cobro por almacenaje |
| **Configuraciones** | Definir condiciones de facturación por cliente |

---

## 2. Panel Principal (Dashboard)

Al ingresar al módulo verá el panel de control con la siguiente información:

### Indicadores (KPI)

| Indicador | Qué muestra |
|-----------|-------------|
| **Facturado este mes** | Monto total facturado en el mes en curso |
| **Cartera pendiente** | Monto total que los clientes aún adeudan |
| **Facturas vencidas** | Cantidad de facturas cuya fecha de pago ya pasó |
| **Borradores** | Cantidad de facturas en estado Borrador (aún no aprobadas) |
| **Total facturas** | Cantidad total de facturas en el sistema |

Haga clic en cualquier indicador para ir directamente al listado de facturas filtrado.

### Acciones Rápidas

Desde el dashboard puede acceder rápidamente a:

- **Nueva Factura** — Crear una factura desde cero
- **Historial de Pagos** — Ver y registrar pagos
- **Períodos de Almacenamiento** — Consultar períodos de cobro por almacenaje
- **Configuraciones** — Administrar condiciones de facturación por cliente

### Últimas Facturas

Tabla con las facturas más recientes mostrando número, cliente, monto total y estado. Haga clic en una fila para abrir su detalle.

### Clientes con Mora

Lista de clientes que tienen facturas vencidas, mostrando:
- Nombre del cliente
- Cantidad de facturas vencidas
- Monto total en mora
- Fecha de vencimiento más antigua

---

## 3. Gestión de Facturas

### 3.1 Listado de Facturas

**Ruta:** Facturación → Facturas

Muestra todas las facturas del sistema con filtros para búsqueda eficiente.

#### Filtros disponibles

| Filtro | Descripción |
|--------|-------------|
| **Estado** | Filtra por estado de la factura (Borrador, Aprobada, Enviada, etc.) |
| **Cliente** | Búsqueda por nombre del cliente |
| **N° Factura** | Búsqueda por número de factura |
| **Desde / Hasta** | Rango de fechas de creación |

#### Información en la tabla

- **N° Factura** — Enlace al detalle
- **Cliente** — Nombre del cliente
- **Estado** — Estado actual con código de color
- **Total** — Monto total de la factura
- **Pendiente** — Monto pendiente de pago
- **Vencimiento** — Fecha límite de pago
- **Creada** — Fecha de creación

Use el botón **Limpiar** para restablecer todos los filtros.

---

### 3.2 Crear Factura

**Ruta:** Facturación → Facturas → Nueva Factura

El proceso de creación se divide en **3 pasos**:

#### Paso 1: Información del Cliente

1. **Seleccionar Cliente** (obligatorio): Use el buscador para encontrar al cliente por nombre. El sistema muestra nombre, tipo y número de documento.
2. **Fecha de Vencimiento**: Fecha límite para el pago (opcional).
3. **Período**: Fechas de inicio y fin del período que cubre la factura (opcional).
4. **Notas**: Observaciones visibles para el cliente (opcional).

Haga clic en **Siguiente** para continuar.

#### Paso 2: Items de la Factura

Agregue los conceptos a facturar:

1. Haga clic en **Agregar Item**.
2. Complete los campos por cada concepto:
   - **Descripción** (obligatorio): Detalle del servicio o concepto.
   - **Cantidad** (obligatorio): Número de unidades.
   - **Precio Unitario** (obligatorio): Valor por unidad en COP.
   - **IVA %**: Porcentaje de impuesto aplicable (por defecto 0%).
   - **Notas**: Observaciones del item (opcional).
3. El sistema calcula automáticamente el subtotal, impuesto y total por item.
4. En la parte inferior verá el **subtotal general**, **impuestos** y **total** de la factura.

> Debe agregar al menos un item con descripción, cantidad y precio para continuar.

Haga clic en **Siguiente** para revisar.

#### Paso 3: Confirmar y Crear

Revise el resumen antes de crear:

- Cliente seleccionado
- Fecha de vencimiento
- Cantidad de items
- Total de la factura
- Tabla detallada de items

Si todo es correcto, haga clic en **Crear Factura**. El sistema creará la factura en estado **Borrador** y lo redirigirá automáticamente al detalle.

---

### 3.3 Detalle de Factura

**Ruta:** Facturación → Facturas → (seleccionar factura)

En el detalle encontrará:

#### Información General

- Número de factura y estado actual
- Cliente (nombre y documento)
- Fecha de vencimiento
- Período facturado
- Notas
- Motivo de anulación (si aplica)

#### Items Facturados

Tabla con línea, descripción, cantidad, precio unitario, IVA y total por item.

#### Resumen Financiero

| Campo | Descripción |
|-------|-------------|
| **Subtotal** | Suma antes de impuestos |
| **Impuestos** | Total de IVA |
| **Total** | Monto total de la factura |
| **Pagado** | Monto recibido hasta la fecha |
| **Pendiente** | Monto que falta por cobrar |

#### Pagos Asociados

Lista de pagos registrados para esta factura con: fecha, monto, método de pago, estado y referencia.

#### Historial (Timeline)

Línea de tiempo que muestra los eventos de la factura: creación, aprobación, envío, pago y/o anulación.

#### Acciones Disponibles

Las acciones dependen del estado actual de la factura:

| Acción | Cuándo está disponible | Qué hace |
|--------|----------------------|----------|
| **Aprobar** | Borrador, Pendiente Aprobación | Aprueba la factura para su envío. Registra quién aprobó. |
| **Enviar** | Aprobada | Marca la factura como enviada al cliente. |
| **Registrar Pago** | Enviada, Pago Parcial, Vencida | Abre el formulario para registrar un pago del cliente. |
| **Anular** | Cualquier estado excepto Pagada y Anulada | Anula la factura. Requiere un motivo obligatorio. |
| **Descargar PDF** | Cualquier estado | Genera y descarga el documento de la factura en PDF. |

---

### 3.4 Ciclo de Vida de una Factura

Una factura pasa por los siguientes estados:

```
  ┌──────────┐     ┌───────────────────┐     ┌───────────┐     ┌──────────┐
  │ Borrador │────→│ Pendiente         │────→│ Aprobada  │────→│ Enviada  │
  │ (Draft)  │     │ Aprobación        │     │ (Approved)│     │ (Sent)   │
  └──────────┘     └───────────────────┘     └───────────┘     └────┬─────┘
                                                                     │
                   ┌───────────────────────────────────────────────┐  │
                   │                                               ▼  ▼
              ┌────┴──────┐     ┌───────────────┐     ┌──────────────────┐
              │  Pagada   │◄────│  Pago Parcial │◄────│ Registrar pago   │
              │  (Paid)   │     │(PartiallyPaid)│     │                  │
              └───────────┘     └───────────────┘     └──────────────────┘
                                                              ▲
                   ┌───────────┐                              │
                   │  Vencida  │──────────────────────────────┘
                   │ (Overdue) │  (aún puede recibir pagos)
                   └───────────┘

  * Desde cualquier estado (excepto Pagada/Anulada) se puede → Anular (Cancelled)
  * Una factura pasa a Vencida automáticamente al superar la fecha de vencimiento.
```

#### Descripción de Estados

| Estado | Color | Descripción |
|--------|-------|-------------|
| **Borrador** | Gris | Factura recién creada, editable. Aún no ha sido aprobada. |
| **Pendiente Aprobación** | Amarillo | En espera de aprobación por un usuario autorizado. |
| **Aprobada** | Azul | Aprobada internamente, lista para enviar al cliente. |
| **Enviada** | Cian | Enviada al cliente, en espera de pago. |
| **Pago Parcial** | Naranja | El cliente ha pagado una parte del monto. |
| **Pagada** | Verde | El cliente ha pagado el monto total. Estado final. |
| **Vencida** | Rojo | La fecha de vencimiento pasó sin recibir el pago completo. |
| **Anulada** | Gris oscuro | Factura cancelada con motivo registrado. Estado final. |

---

## 4. Gestión de Pagos

### 4.1 Historial de Pagos

**Ruta:** Facturación → Pagos

Muestra todos los pagos registrados en el sistema, de todas las facturas.

#### Filtros disponibles

| Filtro | Descripción |
|--------|-------------|
| **Estado** | Pendiente, Recibido, Verificado, Rechazado |
| **Buscar cliente** | Búsqueda por nombre del cliente |

#### Información en la tabla

- **Fecha** — Fecha del pago
- **Factura** — Número de factura (enlace al detalle)
- **Cliente** — Nombre del cliente
- **Monto** — Valor del pago
- **Método** — Método de pago utilizado
- **Estado** — Estado actual del pago
- **Referencia** — Número de referencia bancaria

---

### 4.2 Registrar un Pago

Existen **dos formas** de registrar un pago:

#### Opción A: Desde el Historial de Pagos

1. Vaya a **Facturación → Pagos**.
2. Haga clic en **Registrar Pago**.
3. En el diálogo, busque la factura por número o nombre de cliente.
   - Solo aparecen facturas con estado: Enviada, Aprobada, Pago Parcial o Vencida.
4. Seleccione la factura.
5. Complete el formulario de pago.

#### Opción B: Desde el Detalle de la Factura

1. Abra el detalle de una factura con estado Enviada, Pago Parcial o Vencida.
2. Haga clic en **Registrar Pago**.
3. Complete el formulario de pago.

#### Formulario de Pago

| Campo | Obligatorio | Descripción |
|-------|:-----------:|-------------|
| **Monto** | Sí | Valor del pago. No puede superar el saldo pendiente. |
| **Método de Pago** | Sí | Efectivo, Transferencia Bancaria, Cheque, Tarjeta Crédito, Tarjeta Débito u Otro. |
| **Fecha de Pago** | No | Fecha en que el cliente realizó el pago. |
| **Fecha de Consignación** | No | Fecha en que el dinero ingresó a la cuenta bancaria. |
| **Referencia** | No | Número de referencia bancaria o comprobante. |
| **N° Recibo** | No | Número del recibo emitido al cliente. |
| **Notas** | No | Observaciones adicionales sobre el pago. |

> **Importante:** El monto del pago no puede superar el saldo pendiente de la factura.

Al guardar, el pago queda en estado **Pendiente** y la factura se actualiza:
- Si el pago cubre el total pendiente → La factura pasa a **Pagada**.
- Si el pago es parcial → La factura pasa a **Pago Parcial**.

---

### 4.3 Verificar o Rechazar un Pago

Los pagos en estado **Pendiente** o **Recibido** pueden ser verificados o rechazados.

#### Verificar

1. En el Historial de Pagos o en el detalle de la factura, ubique el pago.
2. Haga clic en el botón **✓ Verificar** (ícono verde).
3. El pago cambia a estado **Verificado** y queda registrado quién lo verificó.

#### Rechazar

1. Ubique el pago.
2. Haga clic en el botón **✗ Rechazar** (ícono rojo).
3. El pago cambia a estado **Rechazado**.

---

### 4.4 Ciclo de Vida de un Pago

```
  ┌────────────┐     ┌────────────┐     ┌─────────────┐
  │ Pendiente  │────→│  Recibido  │────→│ Verificado  │
  │ (Pending)  │     │ (Received) │     │ (Verified)  │
  └─────┬──────┘     └─────┬──────┘     └─────────────┘
        │                   │
        │                   │            ┌─────────────┐
        └───────────────────┴───────────→│ Rechazado   │
                                         │ (Rejected)  │
                                         └─────────────┘
```

| Estado | Color | Descripción |
|--------|-------|-------------|
| **Pendiente** | Amarillo | Pago registrado, pendiente de confirmación. |
| **Recibido** | Azul | Pago recibido, pendiente de verificación final. |
| **Verificado** | Verde | Pago confirmado y verificado. Estado final. |
| **Rechazado** | Rojo | Pago rechazado (datos incorrectos, no se confirmó, etc.). Estado final. |

---

## 5. Períodos de Almacenamiento

**Ruta:** Facturación → Períodos de Almacenamiento

Los períodos de almacenamiento representan los ciclos de cobro por almacenaje de mercancía en la bodega. Se generan automáticamente por el sistema.

### Consultar Períodos

La tabla muestra:

| Columna | Descripción |
|---------|-------------|
| **Cliente** | Nombre del cliente propietario de la mercancía |
| **Inicio** | Fecha de inicio del período |
| **Fin** | Fecha de cierre del período |
| **Tarifa Diaria** | Tarifa diaria de almacenamiento en COP |
| **Total** | Monto total calculado del período |
| **Estado** | Abierto, Cerrado o Facturado |
| **Factura** | Enlace a la factura generada (si existe) |

### Filtrar por Estado

- **Abierto**: Período en curso, aún acumulando días de almacenaje.
- **Cerrado**: Período finalizado, listo para facturar.
- **Facturado**: Período que ya fue incluido en una factura.

### Cerrar un Período

1. Ubique un período con estado **Abierto**.
2. Haga clic en el botón **Cerrar**.
3. El período cambia a estado **Cerrado** y queda disponible para ser facturado.

---

## 6. Configuraciones de Facturación

**Ruta:** Facturación → Configuraciones

Permite definir las condiciones de facturación individuales para cada cliente.

### Consultar Configuraciones

La tabla muestra las configuraciones existentes con:

| Columna | Descripción |
|---------|-------------|
| **Cliente** | Nombre del cliente |
| **Ciclo** | Frecuencia de facturación |
| **Días de Pago** | Plazo de pago después de emitir la factura |
| **Preferencia** | Cómo se agrupan los conceptos en la factura |
| **Límite Crédito** | Monto máximo de crédito permitido |
| **Activo** | Si la configuración está activa |

### Crear Nueva Configuración

1. Haga clic en **Nueva Configuración**.
2. Seleccione el **Cliente** usando el buscador.
3. Complete los campos:

| Campo | Descripción | Opciones |
|-------|-------------|----------|
| **Ciclo de Facturación** | Con qué frecuencia se genera la factura | Semanal, Quincenal, Mensual, Bajo demanda |
| **Días de Pago** | Plazo en días para pagar (0–365) | Ejemplo: 30 días |
| **Preferencia de Facturación** | Cómo se agrupan los conceptos | Consolidada, Por servicio, Por ciclo de báscula |
| **Límite de Crédito** | Monto máximo de crédito (opcional) | Valor en COP o dejar vacío para "Sin límite" |

4. Haga clic en **Guardar**.

#### Descripción de Ciclos de Facturación

| Ciclo | Descripción |
|-------|-------------|
| **Semanal** | Se genera una factura cada semana |
| **Quincenal** | Se genera una factura cada quince días |
| **Mensual** | Se genera una factura cada mes |
| **Bajo demanda** | Se genera una factura manualmente cuando se requiera |

#### Descripción de Preferencias

| Preferencia | Descripción |
|-------------|-------------|
| **Consolidada** | Todos los conceptos del período en una sola factura |
| **Por servicio** | Una factura por cada tipo de servicio prestado |
| **Por ciclo de báscula** | Una factura por cada ciclo de báscula completado |

### Editar Configuración Existente

1. En la tabla, haga clic en el ícono de **lápiz** (✏️) de la fila correspondiente.
2. Modifique los campos necesarios.
3. Haga clic en **Guardar**.

> **Nota:** Si un cliente no tiene configuración de facturación, se deberá crear una antes de que el sistema pueda generar facturas automáticas para él.

---

## 7. Referencia Rápida de Estados

### Estados de Factura

| Estado | Indicador | ¿Se puede pagar? | ¿Se puede anular? |
|--------|-----------|:-----------------:|:------------------:|
| Borrador | ⚪ Gris | No | Sí |
| Pendiente Aprobación | 🟡 Amarillo | No | Sí |
| Aprobada | 🔵 Azul | Sí* | Sí |
| Enviada | 🔵 Cian | Sí | Sí |
| Pago Parcial | 🟠 Naranja | Sí | Sí |
| Pagada | 🟢 Verde | No | No |
| Vencida | 🔴 Rojo | Sí | Sí |
| Anulada | ⚫ Gris oscuro | No | No |

*Aprobada: disponible para pago desde el buscador de facturas en el módulo de Pagos.

### Estados de Pago

| Estado | Indicador | ¿Se puede verificar? | ¿Se puede rechazar? |
|--------|-----------|:--------------------:|:-------------------:|
| Pendiente | 🟡 Amarillo | Sí | Sí |
| Recibido | 🔵 Azul | Sí | Sí |
| Verificado | 🟢 Verde | No | No |
| Rechazado | 🔴 Rojo | No | No |

### Estados de Período de Almacenamiento

| Estado | Indicador | ¿Se puede cerrar? |
|--------|-----------|:------------------:|
| Abierto | 🔵 Azul | Sí |
| Cerrado | 🟡 Amarillo | No (ya cerrado) |
| Facturado | 🟢 Verde | No (ya facturado) |

---

## 8. Preguntas Frecuentes

### ¿Puedo editar una factura después de crearla?

Solo se pueden editar las notas e internotes de una factura. Los items y montos no se pueden modificar una vez creada. Si necesita hacer cambios, anule la factura y cree una nueva.

### ¿Qué pasa si registro un pago por el monto total?

La factura cambia automáticamente a estado **Pagada** y ya no se podrán registrar más pagos.

### ¿Puedo registrar varios pagos parciales?

Sí. Puede registrar múltiples pagos parciales hasta cubrir el monto total. La factura permanecerá en estado **Pago Parcial** hasta que el saldo pendiente llegue a cero.

### ¿Qué pasa con una factura vencida?

Una factura vencida aún puede recibir pagos. El estado Vencida es informativo: indica que la fecha de pago ya pasó. El cliente aparecerá en la sección "Clientes con Mora" del dashboard.

### ¿Quién puede aprobar facturas?

Cualquier usuario con acceso al módulo de facturación puede aprobar. El sistema registra automáticamente qué usuario realizó la aprobación para fines de auditoría.

### ¿Puedo anular una factura que ya tiene pagos?

Sí, siempre que la factura no esté en estado Pagada. Deberá ingresar un motivo obligatorio para la anulación.

### ¿Qué es la descarga de PDF?

Genera un documento formal de la factura en formato PDF, listo para enviar al cliente o imprimir.

### ¿Necesito crear una configuración para cada cliente?

Solo si desea que el sistema aplique condiciones específicas (ciclo, plazo, preferencia, límite de crédito) para ese cliente. Los clientes sin configuración pueden recibir facturas manuales sin problema.
