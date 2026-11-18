## Vista de levantes

Rediseño de la vista legacy de levantes de un depósito. Los levantes se agrupan por mercancía. Cada mercancía tiene un encabezado con su ingreso (cantidad y peso), debajo sus levantes y al final el nacionalizado y el saldo. El operario registra un levante agregando una fila dentro de la misma tabla.

### Tabla de levantes agrupada por mercancía (componente compartido)

**Columnas**

| Columna | Descripción |
|---|---|
| Nº levante | Número del levante DIAN |
| Nº aceptación | Número de aceptación |
| Fecha levante | Fecha del levante |
| Tasa | Tasa del levante (T.Lvte) |
| CIF (USD) | Valor CIF |
| Cantidad | Cantidad nacionalizada, en la unidad de la mercancía |
| Peso (kg) | Peso nacionalizado |
| Acciones | Ver documento, editar, eliminar |

**Bloque por mercancía (de arriba abajo)**

1. **Encabezado de ingreso:** nombre de la mercancía, unidad (sacos, bultos…), estado (Sin levante / Parcial / Nacionalizado), cantidad y peso de ingreso alineados bajo las columnas Cantidad y Peso.
2. **Filas de levantes:** una fila por levante.
3. **Agregar levante:** botón que abre una fila editable con los campos del levante. Muestra el saldo disponible (ej. "saldo 32 bultos · 1.170,00 kg"). La fila editable tiene los botones Guardar y Cancelar.
4. **Nacionalizado:** cantidad y peso.
5. **Saldo:** cantidad y peso. Si hay diferencia de peso, se muestra al lado.

### Vista 1 — Pestaña "Levantes" en el detalle del depósito [Mockup](./levante_detalle_deposito/)

Se muestra dentro del detalle del depósito, que ya tiene la información principal. Esta pestaña solo muestra los levantes.

- **Encabezado:** título "Levantes", botones **Exportar** y **Nuevo levante**.
- **Resumen del depósito (4 tarjetas):**

| Tarjeta | Campos |
|---|---|
| Ingreso | Cantidad, peso |
| Nacionalizado | Cantidad, peso, % y barra de avance |
| Saldo en bodega | Cantidad, peso |
| Levantes | Total de levantes, nº de mercancías, mercancías completas |

- **Alerta de diferencia de peso:** franja visible cuando lo nacionalizado no cuadra con el peso de ingreso.
- **Tabla de levantes agrupada por mercancía.**

### Vista 2 — Depósitos y levantes (maestro-detalle con row expansion) [Mockup](./levantes_vista_general/)

**Barra de filtros** (o Filtros por columnas)

- Búsqueda: depósito, documento comercial, importador, mercancía o Nº de levante.
- Filtro por estado: Todos / Sin nacionalizar / Parcial / Nacionalizados, con su conteo.
- Botón "Con diferencia de peso".

**Columnas de la fila maestra**

| Columna | Campos |
|---|---|
| (expandir) | Botón para expandir o contraer |
| Depósito | Número, fecha |
| Documento comercial | Tipo (carta porte), número, manifiesto DIAN |
| Terceros | Importador (nombre y NIT), transportadora |
| Mercancía | Mercancía principal y "+N" si hay más |
| Ingreso | Cantidad con unidad, peso (kg) |
| Nacionalizado | "X / Y unidad", % y barra de avance |
| Saldo | Cantidad con unidad, peso (kg) |
| Estado | Sin nacionalizar / Parcial / Nacionalizado; debajo, Δ peso o nº de levantes |

**Fila expandida**

- Título "Levantes de {depósito}", con el nº de levantes y la tasa de ingreso.
- Enlace "Ver detalle del depósito".
- La tabla de levantes agrupada por mercancía, en versión compacta, con la opción de agregar levantes.

**Pie:** "Mostrando N de M depósitos" y paginación.