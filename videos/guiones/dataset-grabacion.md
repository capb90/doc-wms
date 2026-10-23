# Ambiente y dataset de grabación — Video tutoriales WMS v2.0

> **Fecha:** 7 de octubre de 2026. **Estado:** propuesta aprobada en el checkpoint del 7-oct-2026; **pendiente de preparar** (con otro encargo).
> **Para qué sirve:** que cada guion de `guiones-video-tutoriales.md` tenga datos ficticios listos y que cada video deje preparados los datos del siguiente.
> **Regla del documento de guiones (§A.2):** usa un cliente y productos ficticios; no muestres datos reales. **Nunca se graba en staging**: tiene clientes, conductores, vehículos y depósitos reales del legacy.

## 1. Ambiente

| Pieza | Propuesta |
|---|---|
| Base de datos | PostgreSQL local **nueva y vacía**, solo para grabar (p. ej. `wms_grabacion`). Puede ser el `postgres-db` de `compose.yaml` con otro nombre de base. |
| Esquema | El build actual de `develop`: `dotnet ef database update --project Wms.Infrastructure --startup-project Wms.Api`. Quedan los catálogos sembrados (§2.1). |
| API | `Wms.Api` en `http://localhost:5281`, con `ASPNETCORE_ENVIRONMENT=Development`. Administrador inicial con `Bootstrap:AdminUsername` y `Bootstrap:AdminPassword` (variables de entorno; no se escriben aquí). |
| Frontend | `Frontend/wms` con `NUXT_PUBLIC_API_BASE=http://localhost:5281/api/v1` y `npm run dev` (`http://localhost:3000`). `Frontend:BaseUrl` del API = `http://localhost:3000`. |
| Correo | Un buzón local de pruebas (p. ej. Mailpit: SMTP `localhost:1025`, bandeja web `localhost:8025`) en la sección `Email`, para grabar 0.3. Ningún correo sale a Internet. |
| TRM de la DIAN | Normal (`DianTrm:BaseUrl` = `https://www.datos.gov.co`). Solo para preparar el depósito de 3.9 se apunta a una dirección que no responde (p. ej. `http://127.0.0.1:9`), se confirma ese depósito y se restablece. |
| Navegador | Ventana limpia a 1920 × 1080 (1080p), zoom 100 %, sin extensiones visibles. Para 0.2 y 1.2, una ventana privada aparte. |
| Fecha de grabación | **D0** = el primer día de grabación del recorrido (Series 4–7). La preparación de mora necesita **D0 − 2** (§5). |

**Contraseñas:** las de las cuentas de §2.2 se definen al preparar el ambiente y se generan al construir el ambiente en `code_workspace/video-tutoriales-trabajo/credenciales.local.json` (fuera de los repositorios, permisos 600; ver `Frontend/wms/tools/video-tutoriales/README.md`). Deben cumplir la política: 8 o más caracteres, mayúscula, minúscula, número y un carácter de `! @ # $ % ^ & * ( ) + { } : < > ?`; el guion, el punto y el guion bajo no cuentan como especiales.

## 2. Datos

**Cómo leer las tablas:**
- **ID:** la clave que citan los REQUISITOS de los guiones (p. ej. «dataset T1»).
- **Se crea en:** el guion que lo crea en cámara, o «PREP-n» si se prepara antes, fuera de cámara (§4).
- **Lo usan:** los guiones que lo necesitan.

**Reglas de lo ficticio:**
- Los terceros llevan «Demo» en el nombre y NIT del rango `999000101`–`999000199`.
- Los documentos llevan el prefijo `DEMO-`: carta porte `DEMO-CP-…`, orden externa `DEMO-OC-…`, N.º SIIGO `DEMO-FE-…`, pagos `DEMO-PAGO-…`, levantes `LEV-DEMO-…` y aceptaciones `ACE-DEMO-…`.
- Los conductores llevan «Demo» como primer apellido y cédulas del rango `1000000101`–`1000000199`.
- Las placas son `VID101`–`VID115` (aspecto colombiano) y `PVD1001` (aspecto ecuatoriano), siempre sin guion. El sistema solo exige de 3 a 20 letras, números o guiones; «PVD-1001» y «PVD1001» serían dos vehículos distintos.

