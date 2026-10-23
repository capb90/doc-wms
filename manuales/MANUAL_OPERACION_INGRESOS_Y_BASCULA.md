# Manual de operación: Ingresos y Báscula

> **Aviso de vigencia (2026-10-23): parcialmente desactualizado.** Es anterior a la báscula rápida, a la unidad de carga y al selector de conductor. La tarifa de báscula se configura en el servicio `BASCULA`, no en el producto `SRV-BASCULA`. El flujo vigente está en `contexto/contexto-negocio-wms-para-ia.md` §5. Para operarios, la guía actual es `planes/migracion-staging/resultados/guia-pruebas-operarios.md` y los video tutoriales (`videos/`).

Guía para el personal que usa el sistema de ingresos de camiones y el módulo de báscula. Incluye qué configurar antes de empezar y cómo realizar cada operación paso a paso.

---

## Índice

1. [Datos que se deben configurar antes de operar](#1-datos-que-se-deben-configurar-antes-de-operar)
2. [Módulo de ingresos (Vigilancia)](#2-módulo-de-ingresos-vigilancia)
3. [Módulo de báscula](#3-módulo-de-báscula)
4. [Preguntas frecuentes](#4-preguntas-frecuentes)

---

## 1. Datos que se deben configurar antes de operar

Estos datos los configura normalmente un administrador o el área de sistemas. Sin ellos, algunas pantallas no funcionarán o mostrarán errores.

### 1.1 Para el módulo de Ingresos (Vigilancia)

| Qué se necesita | Dónde se configura | Para qué sirve |
|----------------|--------------------|----------------|
| **Motivos de ingreso** | Vienen precargados en el sistema (Descargue importación, Cargue exportación, Solo báscula, Solo bodega, Otro, etc.) | Al registrar un ingreso, el vigilante debe elegir por qué motivo entra el vehículo. |
| **Usuarios con permiso de Vigilancia** | Administración → Usuarios | Solo los usuarios autorizados pueden registrar ingresos y salidas. |
| **Vehículos** | No es obligatorio cargarlos antes. Si la placa no existe, se crea al registrar el primer ingreso. | Cada ingreso se asocia a una placa; si no está en el sistema, se da de alta en ese momento. |

**Resumen:** Para ingresos solo hace falta que existan los motivos (ya vienen en el sistema) y que el usuario tenga permiso. Las placas se pueden ir creando solas al registrar.

---

### 1.2 Para el módulo de Báscula

| Qué se necesita | Dónde se configura | Para qué sirve |
|----------------|--------------------|----------------|
| **Producto “Servicio de Báscula”** | Administración → Productos | El sistema cobra el pesaje usando un producto con código **SRV-BASCULA**. Debe existir y tener un **precio base** (tarifa por pesaje). Sin esto aparece: *"No se encontró tarifa para el servicio de báscula"*. |
| **Precio del servicio de báscula** | En el mismo producto (precio estándar o lista de precios) | Es el valor que se cobra por defecto a todos los clientes. Debe ser mayor a cero. |
| **Convenios (opcional)** | Si su empresa usa convenios por cliente | Permite tener un precio especial por cliente (ej. descuento). Si no hay convenio, se usa el precio estándar del producto. |
| **Stakeholders (partes involucradas)** | Administración → Stakeholders | Deben existir al menos **clientes** (rol Cliente). Para ingreso con depósito también se usan importadores, agencias de importación y empresas de transporte, según el caso. |
| **Roles de negocio** | Vienen precargados (Cliente, Importador, Empresa transportadora) | El sistema filtra stakeholders por rol para mostrar en cada formulario (solo clientes, solo transportadoras, etc.). |
| **Modalidades de operación** | Vienen precargadas (Importación, Exportación, Otros) | Se usan para clasificar la operación (importación, exportación, solo pesaje). |
| **Camiones con ingreso abierto** | Módulo de Ingresos (Vigilancia) | Para usar báscula, el vehículo debe haber **entrado primero** por el módulo de ingresos. Los camiones pendientes de pesaje son los que tienen ingreso registrado pero aún no tienen servicio de báscula asignado. |

**Resumen para báscula:**  
Lo indispensable es: **producto SRV-BASCULA con precio**, **clientes** (stakeholders con rol Cliente) y que los **camiones hayan ingresado** por el módulo de ingresos. El resto (convenios, importadores, etc.) es según necesidad de cada operación.

---

## 2. Módulo de ingresos (Vigilancia)

**Menú:** Vigilancia → Ingreso/Salida  
**Quién lo usa:** Personal de vigilancia o recepción que registra la entrada y salida de vehículos de la planta.

### 2.1 Qué hace este módulo

- Registra **ingreso** de un camión (placa, motivo, observaciones).
- Registra **salida** del mismo camión cuando se va.
- Muestra cuántos camiones hay **actualmente en planta** (ingresos abiertos sin salida).

El ingreso es obligatorio antes de usar la báscula: un camión solo aparece en “Proceso de pesaje” si primero tiene un ingreso registrado.

### 2.2 Registrar un ingreso

1. En **Ingreso/Salida**, pulsar **Registro ingreso**.
2. **Placa:** escribir la placa del vehículo (ej. ABC123) y pulsar **Buscar**.
   - Si la placa existe, se mostrará “Vehículo encontrado”.
   - Si no existe, se indicará “No existe, se creará al registrar”. Eso es correcto; al guardar se creará la placa.
3. **Motivo de ingreso:** elegir en la lista (Descargue mercancía importación, Cargue exportación, Solo báscula, Solo bodega, Otro, etc.).
4. **Observaciones:** opcional (ej. “Trae documentación pendiente”).
5. Si el sistema avisa que **este vehículo ya tiene un ingreso abierto**, no se puede registrar otro hasta que se registre su salida.
6. Pulsar **Registrar ingreso**.

Listo: el camión queda “dentro” de planta y podrá ser elegido después en el proceso de pesaje.

### 2.3 Registrar una salida

1. En **Ingreso/Salida**, pulsar **Registro salida**.
2. **Placa:** escribir la placa y pulsar **Buscar**.
3. Si hay un ingreso abierto para esa placa, se mostrará la fecha/hora de ingreso y el motivo.
4. Pulsar **Registrar salida**.

El ingreso queda cerrado y el camión ya no cuenta como “en planta”.

### 2.4 Historial de ingresos

**Menú:** Vigilancia → Historial  

Ahí se puede consultar ingresos y salidas ya registrados (filtros por fecha, placa, etc.).

---

## 3. Módulo de báscula

**Menú:** Báscula → Proceso de Pesaje  
**Quién lo usa:** Operario de báscula que registra pesos y factura el servicio.

### 3.1 Tipos de operación

El proceso de pesaje tiene **tres tipos de operación**:

| Tipo | Nombre en pantalla | Documento principal | Nº de pesajes | Uso típico |
|------|--------------------|----------------------|---------------|------------|
| **A** | Solo Báscula | Ninguno (opcional) | 1 | Solo se pesa el vehículo, no hay depósito ni salida de mercancía. |
| **B** | Ingreso con Depósito | Carta porte (obligatoria) | 2 (bruto y tara) | Entrada de mercancía para almacenar; se crea o se asocia a un depósito por carta porte. |
| **C** | Salida de Mercancía | Orden de cargue (obligatoria) | 2 (tara y bruto) | Salida de mercancía ya almacenada; debe haber orden de cargue y stock. |

El sistema guía en varios pasos: elegir camión → tipo de operación → formulario según tipo → pago → captura de peso(s).

### 3.2 Flujo general (todos los tipos)

1. **Paso 1 – Seleccionar camión**  
   Se muestra la lista de camiones que tienen **ingreso abierto** y **aún no tienen** un servicio de báscula asignado.  
   Seleccionar el vehículo a pesar.

2. **Paso 2 – Tipo de operación**  
   Elegir una de las tres tarjetas: **Solo Báscula**, **Ingreso con Depósito** o **Salida de Mercancía**.

3. **Paso 3 – Formulario de la operación**  
   Según lo elegido, se pide la información necesaria (cliente, carta porte, orden de cargue, etc.). Ver detalle por tipo más abajo.

4. **Paso 4 – Facturación y pago**  
   Se muestra el valor a cobrar (según tarifa o convenio) y se procesa el pago. Al confirmar, se genera la factura y el ciclo queda listo para pesar.

5. **Paso 5 – Captura de peso**  
   - **Solo Báscula:** un solo peso y termina.  
   - **Ingreso con Depósito / Salida de Mercancía:** dos pesos (primer peso y segundo peso según indique la pantalla).

Al terminar el último peso, el proceso finaliza y el camión puede seguir su flujo (salida por vigilancia cuando corresponda).

### 3.3 Operación A – Solo Báscula

- **Documento:** ninguno obligatorio.  
- **Datos en pantalla:**  
  - **Cliente** (obligatorio): elegir de la lista.  
  - Peso esperado y observaciones: opcionales.  
- **Pesajes:** 1.  
- **Uso:** cuando el camión solo pasa a pesarse, sin crear depósito ni sacar mercancía.

### 3.4 Operación B – Ingreso con Depósito

- **Documento:** **Carta porte** (obligatoria).  
  - Se puede **buscar** por número de carta porte: si ya existe un depósito con esa carta, el sistema lo indica y asocia el camión a ese depósito; si no existe, se creará uno nuevo al continuar.
- **Modalidad:** Importación (IMP) o Exportación (EXP).  
- **Datos en pantalla:**  
  - Carta porte, modalidad, **cliente** (obligatorios).  
  - Manifiesto de carga (número, peso, embalaje, cantidad): opcional.  
  - Importador, agencia de importación, empresa de transporte: opcionales.  
  - Producto, descripción, cantidad esperada, unidad de medida, valor de la carga, moneda, observaciones: según necesidad.  
- **Pesajes:** 2 (primero peso bruto, luego tara).  
- **Uso:** entrada de mercancía para almacenar; el primer camión con esa carta porte crea el depósito; los siguientes se asocian al mismo.

### 3.5 Operación C – Salida de Mercancía

- **Documento:** **Orden de cargue** (obligatoria).  
  - Debe **buscar** la orden por número; el sistema valida que exista y que haya stock disponible para el cliente.
- **Modalidad:** según operación (ej. OUTPUT).  
- **Datos en pantalla:**  
  - Número de orden de cargue, modalidad, **cliente** (obligatorios).  
  - Observaciones: opcional.  
- **Pesajes:** 2 (orden según pantalla: tara y bruto, o como indique el flujo).  
- **Uso:** salida de mercancía que ya está en depósito; debe haber orden de cargue válida y stock.

### 3.6 Repesaje e historial

- **Báscula → Repesaje:** para casos en que se deba registrar un repesaje (según configuración de su instalación).  
- **Báscula → Historial:** consulta de operaciones de pesaje ya realizadas (fechas, placas, clientes, pesos, etc.).

---

## 4. Preguntas frecuentes

**¿Por qué no me aparece ningún camión en el proceso de pesaje?**  
Porque solo se listan vehículos con **ingreso abierto** y **sin servicio de báscula** asignado. Hay que registrar primero el ingreso en Vigilancia → Ingreso/Salida.

**¿Qué hago si me dice "No se encontró tarifa para el servicio de báscula"?**  
Falta configurar el producto de báscula: en Administración → Productos debe existir un producto con código **SRV-BASCULA** y un **precio base** (tarifa) mayor a cero. Si su empresa usa convenios por cliente, además puede configurar un precio especial en el convenio.

**¿La carta porte y la orden de cargue se crean en el sistema?**  
No. La carta porte y la orden de cargue son documentos que ya trae el cliente o la operación. En el sistema solo se **registran** (número, y en ingreso con depósito los datos de manifiesto/carga que se pidan) para asociar el pesaje al depósito o a la orden.

**¿Puedo cancelar una operación de báscula ya iniciada?**  
Según el diseño actual, una vez pasada cierta etapa (después de iniciar la operación) no se puede cancelar; debe completarse el proceso. Para casos especiales (error, duplicado, etc.) conviene consultar con el administrador o soporte.

**¿Los motivos de ingreso se pueden cambiar o agregar?**  
Los motivos vienen precargados en el sistema. Si necesita nuevos motivos o cambiar textos, debe solicitarlo al área de sistemas o administración (cambio en base de datos o parámetros).

---

*Documento pensado para operarios y supervisores. Para detalles de configuración técnica (APIs, base de datos, convenios) consulte la documentación técnica o al equipo de sistemas.*
