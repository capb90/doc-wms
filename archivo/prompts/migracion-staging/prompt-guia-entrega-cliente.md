Eres el redactor de la **guía rápida de entrega para el cliente** del WMS de Bodegas Asociadas, en **PDF**. Modelo recomendado: **Sonnet 5.5**.

Es un documento **corto y explícito** para los operarios y el administrador del cliente. Muchos operarios **no son técnicos** y algunos tienen un **nivel educativo bajo**: escribe como si se lo explicaras en persona, con frases cortas y una idea por línea.

## Qué debe contener (solo esto)
1. **Cómo entrar y las credenciales** del administrador y de los operarios.
2. **Los datos de práctica P1 a P6:** qué hacer con cada uno, paso a paso y con palabras simples.
3. **Un aviso:** el sistema tiene cargados **datos reales del sistema anterior, del año 2024**, solo para probar.

**Nada más:** sin arquitectura, sin términos técnicos, sin historial del proyecto. **Máximo 4 páginas.**

## Fuentes (léelas, no las copies enteras)
1. `docs/planes/migracion-staging/resultados/guia-pruebas-operarios.md`: la guía completa. Toma de ahí los pasos por rol, los datos de práctica (§4) y las tarifas.
2. `docs/planes/migracion-staging/resultados/informe-fase-5.md`: §5 (cuentas), §6 (datos de práctica) y §11 (pendientes).
3. **Credenciales,** archivos locales fuera de git:
   - `code_workspace/db_legacy/trabajo/credenciales-operarios-staging.local.md`: las contraseñas iniciales de las 5 cuentas `operario.*`;
   - `code_workspace/db_legacy/trabajo/.admin-staging.local`: la contraseña del `admin`.

   **No uses** las cuentas `qa.*` ni `mig.*`: no van en la guía.

## Antes de redactar
1. **Confirma que los datos de práctica siguen en su estado inicial,** con SQL de **solo lectura** en staging (como en la Fase 5) o por el API con el Admin:
   - P1, P2, P3 y P6: los camiones en la cola de báscula «sin iniciar»;
   - P3: la orden 2026OC00004 pendiente;
   - P4: sin levante nuevo;
   - P5: las dos facturas en Borrador.

   **Si alguno ya fue usado, no lo cambies:** avísale al usuario y espera su indicación.
2. **Pregúntale al usuario, en una sola pregunta:**
   - **contacto de soporte:** nombre y teléfono o WhatsApp de quien recibe los problemas;
   - **fecha de entrega** que va en la portada.

   **No inventes el contacto.**

## Estructura del PDF (orden y extensión)

**Página 1 — Bienvenida y cómo entrar**
- **Título:** «WMS Bodegas Asociadas — Guía rápida para probar el sistema».
- **Aviso destacado,** en un recuadro:
  > «Este sistema es de **prueba**. Tiene información real del sistema anterior, del año **2024**, para que practique con datos conocidos. **Nada de lo que haga aquí afecta la operación real.**»
- **La dirección para entrar:** `https://app.100-60-89-139.sslip.io`, grande y fácil de copiar.
- **Cómo entrar, en 4 pasos numerados:**
  1. abrir la dirección;
  2. escribir el usuario;
  3. escribir la contraseña;
  4. **la primera vez, el sistema pide una contraseña nueva: escríbala dos veces y guárdela.**
- **Si olvida su contraseña:** «pídale al administrador que se la restablezca».

**Página 2 — Usuarios y contraseñas**

Una tabla con letra grande:

| Puesto | Usuario | Contraseña inicial |
|---|---|---|
| Administrador | `admin` | *(de `.admin-staging.local`)* |
| Vigilancia (portería) | `operario.vigilancia` | *(del archivo de credenciales)* |
| Báscula | `operario.bascula` | … |
| Bodega | `operario.bodega` | … |
| Comercio Exterior | `operario.comext` | … |
| Facturación | `operario.facturacion` | … |

- **Debajo de la tabla:**
  - «La contraseña es solo suya. No la comparta»;
  - «Escriba la contraseña igual, respetando mayúsculas, minúsculas y signos».
- **Contraseñas legibles:** fuente monoespaciada, con separación entre caracteres. Si una contraseña tiene caracteres que se confunden (`0/O`, `l/1/I`), agrega debajo una línea pequeña que los aclare, por ejemplo «cero, o mayúscula».
- **Esta página es la única con información sensible.** Ponle al pie: «Página confidencial: entregar solo al administrador. Separe esta hoja antes de repartir la guía».

**Páginas 3 y 4 — Para practicar**
- **Una sección por puesto,** con el ícono o la palabra del puesto bien visible.
- **Cada sección:** qué dato de práctica usar y de 3 a 6 pasos numerados con verbos simples («Busque…», «Oprima el botón…», «Escriba…»), usando **los nombres exactos de los botones y pantallas** de la guía completa.
- **Al final de cada sección:** «Al terminar debe ver: …», en una línea.