### 2.1 Lo que trae una base nueva (semilla)

No hay que crearlo:
- **Roles:** «Administrador», «Facturación», «Comercio exterior», «Operario vigilancia», «Operario báscula» y «Operario bodega».
- **Roles de negocio:** «Cliente», «Importador», «Exportador», «Agencia de aduanas» y «Empresa de transporte».
- **Modalidades:** «Importación», «Exportación», «Otros» y «Depósito por Inspección».
- **Servicios:** BASCULA, ALMACENAMIENTO (con IVA), MONTACARGAS, PAPELERIA y GUIA_SALIDA, sin precios.
- **Impuestos:** «Iva» 19 % y «Rete de fuente» 3 %.
- **Valores mínimos de almacenamiento:** en $0.
- **Unidades de medida:** 10.
- **Tipos de unidad de carga:** «Contenedor», «Tanquero» y «Remolque».
- **Motivos de entrada** (sin tildes en la semilla):
  - con pesaje: «Descargue mercancia importacion», «Cargue mercancia importacion», «Cargue mercancia exportacion», «Descargue mercancia exportacion» y «Solo Bascula»;
  - sin pesaje: «Solo bodega» y «Otro».
- **Tipos de documento de envío.**
- **Parámetros:** `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` (vacío) y los seis datos de la empresa.

**No trae:**
- ubicaciones;
- embalajes;
- ciudades ni cuadrillas;
- tarifas de montacargas;
- precios de BASCULA ni de GUIA_SALIDA, ni el IVA de BASCULA.

### 2.2 Cuentas por rol

| ID | Usuario | Nombre completo | Rol | Se crea en | Lo usan |
|---|---|---|---|---|---|
| C1 | `video.admin` | Admin Demo | Administrador | PREP-1 | Serie 1, Serie 2, 0.3, 0.5 |
| C2 | `video.vigilancia` | Vigilancia Demo | Operario vigilancia | PREP-1 | Serie 4 |
| C3 | `video.bascula` | Báscula Demo | Operario báscula | PREP-1 | Serie 5 |
| C4 | `video.bodega` | Bodega Demo | Operario bodega | PREP-1 | Serie 6 |
| C5 | `video.comext` | Comercio Exterior Demo | Comercio exterior | PREP-1 | Serie 7, 0.4, 0.5 |
| C6 | `video.facturacion` | Facturación Demo | Facturación | PREP-1 | Serie 3, 2.1 |
| C7 | `video.nuevo` | Usuario Nuevo Demo | Operario báscula + Facturación | **1.1** | 1.2, 0.2 |

