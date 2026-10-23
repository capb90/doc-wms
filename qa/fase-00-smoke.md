# Fase 0 — Smoke test y preparación del entorno

> Lee antes `00-plan-maestro.md` (§2 reglas, §3 ambientes, §4 cuentas, §5 datos).
> **Gate inicial.** Corta (1–2 h). No valida funcionalidades a fondo: decide si el ambiente sirve para empezar.

## 1. Objetivo

Comprobar que la aplicación está disponible, que se puede entrar con cada rol, que el menú y los módulos cargan sin errores, que las APIs principales responden y que existen los datos mínimos para la fase 1.

## 2. Alcance

- **Dentro:** disponibilidad de frontend y API, login y logout por rol, sesión al recargar, menú y ruta por defecto por rol, carga de la página principal de cada módulo, APIs de lectura principales, errores visibles en consola, catálogos sembrados, hub de notificaciones.
- **Fuera:** CRUD, reglas de negocio, flujos, permisos exhaustivos (fases 1 a 9).

## 3. Criterios de entrada

1. URL del frontend y del API del ambiente elegido (§3 del plan maestro).
2. Commits de ambos repositorios anotados.
3. Al menos una cuenta Admin utilizable (la del README o `admin` de bootstrap).
4. Navegador con DevTools.

## 4. Datos necesarios

Ninguno creado. Si faltan las cuentas por rol del README, el bloque LOG se ejecuta solo con Admin y se anota «cuentas por rol pendientes de crear en F1-USR». No es BLOCKER.

## 5. Casos

### 5.1 Disponibilidad (DIS)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F0-DIS-001 | Frontend disponible | Abrir la URL del frontend sin sesión. | Redirige a `/auth/login`; carga sin pantalla en blanco; sin errores rojos en consola (anotar advertencias). | P0 | FUN |
| F0-DIS-002 | API disponible | `POST {API}/auth/login` con usuario y contraseña inválidos. | Respuesta 400 o 401 con cuerpo JSON y mensaje en español («Credenciales inválidas»); no 5xx ni timeout. | P0 | API |
| F0-DIS-003 | CORS | Desde el frontend, intentar login inválido y mirar la pestaña Red. | La petición llega al API (sin error CORS en consola). | P0 | API |
| F0-DIS-004 | Swagger (solo local) | Abrir la raíz del API en local. | Swagger UI carga con «WMS API v1». En staging no aplica (Production). | P3 | API |
| F0-DIS-005 | Tiempo de carga inicial | Medir con DevTools el tiempo hasta que el login es usable. | < 5 s en red local; anotar el valor. | P2 | UX |

### 5.2 Login, sesión y logout (LOG)

Ejecutar con cada cuenta del §4 del plan maestro que exista.

| ID | Caso | Rol | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|---|
| F0-LOG-001 | Login Admin | Admin | Login con `capb90` (o `admin`). | Entra a `/` (Trazabilidad). Si la cuenta tiene «debe cambiar contraseña», va a `/auth/change-password` (anotar; no cambiarla sin autorización). | P0 | FUN |
| F0-LOG-002 | Login por rol | Cada rol | Login con `vigilancia`, `bascula`, `bodega`, `c_exterior`, `facturacion`. | Ruta por defecto: Vigilancia → `/operations/entries`; Báscula → `/operations/weighbridge`; Bodega → `/warehouse`; CE → `/`; Facturación → `/billing`. | P0 | FUN |
| F0-LOG-003 | Login inválido | — | Usuario válido con contraseña errada. | Mensaje «Credenciales inválidas»; se queda en login; no revela si el usuario existe. | P0 | ERR |
| F0-LOG-004 | Sesión al recargar | Cualquiera | Con sesión, recargar (F5) en una página interna. | Sigue en la misma página con sesión; no vuelve al login. | P0 | PER |
| F0-LOG-005 | Logout | Cualquiera | Perfil (menú derecho) → «Cerrar sesión» → confirmar. | Vuelve a `/auth/login`. «Atrás» del navegador no muestra datos protegidos sin volver a pedir login. | P0 | FUN |
| F0-LOG-006 | Ruta protegida sin sesión | — | Sin sesión, abrir `/billing` directamente. | Redirige a `/auth/login`. | P0 | ROL |
| F0-LOG-007 | Ruta sin permiso | Vigilancia | Con `vigilancia`, abrir `/billing`. | Muestra `/access-denied` (no la página). | P1 | ROL |
| F0-LOG-008 | Usuario ya autenticado en login | Cualquiera | Con sesión, abrir `/auth/login`. | Redirige fuera del login a la ruta del rol. | P2 | FUN |

### 5.3 Navegación y menú (NAV)