**Los ejercicios, en orden de uso:**

| Puesto | Ejercicios |
|---|---|
| **Báscula** | **P1:** camión **GLS926**, importación: cobrar, primer peso, segundo peso. **P2:** camión **SRC396**, solo báscula. **P3:** camión **SVO318**, salida con la orden 2026OC00004. |
| **Bodega** | Recibir la mercancía de **GLS926** (P1) y cargar la orden **2026OC00004** en **SVO318** (P3). |
| **Comercio Exterior** | Confirmar el depósito nuevo de P1. Ver el depósito **2024BA00006** sin nacionalizar (P4). Hacer la guía de salida de P3. |
| **Facturación** | Poner el número SIIGO de prueba y aprobar las facturas de **2024BA00001** y **2024BA00003** (P5). |
| **Vigilancia** | Registrar la salida de los camiones cuando terminen. Registrar un ingreso nuevo de práctica. |

- **P6, el camión CAH514, va aparte,** en un recuadro: «**No use este camión.** Está reservado para medir el tiempo de registro con el administrador». **No incluyas** la hoja de tiempos completa.
- **Pie de la última página:**
  - «**Si algo no funciona:** anote la hora, la pantalla y qué hizo, tome una foto de la pantalla y comuníquese con **[contacto que dio el usuario]**»;
  - una línea: «Los datos de práctica dicen **PRÁCTICA**. Los camiones que empiezan por **QS** son ejemplos ya hechos: puede mirarlos para guiarse».

## Estilo (obligatorio)
- **Español sencillo:** frases de menos de 15 palabras.
- **Usa «usted».**
- **Evita palabras técnicas:** nada de «API», «staging», «token», «migración», «sistema legacy», «base de datos», «URL» ni «login». Usa «el sistema», «la dirección», «entrar», «el sistema anterior».
- **Explica los términos del negocio que sí se usan** en una línea entre paréntesis la primera vez que aparecen:
  - **depósito:** la mercancía que entra con un documento;
  - **levante:** el permiso para sacar la mercancía;
  - **orden de cargue:** el pedido para cargar un camión.
- **Formato:**
  - letra de **12 pt o más** (14 pt en las tablas de usuarios), alto contraste y márgenes amplios;
  - pasos con números grandes;
  - **negrita solo para lo que el lector tiene que ver o escribir:** botones, placas, números de depósito;
  - sin capturas de pantalla, salvo que las tomes del staging real y no muestren datos de personas.
- **Datos de personas:** los conductores se nombran como «el conductor del camión», nunca por su nombre. Los clientes de las facturas no se nombran, solo el número de depósito.

## Cómo generar el PDF
- **Escribe la guía en HTML con CSS de impresión** (`@page` tamaño **carta**) y conviértela a PDF con Chrome o Chromium sin interfaz, o con Playwright.
- **Revisa el PDF resultante** antes de entregar:
  - que tenga **4 páginas o menos**;
  - que las tablas no se corten entre páginas;
  - que la página de credenciales quede **sola** en su hoja, para poder separarla.

## Dónde se guarda (obligatorio)
- **El PDF tiene contraseñas:** guárdalo **solo** en `code_workspace/db_legacy/trabajo/entrega/guia-rapida-wms.pdf`, con permisos **600**. Esa carpeta **no es un repositorio**.
- **El HTML fuente con contraseñas** va en la misma carpeta, también con permisos 600.
- **Versión sin contraseñas para git (opcional):** guárdala en `docs/planes/migracion-staging/resultados/guia-rapida-wms-sin-credenciales.pdf`, con la tabla de la página 2 diciendo «la entrega el administrador» en lugar de las contraseñas.
- **No subas, envíes ni publiques el PDF con contraseñas** a ningún servicio: correo, nube, chat ni artefactos. Lo entrega el usuario.
- **En el chat y en cualquier informe, no escribas ninguna contraseña.**

## Entrega
Responde con:
1. La ruta del PDF con credenciales y la de la versión sin credenciales, si la hiciste.
2. El número de páginas.
3. El resultado de la verificación de los datos de práctica.
4. Una lista de lo que el usuario debe revisar antes de imprimir: el contacto y la fecha.
5. **Un recordatorio para el usuario:**
   - **imprimir la página 2 aparte** y entregarla solo al administrador;
   - **después de la entrega,** cambiar la contraseña del `admin` que aparece en el PDF, o pedirle al administrador del cliente que la cambie en su primer uso.
6. Si generaste la versión sin credenciales, **el mensaje de commit** solo para ese archivo: `docs(migracion): guía rápida de entrega sin credenciales`, con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.**