El Admin C1 necesita un correo de la bandeja local (p. ej. `admin.demo@bodega-demo.test`) para 0.3. El parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` apunta a ese mismo correo (se edita en 1.13; lo exige el CE-7 de 7.6).

### 2.3 Terceros

| ID | Nombre | Identificación | Roles de negocio | Configuración de facturación | Se crea en | Lo usan |
|---|---|---|---|---|---|---|
| T1 | Comercializadora Andina Demo S.A.S. | NIT 999000101 | Cliente, Importador | «Mensual (mes calendario)», 30 días, «Por servicio», límite $50.000.000 (en **3.1**) | **1.3** (con la cuenta «Banco Demo · Ahorros · 000111222» y el contacto «Ana Demo Ruiz · ana.ruiz@andina-demo.test · 3000000101 · Colombia») | Series 2–7 |
| T2 | Distribuidora Nariño Demo S.A.S. | NIT 999000102 | Cliente, Importador | «Quincenal (15 días)», 30 días, «Consolidada», sin límite | PREP-2 | 2.9, 2.10, 5.6, 5.8, 7.10, 7.12 |
| T3 | Agencia de Aduanas Demo Nivel 1 S.A.S. | NIT 999000103 | Agencia de aduanas | — | PREP-2 | 5.3, 7.2, 7.10 (emisor) |
| T4 | Transportes Frontera Demo Ltda. | NIT 999000104 | Empresa de transporte | — | PREP-2 | 5.x (Empresa Transportista) |
| T5 | Exportadora Pacífico Demo S.A.S. | NIT 999000105 | Cliente, Exportador | «Mensual (mes calendario)», 30 días, «Por servicio», sin límite | PREP-2 | 7.1, 3.5, 3.6 |
| T6 | Cliente Moroso Demo S.A.S. | NIT 999000106 | Cliente | «Mensual (mes calendario)», **0 días**, «Por servicio», límite **$10.000** | PREP-2 | 5.4, 3.12 |

### 2.4 Productos y catálogos

| ID | Dato | Valores | Se crea en | Lo usan |
|---|---|---|---|---|
| E1 | Tipo de embalaje | Código `SACO`, nombre «Saco» | **1.4** (con «+» en el producto) | P1 |
| P1 | Producto | «Cebolla cabezona», unidad «Bulto», embalaje «Saco» | **1.4** | Series 5–7 |
| P2 | Producto | «Aceite de palma a granel», unidad «Litro» | PREP-2 | 5.6 (unidad de carga) |
| P3 | Producto | «Llantas para camión», unidad «Unidad» | PREP-2 | 5.3, 7.5, 7.6, 7.10 |
| M1 | Unidad de medida | `GALON` «Galón» | **1.5** | — (solo demostración) |
| M2 | Tipo de unidad de carga | `ISOTANQUE` «Isotanque» | **1.5** | — (solo demostración) |
| U1–U2 | Ubicaciones | `A01-R01-N01` «Pasillo A - Rack 01 - Nivel 01» (5.000 kg) y `PATIO-01` «Patio Principal» (50.000 kg, zona especial) | **1.10** | 6.2, 6.4, 6.7 |
| U3–U5 | Ubicaciones | `A01-R01-N02`, `B01-R01-N01` (disponibles) y `A01-R02-N01` (**no disponible**) | PREP-3 | 6.7 |
| K1 | Ciudad | «PASTO», COL, «Nariño», 1 día de tránsito | **1.12** | 7.10, 7.12 |
| K2 | Ciudad | «QUITO», ECU, «Pichincha», 2 días | **1.12** | — |
| K3 | Ciudad | «BOGOTA», COL, «Cundinamarca», 3 días, **destino de abandono** | PREP-3 | 7.15 |
| Q1 | Cuadrilla | «Cuadrilla A» | **1.12** | 6.2, 6.6 |
| Q2 | Cuadrilla | «Cuadrilla B» | PREP-3 | 7.10 |
| MV1 | Motivo de entrada | «Entrega de documentos», sin «Requiere Pesaje» | **1.11** | — (solo demostración) |

### 2.5 Servicios y tarifas (los mismos importes de staging)

| ID | Dato | Valores | Se crea en | Lo usan |
|---|---|---|---|---|
| S1 | BASCULA | IVA 19 % y precio base **$16.806,72** (el video 1.6 se grabó con $16.807 porque el campo aún no admitía centavos) vigente desde D0 − 3 o antes: total **$20.000** | **1.6** | Serie 5 |
| S2 | GUIA_SALIDA | Precio base **$15.000** (sin IVA) | PREP-3 | 7.12 |
| S3 | PAPELERIA | Precio base **$10.000** | PREP-3 | 2.10 (servicio complementario) |
| S4 | Tarifa base de ALMACENAMIENTO | «Porcentaje del valor declarado (sin prorrateo)», tipo de depósito «Importación», «Porcentaje» 0,295, «Mínimo a cobrar ($)» 50.000 con «El mínimo incluye IVA» marcado | **1.7** | Depósitos de clientes sin acuerdo |
| S5 | Valores mínimos | Importación **$50.000** «Con IVA incluido» (en **1.8**); Exportación **$50.000** «Con IVA incluido» (PREP-3) | 1.8 / PREP-3 | 3.5, 3.6 |
| S6 | Tarifas de montacargas | Tractomula $220.000 · Doble troque $150.000 · Sencillo $140.000 · Turbo $110.000 · Guacal / Estiba $40.000 | **1.9** | 6.5 (Tractomula + IVA = **$261.800**) |
| S7 | Tarifa base para perecederos | «Solo perecederos», «Por umbral de peso (perecederos)», umbral 20.000 kg, mínimo $60.000, $3 por kg | **2.6** | — |

### 2.6 Acuerdos (convenios)

| ID | Cliente | Referencia y nombre | Servicios | Estado | Se crea en |
|---|---|---|---|---|---|
| A0 | T1 | `CONV-DEMO-000` «Convenio 2025 Andina Demo» | ALMACENAMIENTO, Importación, «Fijo» $80.000 | **Activo** (se archiva en 2.8) | PREP-4 |
| A1 | T1 | `CONV-DEMO-001` «Convenio 2026 Andina Demo» | (1) ALMACENAMIENTO, Importación, «Porcentaje del valor declarado (sin prorrateo)» 0,25 %, mínimo $45.000 con IVA; (2) ALMACENAMIENTO, P3 + Importación, 0,20 %, mínimo $30.000 con IVA | Borrador → **Activo** en 2.8 | 2.2 (servicio 1), 2.7 (servicio 2) |
| A2 | T2 | `CONV-DEMO-002` «Convenio almacenamiento Nariño Demo» | ALMACENAMIENTO, Importación, 0,28 %, mínimo $50.000 con IVA; luego MONTACARGAS «Por tipo de vehículo» (Tractomula $200.000, Doble troque $140.000, Sencillo $130.000, Turbo $100.000, Guacal / Estiba $35.000) y PAPELERIA como complementario | **Activo** | 2.9; 2.10 |

### 2.7 Camiones, conductores y documentos

Todos los camiones son de la Empresa Transportista T4, salvo `PVD1001`.

| ID | Placa | Tipo · país | Conductor | Motivo de ingreso | Para qué | Ingreso en |
|---|---|---|---|---|---|---|
| V01 | VID101 | Tractomula · Colombia | Luis Demo Castillo, CC 1000000101 | Descargue mercancia importacion | Primer camión de `DEMO-CP-0001` (T1): P1 600 bultos + P3 40 unidades; manifiesto `MAN-DEMO-0001`, 28.000 kg. En báscula solo se digitan cliente e importador; fecha del documento, agencia, valor (USD 12.000) y moneda los completa CE en 7.2 | **4.1** (vehículo nuevo) |
| V02 | VID102 | Sencillo · Colombia | Mario Demo Benavides, CC 1000000102 | Solo Bascula | Solo báscula para T1, cobro inmediato | PREP-5 |
| V03 | VID103 | Tractomula · Colombia | Jorge Demo Paz, CC 1000000103 | Descargue mercancia importacion | `DEMO-CP-0002` (T2) con unidad de carga Tanquero `TQD9001`: P2 30.000 litros | PREP-5 |
| V04 | VID104 | Doble troque · Colombia | Pedro Demo Ruano, CC 1000000104 | Descargue mercancia importacion | `DEMO-CP-0003` (T1) en modalidad **Inspección**: P1 200 bultos | PREP-5 |
| V05 | VID105 | Tractomula · Colombia | Carlos Demo Erazo, CC 1000000105 | Descargue mercancia importacion | Segundo camión de `DEMO-CP-0001`: P1 400 bultos; sin manifiesto en báscula (CE lo completa en 7.2: `MAN-DEMO-0002`, 18.000 kg) | PREP-5 (antes de 5.7) |
| V06 | VID106 | Tractomula · Colombia | Diego Demo Muñoz, CC 1000000106 | Descargue mercancia importacion | Multidepósito: `DEMO-CP-0004` (T1: P1 300 bultos + P3 20 unidades) y `DEMO-CP-0005` (T2: P1 150 bultos) | PREP-5 |
| V07 | VID107 | Sencillo · Colombia | Hugo Demo Ortiz, CC 1000000107 | Solo bodega | Recepción directa (T1, P1 80 bultos, carta porte `DEMO-CP-0010`) | PREP-5 |
| V08 | VID108 | Tractomula · Colombia | Jaime Demo Revelo, CC 1000000108 | Cargue mercancia importacion | Sale con la orden `DEMO-OC-0001` | PREP-6 (antes de 5.9) |
| V09 | VID109 | — | — | Solo Bascula | Ingreso «equivocado» que 4.4 corrige a **VID110** y a «Solo bodega». En 0.4, VID109 (ya sin ingreso abierto) vuelve a entrar para disparar un aviso en vivo | PREP-6 |
| V11 | VID111 | Sencillo · Colombia | Raúl Demo Cerón, CC 1000000111 | Solo Bascula | Registrada y abandonada antes del cobro (5.10 la descarta) | PREP-5 |
| V12 | VID112 | Tractomula · Colombia | Iván Demo Bravo, CC 1000000112 | Descargue mercancia importacion | `DEMO-CP-0007` (T1, P1 500 bultos), ingreso retrocedido **25 días** (en alerta de abandono) | PREP-7 |
| V13 | VID113 | Sencillo · Colombia | Óscar Demo Guerrero, CC 1000000113 | Solo Bascula | Solo báscula de T1 con «Tiene segundo pesaje» y solo el primer peso («Por repesar»): bloquea la salida en 4.2 y se anula en 5.11 | PREP-6 |
| V14 | VID114 | Tractomula · Colombia | Fabio Demo Rosas, CC 1000000114 | Descargue mercancia importacion | `DEMO-CP-0009` (T1, P3 60 unidades), ingreso retrocedido **35 días** (en abandono) | PREP-7 |
| V15 | VID115 | Sencillo · Colombia | Nelson Demo Pinto, CC 1000000115 | Solo Bascula | Solo báscula «Por facturar» a T6, aprobada y vencida (mora) | PREP-8 |
| V16 | PVD1001 | Tractomula · Ecuador | Galo Demo Andrade, CC 1000000116 | Descargue mercancia exportacion | `DEMO-CP-0006` (T5) en modalidad **Exportación**, P1 400 bultos, valor COP 30.000.000; confirmado sin tarifa: factura al **valor mínimo** | PREP-7 |
| V17 | VID116 | Sencillo · Colombia | Wilson Demo Mora, CC 1000000117 | Descargue mercancia importacion | `DEMO-CP-0008` (T1, P3 10 unidades, valor USD 2.000), confirmado con la DIAN caída: **TRM pendiente** | PREP-9 |

### 2.8 Depósitos esperados (si se respeta el orden de §3)

Los consecutivos dependen del orden en que se registran. Con el orden de §3, los números son estos (si cambian, usa los que muestre la pantalla):

| Documento | Depósito | Estado al grabar la Serie 7 |
|---|---|---|
| `DEMO-CP-0001` (V01 + V05) | 2026BA00001 | Borrador → Confirmado en 7.3 → Nacionalizado en 7.7 |
| `DEMO-CP-0002` (V03, tanquero) | 2026BA00002 | Confirmado y con levante (PREP-10) |
| `DEMO-CP-0003` (V04) | 2026INSP00001 | Confirmado (PREP-10) |
| `DEMO-CP-0004` (V06) | 2026BA00003 | Borrador (7.5, 7.9) |
| `DEMO-CP-0005` (V06) | 2026BA00004 | Borrador (se anula en 7.14) |
| `DEMO-CP-0010` (V07, recepción directa) | 2026INSP00002 | Borrador |
| `DEMO-CP-0007` (V12) | 2026BA00005 | Borrador (en alerta, 7.8) |
| `DEMO-CP-0009` (V14) | 2026BA00006 | Borrador (en abandono, 7.8) |
| `DEMO-CP-0006` (PVD1001) | 2026EXP00001 | Confirmado (factura al valor mínimo) |
| `DEMO-CP-0008` (V17, VID116) | 2026BA00007 | Confirmado (TRM pendiente) |

### 2.9 Órdenes, guías, facturas y archivos

| ID | Dato | Valores | Se crea en |
|---|---|---|---|
| OC1 | Orden de cargue `DEMO-OC-0001`, emisor T3 | 2026BA00001 P1 200 bultos (T1) + 2026BA00002 P2 5.000 litros de la unidad `TQD9001` (T2); vehículo VID108; conductor Jaime Demo Revelo, CC 1000000108 (se agrega con «Agregar Nuevo»); destino PASTO; «Cuadrilla B» | **7.10** |
| OC2 | Orden de cargue `DEMO-OC-0002`, emisor T3 | 2026BA00001 P1 50 bultos; VID108 | PREP-11 (se modifica y cancela en 7.11) |
| G1 | Guía de salida de OC1 | Firmante «Conductor» (dos clientes dueños); cobro «Clientes»: 2 × $15.000 = **$30.000**, «Pendiente por facturar» | **7.12** |
| F-SIIGO | Números SIIGO | `DEMO-FE-0001` (factura de almacenamiento de 2026BA00001), `DEMO-FE-0002` (factura de contado de VID102) | 3.7, 3.4 |
| PAG1 | Pago | Transferencia `DEMO-PAGO-0001` por $50.000 a la factura `DEMO-FE-0001`, con el comprobante `comprobante-demo.pdf` (< 5 MB) | **3.8** |
| PAG2 | Pago | Transferencia `DEMO-PAGO-0002` por $20.000 a la factura `DEMO-FE-0099` de T6 (desbloquea al cliente) | **3.12** |
| ARCH-1 | Fotos de mercancía | 3 fotos JPG de sacos genéricos, sin logos ni personas, cada una < 5 MB | 6.2, 6.6 |
| ARCH-2 | Comprobante | `comprobante-demo.pdf`, una página «COMPROBANTE DE PRUEBA — DATOS FICTICIOS» | 3.8 |
| ARCH-3 | Lista de empaque | `lista-empaque-demo.csv` (§2.10) | 7.9 |
| ARCH-4 | Soporte de la orden externa | `orden-externa-demo.pdf`, una página «ORDEN DE CARGUE DE PRUEBA DEMO-OC-0001» | 7.10 |

### 2.10 Archivo `lista-empaque-demo.csv`

Separador `;`, coma decimal y UTF-8, con una fila de encabezado. Las columnas van en el orden que exige la pantalla:

```
codigo;NOMBRE;CANT_BULTOS;UNID_X_BULTOS;PSO_TOTAL_NETO
DEMO-ART-01;Cebolla cabezona seleccionada;100;1;5000,00
DEMO-ART-02;Llanta radial 295/80 R22.5;10;1;650,00
DEMO-ART-03;Saco de cebolla roja;50;1;2500,00
```

Proveedor: «Proveedor Andino Demo» (se crea en 7.9). Importador: T1.

## 3. Orden de grabación y datos que deja cada paso

Es el plan maestro de la sección A.3 de los guiones. «→» indica lo que deja listo para el paso siguiente.

| Paso | Guion | Graba con | Deja listo |
|---|---|---|---|
| 1 | 1.1 Crear un usuario | C1 | C7 |
| 2 | 1.2 Gestionar la cuenta | C1 | C7 con cambio de contraseña pendiente (para 0.2) |
| 3 | 1.3 Registrar un tercero | C1 | T1 |
| 4 | 1.4 Productos y embalajes | C1 | E1, P1 |
| 5 | 1.5 Unidades y tipos de unidad de carga | C1 | M1, M2 |
| 6 | 1.6 Servicios: IVA y precio base | C1 | S1 |
| 7 | 1.7 Tarifas base de almacenamiento | C1 | S4 |
| 8 | 1.8 Valores mínimos | C1 | S5 (Importación) |
| 9 | 1.9 Tarifas de montacargas | C1 | S6 |
| 10 | 1.10 Ubicaciones | C1 | U1, U2 |
| 11 | 1.12 Ciudades y cuadrillas | C1 | K1, K2, Q1 |
| 12 | 2.1 a 2.10 Acuerdos | C1 (y C6 en 2.1) | A1 activo, A2 activo, S7 |
| 13 | 3.1 Configuración de facturación | C6 | Configuración de T1 |
| 14 | 4.1 Registrar el ingreso | C2 | V01 en la cola de báscula |
| 15 | 5.1 La pantalla de báscula | C3 | — |
| 16 | 5.2 Solo báscula | C3 | Factura de contado de VID102 |
| 17 | 5.3 Ingreso con depósito | C3 | 2026BA00001 en Borrador |
| 18 | 5.4 El cobro | C3 | Cobro «Por facturar» de VID101 |
| 19 | 5.5 Pesos y tiquete, primera toma (primer peso, «Falta llegada a Bodega») | C3 | VID101 «Por repesar» |
| 20 | 6.1 Registrar la llegada | C4 | Llegada de VID101 |
| 21 | 5.5 Pesos y tiquete, segunda toma (segundo peso y tiquete) | C3 | Ciclo de VID101 completo |
| 22 | 6.2 Completar la recepción | C4 | Recepción con diferencia → aviso a CE |
| 23 | 5.6 Unidades de carga e inspección | C3 | 2026BA00002 (tanquero), 2026INSP00001 |
| 24 | 6.3 Recibir unidades de carga | C4 | Tanquero recibido |
| 25 | 5.7 Mismo documento | C3 | VID105 en 2026BA00001 |
| 26 | 5.8 Multidepósito | C3 | 2026BA00003, 2026BA00004, factura en cero |
| 27 | 5.10 Retomar y descartar | C3 | VID111 descartado |
| 28 | 6.4 Recepción directa | C4 | 2026INSP00002 |
| 29 | 6.5 Montacargas | C4 | Factura de montacargas de $261.800 |
| 30 | 7.1 Tablero y Kanban | C5 | — |
| 31 | 7.2 Completar un depósito en Borrador | C5 | 2026BA00001 completo |
| 32 | 7.3 Confirmar y cerrar el ingreso de camiones | C5 | 2026BA00001 Confirmado + factura de almacenamiento |
| 33 | 7.4 Etiqueta y documentos | C5 | — |
| 34 | 7.5 Corregir productos | C5 | 2026BA00003 corregido |
| 35 | 7.7 Levantes | C5 | 2026BA00001 Nacionalizado |
| 36 | 7.8 Abandono y prórrogas | C5 | Prórroga de 2026BA00005 |
| 37 | 7.9 Listas de empaque | C5 | Artículos asociados a 2026BA00003 |
| 38 | 7.10 Crear una orden de cargue | C5 | OC1 |
| 39 | 5.9 Salida de mercancía, primera toma (tara y cobro) | C3 | OC1 «en cargue» |
| 40 | 6.6 Ejecutar la orden de cargue | C4 | OC1 cargada |
| 41 | 7.12 Generar la guía | C5 | G1 |
| 42 | 5.9 Salida de mercancía, segunda toma (repesaje) | C3 | OC1 despachada |
| 43 | 4.2 Registrar la salida | C2 | VID108 fuera |
| 44 | 4.4 Corregir un ingreso | C2 | VID110 corregido |
| 45 | 4.3 Historial | C2 | — |
| 46 | 7.11 Modificar, cancelar y revertir | C5 | OC2 cancelada |
| 47 | 7.13 Guías pendientes e historial | C5 | — |
| 48 | 7.14 Anular un depósito | C5 | 2026BA00004 anulado |
| 49 | 6.7 Inventario y ubicaciones | C4 | Mercancía ubicada |
| 50 | 6.8 Novedades | C4 | Novedad de 2026BA00001 |
| 51 | 6.9 Inventario general e historiales | C4 | — |
| 52 | 5.11 Historial de báscula | C3 | Pesaje de VID113 anulado |
| 53 | 5.12 Reporte de Facturación Diaria | C3 | — |
| 54 | 3.2 a 3.5 | C6 | — |
| 55 | 3.7 Ciclo de vida de la factura | C6 | `DEMO-FE-0001` aprobada |
| 56 | 7.6 Ajuste CE-7 | C5 | Factura `DEMO-FE-0001` recalculada |
| 57 | 3.11 Factura recalculada | C6 | — |
| 58 | 3.6, 3.8, 3.9, 3.10, 3.12, 3.13 | C6 | — |
| 59 | 7.15 Reportes de Comercio Exterior | C5 | — |
| 60 | 1.11 Motivos, conductores y vehículos | C1 | MV1 |
| 61 | 1.13 Auditoría y parámetros | C1 | Parámetro de correo configurado* |
| 62 | 0.1 a 0.5 Introducción | C7, C1, C5 | — |

\* El parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` se necesita antes de 7.6. Si 1.13 se graba al final, se configura en PREP-3 y 1.13 lo muestra ya lleno.