| ID | Caso | Rol | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|---|
| F0-NAV-001 | Menú Admin completo | Admin | Revisar el menú lateral. | Grupos: Notificaciones, Dashboards, Administración (con «Terceros» → Listado, Clientes, Transportadoras, Agencias de aduanas, Crear; y «Tarifas base» bajo Servicios, según F7-02), Vigilancia, Báscula, Bodega, Comercio Exterior, Facturación, Reportes. | P0 | FUN |
| F0-NAV-002 | Menú por rol | Cada rol | Revisar el menú con cada cuenta. | Cada rol ve solo sus grupos (Notificaciones para todos). Anotar diferencias para la fase 9. | P1 | ROL |
| F0-NAV-003 | Cada entrada del menú carga | Admin | Hacer clic en todas las entradas del menú. | Cada página carga sin error visible ni pantalla en blanco; sin errores rojos en consola; sin 4xx/5xx en Red (salvo esperados). Lista de páginas con error → defecto. | P0 | FUN |
| F0-NAV-004 | Ruta inexistente | Admin | Abrir `/no-existe`. | Página 404 (por defecto de Nuxt); se puede volver. Anotar si no hay forma de volver. | P3 | UX |
| F0-NAV-005 | Logo | Báscula | Clic en el logo de la barra superior. | Anotar destino. Riesgo R-ADM-08: puede terminar en access-denied. | P2 | UX |

### 5.4 APIs principales (API)

Con el token de Admin (copiar de la sesión del navegador o hacer login por API). Solo lecturas.

| ID | Endpoint | Resultado esperado | P | Tipo |
|---|---|---|---|---|
| F0-API-001 | `GET user/me` | 200 con el usuario y sus roles. | P0 | API |
| F0-API-002 | `GET administration/system-roles` | 6 roles. | P1 | API |
| F0-API-003 | `GET administration/operation-modalities` | IMP001, EXP001, OTH001, INSP001. | P0 | API |
| F0-API-004 | `GET entry-reasons` (o la pantalla de motivos) | 7 motivos: 5 con pesaje + «Solo bodega» + «Otro». | P0 | API |
| F0-API-005 | `GET weighbridge/queue` | 200 (lista, posiblemente vacía). | P0 | API |
| F0-API-006 | `GET foreign-trade/deposits` | 200. | P0 | API |
| F0-API-007 | `GET billing/invoices` (vía la pantalla de facturas) | 200. | P0 | API |
| F0-API-008 | `GET warehouse/locations` | 20 ubicaciones sembradas. | P1 | API |
| F0-API-009 | Servicios (`/admin/services`) | BASCULA, ALMACENAMIENTO, MONTACARGAS, PAPELERIA, GUIA_SALIDA. | P0 | API |
| F0-API-010 | Impuestos | IVA 19 % y RETE_FUENTE 3 %. | P1 | API |
| F0-API-011 | Unidades de medida y tipos de unidad de carga | 10 unidades; Contenedor, Tanquero, Remolque. | P1 | API |
| F0-API-012 | Hub SignalR | Tras el login, en Red aparece la negociación de `/hubs/notifications` con 200 y conexión WebSocket abierta. | P1 | INT |

### 5.5 Estado del entorno y datos mínimos (ENV)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F0-ENV-001 | Cuentas por rol | Admin → Usuarios: listar. | Anotar qué cuentas del §4 existen, activas y con qué roles. Faltantes → se crean en F1. | P0 | FUN |
| F0-ENV-002 | Terceros existentes | Admin → Terceros. | Anotar cuántos hay y si hay al menos un CUSTOMER, IMPORTER, CUSTOMS_AGENCY, TRANSPORT_COMPANY. | P1 | FUN |
| F0-ENV-003 | Tarifas mínimas | Admin → Servicios → BASCULA. | Anotar si tiene precio vigente o tarifa base. Sin tarifa, el cobro de báscula falla («No se encontró tarifa…»): F1 la configura. | P0 | FUN |
| F0-ENV-004 | Parámetro de ajustes | Perfil → Parámetros. | Anotar si `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` tiene valor (R-ADM-10). | P1 | FUN |
| F0-ENV-005 | Datos operativos previos | Revisar cola de báscula, depósitos, facturas. | Anotar si la base está vacía, tiene datos de pruebas anteriores o datos migrados del legacy. Si hay datos de clientes reales, **detener** y consultar al usuario. | P0 | FUN |
| F0-ENV-006 | Jobs | (Local) revisar el log del API tras arrancar. | Mensajes «…Job iniciado» de Overdue, DailyChargeConsolidation, StoragePeriodAutoClose, InvoiceDueNotification, AbandonmentAlert; sin excepciones al arrancar. | P2 | FUN |
| F0-ENV-007 | Zona horaria | Comparar la hora mostrada en una pantalla con la hora de Colombia. | Coinciden o se anota la diferencia. | P2 | FUN |

## 6. Criterios de salida

- **Continuar** si: F0-DIS-001/002, F0-LOG-001/004/005/006 y F0-NAV-003 pasan (salvo páginas aisladas con error, que se registran como defecto), y las APIs P0 responden.
- **Detener** si hay un BLOCKER: frontend o API caídos, login imposible para Admin, la mayoría de páginas con error, base con datos reales.
- Las cuentas o tarifas faltantes **no** detienen: pasan como tarea de preparación a la fase 1.

## 7. Entregables

Informe de fase con: inventario del entorno (cuentas, datos, catálogos), lista de páginas que no cargan, defectos y recomendación. Detenerse.
