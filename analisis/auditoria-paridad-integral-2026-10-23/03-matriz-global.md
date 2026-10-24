# 03 — Matriz global de paridad

> **Fecha:** 2026-10-23. Auditoría estática (código y documentación; nada se ejecutó; sin Git). Código en disco ese día; según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`.
> **Qué es:** la consolidación de las matrices de los 8 módulos (`modulos/<NN>-<modulo>/06-matriz-paridad.md` y `07-matriz-paridad.csv`), sin repetir el análisis de código.
> **Versión completa:** `04-matriz-global.csv` (todas las filas, las 20 columnas del encargo con su evidencia, y 4 columnas de consolidación: Origen, Nivel, Módulo de auditoría y Clasificación V2). Esta vista en Markdown es **condensada**: deja fuera la evidencia y la trazabilidad, que se consultan en el CSV o en la matriz del módulo.

## 1. Reglas de consolidación

1. **Filas:** 410 filas de módulo (capacidades y desgloses por operación `CF-Lnnn.x`). Se eliminó un duplicado: `CF-L172.c` (reporte general de Bodega), que el módulo 03 dejó `NO_VERIFICADO` y el módulo 07 cerró como `PARCIAL`; queda la fila del 07.
2. **Nivel capacidad:** cuando una capacidad tiene fila propia, manda esa fila. Cuando solo tiene desgloses (p. ej. `CF-L172`, `CF-V030`), su estado por dimensión se agrega así: `NO_VERIFICADO` si algún desglose lo es; `NO_IMPLEMENTADO` si todos lo son; `PARCIAL` si alguno es `PARCIAL` o `NO_IMPLEMENTADO`; `DIFERENCIA_INTENCIONAL` si alguno lo es y el resto está completo; si no, `COMPLETO_CODIGO`. `NO_APLICA` no cuenta salvo que todos lo sean.
3. **V2:** las capacidades V2 reasignadas a una capacidad legacy no cuentan como `SOLO_V2`: `CF-V045` (→ `CF-L134`/`CF-L135`), `CF-V051` (→ `CF-L158`/`L159`/`L162`/`L163`), `CF-V053` (→ `CF-L166`), `CF-V071` (→ `CF-L209`) y `CF-V050`, duplicada de `CF-V036`.
4. **Ajuste del orquestador:** `CF-L172` (consultar ubicación y ocupación) pasa de `NO_VERIFICADO` (módulo 03) a `PARCIAL` por la fila `CF-L172.c` del módulo 07 (BR-07-010). Es el único estado que el orquestador cambió durante la consolidación.
5. **Decisiones posteriores (2026-10-23):** el usuario respondió las 13 preguntas de `06-brechas-priorizadas.md` §3.1 (`docs/contexto/decisiones.md`, DEC-050…054). Las 6 brechas aceptadas (BR-02-001, BR-02-010, BR-04-001, BR-04-002, BR-04-012, BR-08-008) salen de la columna «Brechas» y quedan citadas en «Observaciones». Una fila sin brechas restantes pasa de `PARCIAL` a `DIFERENCIA_INTENCIONAL` en su paridad (`CF-L107`, `CF-L141.a`, `CF-L260`) y de `PARCIAL` a completo en sus dimensiones. Las 7 brechas que se construyen siguen abiertas, con la decisión anotada. **Las matrices de módulo (`modulos/*/07-matriz-paridad.csv`) son la foto previa a las decisiones; esta matriz y `04-matriz-global.csv` las incorporan.**

## 2. Resumen por módulo (nivel capacidad)

| Módulo | Capacidades legacy (incl. no catalogadas) | COMPLETO_CODIGO | DIFERENCIA_INTENCIONAL | PARCIAL | NO_IMPLEMENTADO | NO_VERIFICADO | NO_APLICA | SOLO_V2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 01-administracion-catalogos | 100 | 30 | 45 | 20 | 0 | 0 | 5 | 13 |
| 02-bascula | 23 | 5 | 6 | 12 | 0 | 0 | 0 | 10 |
| 03-vigilancia-bodega | 19 | 5 | 3 | 5 | 0 | 0 | 6 | 10 |
| 04-ce-ingresos-depositos | 25 | 4 | 7 | 11 | 1 | 0 | 2 | 9 |
| 05-ce-levantes-salidas | 30 | 6 | 6 | 13 | 2 | 0 | 3 | 6 |
| 06-facturacion | 23 | 0 | 9 | 14 | 0 | 0 | 0 | 12 |
| 07-reportes-exportaciones | 17 | 3 | 3 | 9 | 0 | 0 | 2 | 1 |
| 08-procesos-infra-fuera-alcance | 39 | 1 | 1 | 0 | 0 | 0 | 37 | 7 |
| **Total** | **276** | **54** | **80** | **84** | **3** | **0** | **55** | **68** |

## 3. Matriz condensada por capacidad

`FE` frontend · `BE` backend · `INT` integración · `RN` reglas de negocio · `Paridad` paridad integral · `Val.` validación ya documentada por QA o migración (`Sí` = la fila cita una ejecución previa; nunca se ejecutó nada en esta auditoría). Abreviaturas de estado: `COMP` COMPLETO_CODIGO · `CON` CONECTADO_CODIGO · `PARC` PARCIAL · `DIF` DIFERENCIA_INTENCIONAL · `NOIMP` NO_IMPLEMENTADO · `NOVER` NO_VERIFICADO · `N/A` NO_APLICA · `MAQ` SOLO_MAQUETADO · `SININT` SIN_INTEGRACION.

### 01-administracion-catalogos

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L001 | Iniciar sesión de operador | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L002 | Cerrar sesión de operador | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L003 | Consultar panel, menú y alertas | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L005 | Consultar ciudades/destinos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L006 | Registrar ciudades/destinos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L007 | Modificar ciudades/destinos | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L008 | Eliminar ciudades/destinos | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L009 | Consultar clientes | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L010 | Registrar clientes | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L011 | Modificar clientes | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L012 | Eliminar clientes | COMP | COMP | CON | PARC | PARC | BR-01-006 | BAJA | Sí |  |
| CF-L013 | Consultar color de vehículo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L014 | Registrar color de vehículo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L015 | Modificar color de vehículo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L016 | Eliminar color de vehículo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L021 | Consultar cuadrillas | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L022 | Registrar cuadrillas | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L023 | Modificar cuadrillas | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L024 | Eliminar cuadrillas | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L025 | Consultar documentos comerciales | N/A | COMP | CON | N/A | DIF | — | — | No |  |
| CF-L026 | Registrar documentos comerciales | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L027 | Modificar documentos comerciales | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L028 | Eliminar documentos comerciales | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L029 | Consultar embalajes | COMP | COMP | CON | PARC | PARC | BR-01-002 | BAJA | Sí |  |
| CF-L030 | Registrar embalajes | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L031 | Modificar embalajes | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L032 | Eliminar embalajes | PARC | PARC | CON | PARC | PARC | BR-01-001 | MEDIA | No |  |
| CF-L033 | Consultar empresas de transporte | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L034 | Registrar empresas de transporte | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L035 | Modificar empresas de transporte | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L036 | Eliminar empresas de transporte | COMP | COMP | CON | PARC | PARC | BR-01-006 | BAJA | Sí |  |
| CF-L037 | Consultar modalidades | N/A | COMP | CON | N/A | PARC | BR-01-002 | BAJA | No |  |
| CF-L038 | Registrar modalidades | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L039 | Modificar modalidades | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L040 | Eliminar modalidades | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L041 | Consultar naturaleza de mercancía | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L042 | Registrar naturaleza de mercancía | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L043 | Modificar naturaleza de mercancía | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L044 | Eliminar naturaleza de mercancía | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L045 | Consultar personas | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L046 | Registrar personas | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L047 | Modificar personas | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L048 | Eliminar personas | COMP | COMP | CON | PARC | PARC | BR-01-006 | BAJA | No |  |
| CF-L049 | Consultar productos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L050 | Registrar productos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L051 | Modificar productos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L052 | Eliminar productos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L053 | Consultar resoluciones | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L054 | Registrar resoluciones | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L055 | Modificar resoluciones | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L056 | Eliminar resoluciones | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L057 | Consultar servicios | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L058 | Registrar servicios | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L059 | Modificar servicios | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L060 | Eliminar servicios | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L061 | Consultar SIA | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L062 | Registrar SIA | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | Sí |  |
| CF-L063 | Modificar SIA | COMP | COMP | CON | PARC | PARC | BR-01-004 | BAJA | No |  |
| CF-L064 | Eliminar SIA | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L073 | Consultar tipos de bodega | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L074 | Registrar tipos de bodega | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L075 | Modificar tipos de bodega | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L076 | Eliminar tipos de bodega | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L077 | Consultar unidades de carga | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L078 | Registrar unidades de carga | COMP | COMP | CON | N/A | DIF | — | — | No |  |
| CF-L079 | Modificar unidades de carga | COMP | COMP | CON | N/A | DIF | — | — | No |  |
| CF-L080 | Eliminar unidades de carga | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L081 | Consultar usuarios internos | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L082 | Registrar usuarios internos | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L083 | Modificar usuarios internos | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L084 | Eliminar usuarios internos | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L085 | Consultar vehículos | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L086 | Registrar vehículos | COMP | COMP | CON | PARC | PARC | BR-01-004, BR-01-005 | BAJA | Sí |  |
| CF-L087 | Modificar vehículos | COMP | COMP | CON | PARC | PARC | BR-01-004, BR-01-005 | BAJA | Sí |  |
| CF-L088 | Eliminar vehículos | COMP | COMP | CON | PARC | PARC | BR-01-006 | BAJA | No |  |
| CF-L089 | Consultar bodegas | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L090 | Registrar bodegas | COMP | COMP | CON | PARC | PARC | BR-01-007 | BAJA | Sí |  |
| CF-L091 | Modificar bodegas | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L092 | Eliminar bodegas | COMP | COMP | CON | PARC | PARC | BR-01-007 | BAJA | No |  |
| CF-L093 | Registrar tipo de documento | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L094 | Eliminar tipo de documento | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L095 | Consultar prefijos | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L096 | Modificar prefijo | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L097 | Cambiar contraseña propia | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L098 | Gestionar permisos de usuario | COMP | COMP | CON | N/A | DIF | — | — | Sí |  |
| CF-L099 | Gestionar usuarios del portal | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L100 | Asignar y desasignar vehículos a convenio | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L101 | Configurar requisitos de modalidad | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L241 | Autocompletar y seleccionar datos de selecciones | COMP | COMP | CON | N/A | DIF | — | — | No |  |
| CF-L242 | Autocompletar y seleccionar datos de clientes | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L243 | Autocompletar y seleccionar datos de personas | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L244 | Autocompletar y seleccionar datos de productos | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L245 | Autocompletar y seleccionar datos de empresas de transporte | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L246 | Autocompletar y seleccionar datos de usuarios | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L247 | Autocompletar y seleccionar datos de vehículos | COMP | COMP | CON | PARC | PARC | BR-01-005 | BAJA | Sí |  |
| CF-L248 | Autocompletar y seleccionar datos de unidades de carga | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L253 | Servir tablas paginadas AJAX | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L256 | Cargar fotografía de ficha | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-LX01-01 | Registrar auditoría de inicio de sesión | N/A | N/A | N/A | N/A | DIF | — | — | No | No catalogada |
| CF-LX01-02 | Registrar auditoría de acciones sobre maestros | COMP | COMP | CON | COMP | COMP | — | — | Sí | No catalogada |
| CF-V001 | Autenticación con JWT (login, refresh, logout) | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V002 | Recuperación y cambio de contraseña | COMP | COMP | CON | N/A | N/A | BR-01-008 | BAJA | Sí | SOLO_V2 |
| CF-V003 | Usuarios con 6 roles y matriz de políticas | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V004 | Consulta de la auditoría genérica | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V005 | Parámetros del sistema | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V006 | Catálogo de unidades de medida (DEC-015) | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V007 | Catálogo de tipos de unidad de carga (DEC-014) | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V008 | Motivos de ingreso | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V009 | Conductores con selector paginado y edición (DEC-017) | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V010 | Terceros con varios roles y alta rápida | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V011 | Panel de inicio por rol | COMP | N/A | N/A | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V012 | Carga masiva de ciudades por CSV con simulación | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V013 | Contactos y cuentas bancarias de terceros | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |

### 02-bascula

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L102 | Consultar y filtrar entradas de báscula | COMP | COMP | CON | COMP | COMP | BR-02-008 | BAJA | No |  |
| CF-L103 | Registrar entrada y pesaje | COMP | COMP | CON | PARC | PARC | BR-02-003, BR-02-006, BR-02-013 | ALTA | No |  |
| CF-L104 | Modificar entrada y pesaje | PARC | PARC | CON | PARC | PARC | BR-02-006, BR-02-007 | ALTA | No |  |
| CF-L105 | Anular entrada | COMP | COMP | CON | PARC | PARC | BR-02-012 | BAJA | Sí |  |
| CF-L106 | Consultar y filtrar salidas de báscula | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L107 | Registrar salida de báscula | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L108 | Modificar salida de báscula | PARC | PARC | CON | PARC | PARC | BR-02-007 | BAJA | No |  |
| CF-L109 | Anular salida de báscula | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L110 | Consultar solo pesajes | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L111 | Registrar solo pesaje | COMP | PARC | CON | PARC | PARC | BR-02-002 | MEDIA | Sí |  |
| CF-L112 | Modificar solo pesaje | PARC | PARC | CON | PARC | PARC | BR-02-007 | BAJA | No |  |
| CF-L113 | Anular solo pesaje | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L114 | Registrar repesaje | COMP | COMP | CON | PARC | PARC | BR-02-015 | BAJA | Sí |  |
| CF-L115 | Ver tiquete y repesaje | COMP | PARC | CON | PARC | PARC | BR-02-005, BR-02-009 | MEDIA | Sí |  |
| CF-L116 | Facturar servicios de báscula | COMP | PARC | CON | PARC | PARC | BR-02-003, BR-02-004, BR-02-017 | BAJA | No |  |
| CF-L117 | Registrar factura SIIGO de tiquete | N/A | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L118 | Cobrar cartera pendiente | N/A | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L119 | Duplicar recibo | COMP | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L120 | Usar tiquete existente | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L121 | Consultar reportes de báscula | PARC | COMP | CON | PARC | PARC | BR-02-009, BR-02-014 | BAJA | No |  |
| CF-L235 | Autocompletar y seleccionar datos de báscula | PARC | PARC | PARC | PARC | PARC | BR-02-004, BR-02-009, BR-02-011, BR-02-018 | BAJA | No |  |
| CF-L255 | Consultar último peso | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-LX02-01 | Atajos de teclado de báscula | PARC | N/A | N/A | PARC | PARC | BR-02-016 | BAJA | No | No catalogada |
| CF-V020 | Cola de camiones de báscula | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V021 | Recuperar operaciones de báscula a medias | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V022 | Pendientes de repesar y en proceso | COMP | N/A | CON | N/A | N/A | BR-02-018 | BAJA | Sí | SOLO_V2 |
| CF-V023 | Tablero de báscula | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V024 | Corrección de ciclo de báscula | COMP | PARC | CON | N/A | N/A | BR-02-006, BR-02-007 | ALTA | No | SOLO_V2 |
| CF-V025 | Flujo perecedero y depósito adicional | PARC | PARC | CON | N/A | N/A | — | — | No | SOLO_V2 |
| CF-V026 | Reporte diario de facturación de báscula | COMP | COMP | CON | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V027 | Documentos de envío del servicio de báscula | COMP | COMP | CON | N/A | N/A | — | — | No | SOLO_V2 |
| CF-V028 | Alta rápida de terceros y transportadoras desde báscula | COMP | COMP | CON | N/A | N/A | — | — | No | SOLO_V2 |
| CF-V029 | Observación del tiquete y reimpresión | COMP | COMP | CON | N/A | N/A | BR-02-007 | BAJA | No | SOLO_V2 |

### 03-vigilancia-bodega

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L168 | Asignar productos a bodega | PARC | COMP | CON | COMP | PARC | BR-03-004, BR-03-006 | BAJA | Sí |  |
| CF-L169 | Ubicar cantidades en posiciones | COMP | COMP | CON | COMP | COMP | — | — | Sí | agregada de desgloses |
| CF-L170 | Asignar vehículos a bodega | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L171 | Secciones y posiciones (cuadrícula y contenido) | PARC | COMP | CON | COMP | PARC | BR-03-007 | BAJA | Sí | agregada de desgloses |
| CF-L172 | Consultar ubicación de un lote | COMP | COMP | CON | PARC | PARC | BR-07-010 | BAJA | Sí | agregada de desgloses; ajuste del orquestador (§1.4) |
| CF-L173 | Registrar observaciones y novedades | COMP | COMP | CON | COMP | COMP | — | — | Sí | agregada de desgloses |
| CF-L174 | Modificar observación/novedad | COMP | COMP | CON | PARC | PARC | BR-03-010 | BAJA | Sí | agregada de desgloses |
| CF-L175 | Registrar avería de vehículo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L176 | Modificar o eliminar avería | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L177 | Consultar e imprimir observación | COMP | PARC | CON | PARC | PARC | BR-03-005 | BAJA | Sí |  |
| CF-L178 | Gestionar fotografías de observación | COMP | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L179 | Consultar órdenes de cargue | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L180 | Completar cargue | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L230 | Registrar entrega por guía (portería) | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L236 | Selector de VIN de bodegas | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L254 | Listas de bodega por filtro | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-LX03-01 | Liberar posiciones al emitir la guía | COMP | COMP | CON | COMP | DIF | — | — | Sí | No catalogada |
| CF-LX03-02 | Eliminar registro de portería | N/A | N/A | N/A | N/A | N/A | — | — | No | No catalogada |
| CF-LX03-03 | Plantilla de autorización imprimible | N/A | N/A | N/A | N/A | N/A | — | — | No | No catalogada |
| CF-V030 | Vigilancia: ingreso de vehículos | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2; agregada de desgloses |
| CF-V031 | Corrección de registros de Vigilancia | COMP | PARC | CON | PARC | N/A | BR-03-001 | MEDIA | Sí | SOLO_V2 |
| CF-V032 | Recepción informativa en Bodega | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V033 | Montacargas: registro de uso | COMP | COMP | CON | PARC | N/A | BR-03-009, BR-03-011 | BAJA | Sí | SOLO_V2; agregada de desgloses |
| CF-V034 | Trazabilidad por placa | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V035 | Inventario de Bodega | PARC | COMP | CON | COMP | N/A | BR-03-007 | BAJA | Sí | SOLO_V2 |
| CF-V036 | Autorizaciones de salida y manifiestos desde Vigilancia | MAQ | COMP | SININT | COMP | N/A | BR-03-003 | BAJA | No | SOLO_V2 |
| CF-V037 | Recepción directa sin báscula | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V038 | Cancelar orden de cargue desde Bodega | COMP | PARC | CON | PARC | N/A | BR-03-002 | MEDIA | Sí | SOLO_V2 |
| CF-V039 | Orden de trabajo de cargue en PDF | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |

### 04-ce-ingresos-depositos

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L122 | Consultar y filtrar ingresos | COMP | COMP | CON | COMP | PARC | BR-04-011 | BAJA | Sí |  |
| CF-L123 | Registrar ingreso | N/A | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L124 | Modificar ingreso | COMP | COMP | CON | PARC | PARC | BR-04-005 | BAJA | Sí |  |
| CF-L125 | Anular ingreso | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L126 | Agregar productos amparados | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L127 | Modificar producto amparado | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L128 | Eliminar producto amparado | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L129 | Consultar listas de empaque | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L130 | Importar lista de empaque | COMP | COMP | CON | PARC | PARC | BR-04-006 | BAJA | Sí |  |
| CF-L131 | Eliminar lista de empaque | COMP | COMP | CON | PARC | PARC | BR-04-006 | BAJA | Sí |  |
| CF-L132 | Asociar artículos de lista a ingreso | COMP | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L133 | Consultar y filtrar depósitos de importación | COMP | COMP | CON | COMP | PARC | BR-04-008, BR-04-011 | BAJA | Sí |  |
| CF-L134 | Consultar depósitos de exportación | COMP | COMP | CON | PARC | PARC | BR-04-011 | BAJA | Sí |  |
| CF-L135 | Registrar depósito | N/A | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L136 | Modificar depósito | COMP | COMP | CON | PARC | PARC | BR-04-005 | BAJA | Sí |  |
| CF-L137 | Eliminar depósito | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L138 | Consultar detalle y seriales de producto | PARC | PARC | CON | NOIMP | PARC | BR-04-009 | BAJA | No |  |
| CF-L139 | Modificar serial de depósito | NOIMP | NOIMP | N/A | NOIMP | NOIMP | BR-04-009 | BAJA | No |  |
| CF-L140 | Consultar y registrar prórroga | COMP | COMP | CON | PARC | PARC | BR-04-003, BR-04-010 | BAJA | Sí |  |
| CF-L141 | Generar y consultar adhesivos | COMP | COMP | CON | PARC | PARC | BR-04-004 | BAJA | Sí |  |
| CF-L142 | Gestionar soportes de depósito | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L237 | Selector de depósitos (VIN no asociado) | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L259 | Conciliar VIN leídos al listar | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L260 | Reactivar depósito con saldo pendiente | N/A | COMP | N/A | COMP | DIF | — | — | No |  |
| CF-LX04-01 | Alerta de abandono en el panel y el menú | COMP | COMP | CON | PARC | PARC | BR-04-003, BR-04-010 | BAJA | Sí | No catalogada |
| CF-V040 | Unidades de carga en el depósito (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V041 | Inspecciones INSP (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V042 | Cierre explícito del ingreso de camiones (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V043 | Fecha de ingreso editable (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V044 | Ajuste de cantidad CE-7 con kárdex (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V045 | Exportaciones EXP como operación propia | COMP | COMP | CON | COMP | N/A | — | — | No | REASIGNADA → CF-L134/CF-L135 |
| CF-V046 | Confirmación del depósito con requisitos y devolución a corrección (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V047 | Validación del depósito contra la plantilla (SOLO_V2) | MAQ | COMP | SININT | NOVER | N/A | BR-04-007, BR-04-008 | BAJA | Sí | SOLO_V2 |
| CF-V048 | Manifiesto por camión y cambio de producto de la línea (SOLO_V2) | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V084 | Alerta diaria de abandono (job, SOLO_V2) | N/A | COMP | CON | PARC | N/A | BR-04-010 | BAJA | No | SOLO_V2 |

### 05-ce-levantes-salidas

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L143 | Consultar y filtrar levantes | PARC | COMP | PARC | COMP | PARC | BR-05-007 | MEDIA | Sí |  |
| CF-L144 | Registrar levante | COMP | COMP | CON | PARC | PARC | BR-05-003, BR-05-012 | MEDIA | Sí |  |
| CF-L145 | Modificar levante | COMP | COMP | CON | PARC | PARC | BR-05-002, BR-05-012 | MEDIA | Sí |  |
| CF-L146 | Eliminar levante | COMP | COMP | CON | PARC | PARC | BR-05-002, BR-05-003 | MEDIA | Sí |  |
| CF-L147 | Asignar productos a levante | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L148 | Asignar VIN a levante | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L149 | Quitar producto o VIN de levante | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L150 | Gestionar soportes de levante | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L151 | Consultar y filtrar salidas de importación | PARC | COMP | CON | COMP | PARC | BR-05-008 | BAJA | Sí |  |
| CF-L152 | Consultar y filtrar salidas de exportación | PARC | COMP | CON | COMP | PARC | BR-05-008 | BAJA | Sí |  |
| CF-L153 | Elegir modalidad de nueva salida | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L154 | Registrar salida de importación | COMP | PARC | CON | PARC | PARC | BR-05-002, BR-05-004, BR-05-013 | MEDIA | Sí |  |
| CF-L155 | Registrar salida de exportación | COMP | PARC | CON | PARC | PARC | BR-05-009 | BAJA | Sí |  |
| CF-L156 | Registrar salida consolidada | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L157 | Registrar salida Colmotores | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L158 | Modificar salida | PARC | PARC | CON | PARC | PARC | BR-05-001, BR-05-005 | MEDIA | Sí |  |
| CF-L159 | Anular salida | PARC | PARC | CON | PARC | PARC | BR-05-001, BR-05-002 | MEDIA | Sí |  |
| CF-L160 | Asignar productos a salida | COMP | COMP | CON | PARC | PARC | BR-05-002 | MEDIA | Sí |  |
| CF-L161 | Asignar VIN a salida | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L162 | Quitar producto o VIN de salida | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L163 | Generar y consultar guía de salida | PARC | PARC | CON | PARC | PARC | BR-05-001, BR-05-006, BR-05-010, BR-05-011 | MEDIA | Sí |  |
| CF-L164 | Autorizar orden de cargue | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L165 | Consultar tiquete de salida | COMP | COMP | CON | COMP | COMP | — | — | No |  |
| CF-L166 | Consultar pesajes globales | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L167 | Gestionar soportes de salida | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L238 | Autocompletar y seleccionar datos de levantes | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L239 | Autocompletar y seleccionar datos de salidas | PARC | COMP | CON | COMP | PARC | BR-05-008 | BAJA | Sí |  |
| CF-L261 | Marcar salida sin mercancía como incompleta | N/A | COMP | N/A | COMP | COMP | — | — | No |  |
| CF-LX05-01 | Bloquear las salidas de un cliente | NOIMP | NOIMP | SININT | NOIMP | NOIMP | BR-05-004 | MEDIA | No | No catalogada |
| CF-LX05-02 | Crear la guía solo con el cargue completo | NOIMP | NOIMP | N/A | NOIMP | NOIMP | BR-05-006 | MEDIA | Sí | No catalogada |
| CF-V050 | Autorización de salida | MAQ | COMP | SININT | N/A | N/A | BR-03-003 | BAJA | No | REASIGNADA → duplicada de CF-V036 |
| CF-V051 | Correcciones de orden de cargue | COMP | COMP | CON | N/A | N/A | — | — | No | REASIGNADA → CF-L158/L159/L162/L163 |
| CF-V052 | Guías pendientes | COMP | COMP | CON | COMP | N/A | BR-05-013 | BAJA | Sí | SOLO_V2 |
| CF-V053 | Salida de la orden con el tiquete de ingreso | COMP | COMP | CON | N/A | N/A | — | — | No | REASIGNADA → CF-L166 |
| CF-V054 | Vista previa y cobro de la guía por cliente dueño | COMP | COMP | CON | NOVER | N/A | BR-05-011 | BAJA | Sí | SOLO_V2 |
| CF-V055 | Cambiar el modo de pago de la guía | COMP | COMP | CON | COMP | N/A | BR-05-009 | BAJA | No | SOLO_V2 |
| CF-V056 | Guía por depósito en ZIP con registro de impresión | COMP | COMP | CON | COMP | N/A | BR-05-010 | BAJA | Sí | SOLO_V2 |
| CF-V057 | Orden de cargue externa | COMP | COMP | CON | COMP | N/A | BR-05-005 | MEDIA | Sí | SOLO_V2 |
| CF-V058 | Salida de importación solo con guía y regularización | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |

### 06-facturacion

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L017 | Consultar convenios | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L018 | Registrar convenio | COMP | PARC | CON | PARC | PARC | BR-06-001 | ALTA | No |  |
| CF-L019 | Modificar convenio | COMP | PARC | CON | PARC | PARC | BR-06-001 | ALTA | No |  |
| CF-L020 | Eliminar convenio | COMP | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L065 | Consultar tarifas | PARC | COMP | CON | COMP | PARC | BR-06-002 | MEDIA | No |  |
| CF-L066 | Registrar tarifa | PARC | COMP | CON | COMP | PARC | BR-06-002 | MEDIA | No |  |
| CF-L067 | Modificar tarifa | PARC | COMP | CON | COMP | PARC | BR-06-002 | MEDIA | No |  |
| CF-L068 | Eliminar tarifa | PARC | COMP | CON | COMP | PARC | BR-06-002 | MEDIA | No |  |
| CF-L069 | Consultar tasas de cambio | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L070 | Registrar tasa de cambio | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L071 | Modificar tasa de cambio | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L072 | Eliminar tasa de cambio | N/A | N/A | N/A | N/A | DIF | — | — | No |  |
| CF-L201 | Depósitos por facturar | COMP | PARC | CON | PARC | PARC | BR-06-003, BR-06-013, BR-06-014 | MEDIA | No |  |
| CF-L202 | Facturar período en SIIGO | PARC | PARC | CON | PARC | PARC | BR-06-004, BR-06-005, BR-06-006, BR-06-007 | ALTA | No |  |
| CF-L203 | Facturas emitidas | PARC | COMP | CON | COMP | PARC | BR-06-008, BR-06-013 | BAJA | Sí |  |
| CF-L204 | Modificar factura | COMP | COMP | CON | PARC | PARC | BR-06-006, BR-06-007 | MEDIA | Sí |  |
| CF-L205 | Anular factura | COMP | COMP | CON | COMP | DIF | — | — | Sí |  |
| CF-L206 | Informe de facturación | COMP | PARC | CON | PARC | PARC | BR-06-006 | MEDIA | Sí |  |
| CF-L207 | Informe por CPI | PARC | COMP | CON | COMP | PARC | BR-06-006, BR-06-009, BR-06-013 | MEDIA | Sí |  |
| CF-L234 | Recalcular períodos (cron) | N/A | PARC | N/A | PARC | PARC | BR-06-005, BR-06-010 | MEDIA | No |  |
| CF-L249 | Consulta de tasa de cambio (AJAX) | N/A | COMP | SININT | COMP | DIF | BR-06-011 | BAJA | No |  |
| CF-L251 | Selector de depósito | PARC | COMP | CON | PARC | PARC | BR-06-009 | BAJA | No |  |
| CF-LX06-01 | Alerta de TRM desactualizada | N/A | COMP | CON | COMP | DIF | — | — | No | No catalogada |
| CF-V060 | Motor de acuerdos y fórmulas | COMP | PARC | CON | PARC | N/A | BR-06-001, BR-06-004, BR-06-011 | ALTA | Sí | SOLO_V2 |
| CF-V061 | Ciclos de facturación configurables | COMP | COMP | CON | PARC | N/A | BR-06-010 | BAJA | Sí | SOLO_V2 |
| CF-V062 | Pagos y conciliación diaria | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V063 | Detección de mora y bloqueo | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V064 | Aviso de vencimiento de facturas | N/A | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V065 | Refacturación de una factura anulada | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V066 | TRM de la DIAN al crear la factura | N/A | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V067 | Cierre automático y renovación de períodos | N/A | PARC | CON | PARC | N/A | BR-06-004, BR-06-005, BR-06-011 | ALTA | Sí | SOLO_V2 |
| CF-V068 | Tablero de facturación | COMP | PARC | CON | PARC | N/A | BR-06-012 | BAJA | Sí | SOLO_V2 |
| CF-V069 | Sobrescritura del total de una línea | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |
| CF-V06A | Factura consolidada por cliente | COMP | PARC | CON | PARC | N/A | BR-06-012 | BAJA | Sí | SOLO_V2 |
| CF-V06B | PDF interno de la factura | COMP | COMP | CON | COMP | N/A | — | — | Sí | SOLO_V2 |

### 07-reportes-exportaciones

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L208 | Abrir reportes de importación y exportación | COMP | N/A | N/A | COMP | COMP | — | — | No |  |
| CF-L209 | Kardex de depósito | PARC | PARC | CON | PARC | PARC | BR-07-003, BR-07-004, BR-07-005, BR-07-013 | MEDIA | Sí |  |
| CF-L210 | Diarios de ingreso y salida | PARC | PARC | CON | PARC | PARC | BR-07-001, BR-07-002, BR-07-003, BR-07-004 | MEDIA | No |  |
| CF-L211 | Inventario general | PARC | COMP | CON | PARC | PARC | BR-07-005, BR-07-010 | BAJA | Sí |  |
| CF-L212 | Inventario de vehículos (Colmotores) | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L213 | Mercancía nacionalizada y sin nacionalizar | PARC | PARC | CON | PARC | PARC | BR-07-008 | BAJA | No |  |
| CF-L214 | Prórrogas y salidas en abandono | COMP | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L215 | Pólizas | PARC | PARC | CON | COMP | PARC | BR-07-005, BR-07-006, BR-07-009 | BAJA | Sí |  |
| CF-L216 | Ingresos por producto y cliente | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L229 | Reporte de ingresos por agencia de aduanas (portal SIA) | PARC | COMP | PARC | COMP | PARC | BR-07-011 | BAJA | Sí |  |
| CF-L231 | PDF de reporte o etiqueta | PARC | PARC | CON | PARC | PARC | BR-04-004, BR-07-006 | BAJA | No |  |
| CF-L232 | Excel de reporte | PARC | COMP | CON | PARC | PARC | BR-07-001, BR-07-003, BR-07-005, BR-07-007 | MEDIA | Sí |  |
| CF-L233 | Imprimir documentos y adhesivos | COMP | COMP | CON | COMP | DIF | — | — | No |  |
| CF-L252 | Selector de inventario (bodegas) | COMP | COMP | CON | COMP | COMP | — | — | Sí |  |
| CF-L258 | Código de barras de documentos | N/A | PARC | N/A | PARC | PARC | BR-07-012 | BAJA | No |  |
| CF-LX07-01 | Caché HTML por usuario y descarga sin sesión | COMP | COMP | CON | COMP | DIF | — | — | No | No catalogada |
| CF-LX07-02 | Plantilla de ejemplo de dompdf | N/A | N/A | N/A | N/A | N/A | — | — | No | No catalogada |
| CF-V070 | Estadísticas operativas | COMP | COMP | PARC | N/A | N/A | — | — | Sí | SOLO_V2 |
| CF-V071 | Movimientos de bodega (WarehouseMovementsReportController) | COMP | COMP | CON | N/A | N/A | — | — | No | REASIGNADA → CF-L209 |

### 08-procesos-infra-fuera-alcance

| ID | Funcionalidad | FE | BE | INT | RN | Paridad | Brechas | Crit. máx. | Val. | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CF-L004 | Generar copia de seguridad | N/A | COMP | N/A | COMP | DIF | BR-08-001, BR-08-002 | ALTA | Sí |  |
| CF-L181 | Consultar salidas de patio externo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L182 | Registrar salida de patio externo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L183 | Modificar salida de patio externo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L184 | Asignar y quitar VIN de salida externa | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L185 | Generar guía de patio externo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L186 | Importar y comparar archivo Colmotores | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L187 | Importar plano de voltajes | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L188 | Registrar voltaje de vehículo | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L189 | Consultar y modificar voltajes | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L190 | Gestionar observaciones externas | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L191 | Gestionar soportes de salida externa | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L192 | Leer VIN al ingreso | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L193 | Eliminar lectura de VIN | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L194 | Leer VIN en cargue | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L195 | Quitar VIN de cargue | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L196 | Consultar menú y archivos de seriales | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L197 | Importar seriales de lista de empaque | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L198 | Cargar levantes Colmotores | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L199 | Cargar facturados Colmotores | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L200 | Eliminar archivo importado | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L217 | Iniciar y cerrar sesión de cliente (portal) | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L218 | Consultar almacenamiento (portal) | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L219 | Consultar control de inventario (portal) | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L220 | Consultar control y cumplimiento de entregas | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L221 | Consultar inventario y desglose | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L222 | Consultar antigüedad de vehículos | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L223 | Consultar resumen de facturados | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L224 | Consultar novedades y voltajes | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L225 | Consultar promedio de almacenamiento | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L226 | Consultar ocupación y ubicación de vehículos | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L227 | Consultar reporte por VIN | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L228 | Consultar reporte diario y descargue | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L240 | Autocompletar y seleccionar datos de Colmotores | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L250 | Autocompletar y seleccionar datos de lecturas | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L257 | Autocompletar modelos, salidas y VIN (portal) | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L262 | Migrar placas Colmotores a convenios | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-L263 | Generar base comprimida de actualización Colmotores | N/A | N/A | N/A | N/A | N/A | — | — | No |  |
| CF-LX08-01 | Procesos periódicos del legacy (mecanismo) | N/A | COMP | N/A | N/A | COMP | — | — | No | No catalogada |
| CF-V080 | Respaldos con destinos configurables | N/A | COMP | N/A | COMP | N/A | BR-08-001, BR-08-002 | ALTA | Sí | SOLO_V2 |
| CF-V081 | Importación legacy por CSV con simulación y conciliación | N/A | COMP | N/A | PARC | N/A | BR-08-003, BR-08-004, BR-08-005, BR-08-006, BR-08-007, BR-08-013 | MEDIA | Sí | SOLO_V2 |
| CF-V082 | Notificaciones en tiempo real | PARC | PARC | CON | PARC | N/A | BR-08-010, BR-08-014 | MEDIA | Sí | SOLO_V2 |
| CF-V083 | Centro de ayuda con videos | COMP | N/A | CON | N/A | N/A | — | — | No | SOLO_V2 |
| CF-V085 | SystemController: TRM de la DIAN del día | NOIMP | COMP | SININT | N/A | N/A | BR-08-011 | BAJA | No | SOLO_V2 |
| CF-V086 | Infraestructura de jobs en segundo plano | N/A | PARC | N/A | N/A | N/A | BR-08-012 | BAJA | No | SOLO_V2 |
| CF-V087 | Avisos por correo SMTP a los administradores | N/A | PARC | N/A | PARC | N/A | BR-08-009 | BAJA | No | SOLO_V2 |