## 4. Preparación fuera de cámara

| PREP | Cuándo | Qué | Con |
|---|---|---|---|
| PREP-1 | Antes de todo | Crear las cuentas C1–C6 desde el Admin inicial y cambiar sus contraseñas temporales. Dar a C1 el correo de la bandeja local. | Admin inicial |
| PREP-2 | Antes de la Serie 2 | Crear T2–T6 (con sus roles) y P2, P3. Configuración de facturación de T2, T5 y T6 (§2.3). | C1, C6 |
| PREP-3 | Antes de la Serie 5 | U3–U5 (marcar `A01-R02-N01` como no disponible), K3, Q2, S2, S3, mínimo de Exportación (S5) y `INVENTORY_ADJUSTMENT_ADMIN_EMAIL`. | C1 |
| PREP-4 | Antes de 2.2 | Acuerdo A0 activo para T1. | C1 |
| PREP-5 | Antes de 4.1 | Ingresos de Vigilancia de V02, V03, V04, V06, V07 y V11 el día D0. V05 entra después del ciclo de V01 (antes de 5.7). V11: registrar en báscula «Solo báscula» y soltarla sin cobrar. | C2, C3 |
| PREP-6 | Antes de 7.10 | V08 con su ingreso de Vigilancia (el vehículo VID108 debe existir para la orden; el conductor se agrega en 7.10). V09: ingreso con placa VID109 y motivo «Solo Bascula», sin báscula. V13: solo báscula de T1 con «Tiene segundo pesaje», cobro inmediato y solo el primer peso. | C2, C3 |
| PREP-7 | Antes de 7.1 | V12 y V14: ingreso, «Corregir ingreso» con la fecha a 25 y 35 días atrás (motivo «Preparación de datos de grabación») y registro en báscula hasta el primer peso. PVD1001: depósito de exportación de T5 con todos los datos de CE, recibido y confirmado (factura al mínimo de Exportación). | C2, C3, C4, C5 |
| PREP-8 | **D0 − 2** | V15: solo báscula para T6 «Por facturar». Facturación asigna `DEMO-FE-0099` y aprueba: con plazo de 0 días vence ese día. El job del día siguiente la marca «Vencida» y bloquea a T6 (deuda $20.000 > límite $10.000). **Verificar en D0 − 1** que T6 aparezca «Bloqueado». | C2, C3, C6 |
| PREP-9 | Antes de 3.9 | Con `DianTrm:BaseUrl` apuntando a una dirección que no responde: ingreso de VID116 con `DEMO-CP-0008` (USD), recepción y confirmación de 2026BA00007. Restablecer la URL de la DIAN y reiniciar el API. | Técnico, C2–C5 |
| PREP-10 | Antes de 7.10 | Terminar los ciclos de VID103 y VID106 (llegadas en Bodega, recepciones y pesajes finales). 2026BA00002 (T2, tanquero) completo, confirmado y con un levante `LEV-DEMO-0002` / `ACE-DEMO-0002` por 30.000 litros. 2026INSP00001 completo y confirmado. | C5 |
| PREP-11 | Antes de 7.11 | OC2 creada por CE (queda «Pendiente»). | C5 |

## 5. Mapa video → datos

Cada guion cita en REQUISITOS los ID de este documento. Resumen por serie:

| Serie | Datos previos clave |
|---|---|
| 0 | C7 con cambio pendiente (0.2); bandeja local y C1 con correo (0.3); avisos de CE guardados (0.4); camiones en etapas distintas en la semana (0.5). |
| 1 | Admin inicial y C1; semilla. |
| 2 | T1, T2 (PREP-2), P1, P3, A0 (PREP-4), S3 (PREP-3). |
| 3 | Facturas de los pasos 16, 18, 26, 29, 32 y 41; T6 bloqueado (PREP-8); 2026BA00007 con TRM pendiente (PREP-9); 2026EXP00001 al mínimo (PREP-7). |
| 4 | Motivos sembrados; V01 nuevo; V09 y V13 (PREP-6); VID108 con guía vigente. |
| 5 | Ingresos de PREP-5 y PREP-6; T1–T4; P1–P3; S1; OC1. |
| 6 | VID101 con primer peso; U1–U5; Q1; S6; V07 (Solo bodega); OC1 «en cargue». |
| 7 | 2026BA00001 en Borrador con aviso de diferencia; T3; K1; Q2; PREP-7, PREP-10, PREP-11; ARCH-3 y ARCH-4. |
