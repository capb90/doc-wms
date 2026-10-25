# Plan de la ronda QA de preproducción — regresión integral antes de la fase 13

> **Fecha:** 25 de octubre de 2026. **Estado:** aprobado por el usuario el 2026-10-25.
> **Build bajo prueba:** BE `develop` `57c94dd` · FE `develop` `cb2a4f7`. Es el que se desplegará en la fase 13 del plan de brechas P1.
> **Ejecutor:** un agente sin historial, solo, con el prompt `qa/prompt-ronda-qa-preproduccion-2026-10-25.md`.
> **Rutas:** relativas a `code_workspace/`.

---

## 1. Objetivo

Confirmar, antes de desplegar en staging, que la aplicación completa funciona sobre **datos migrados del legacy**, con todo lo construido en el plan de brechas P1 (fases 1 a 12c), y ensayar las migraciones del despliegue sobre esos datos.

**El resultado es un veredicto:**

- **GO para la fase 13;**
- **GO con condiciones,** con su lista;
- o **NO GO,** con los defectos que lo impiden.

**Esta ronda no:**

- corrige código: solo observa, documenta y registra defectos;
- toca staging;
- hace commits.

---

## 2. Decisiones de la ronda

| # | Decisión | Fuente |
| --- | --- | --- |
| R1 | **Alcance: regresión integral.** Lleva estos bloques:<br>• un humo de todas las pantallas por rol;<br>• los flujos de punta a punta de `qa/fase-08-e2e.md`;<br>• los casos nuevos del plan P1;<br>• los 31 casos `NO EJECUTADO` de `qa/resultados/P1-informe-2026-10-24.md`;<br>• los casos de la fase 12c;<br>• roles y permisos;<br>• los reportes sobre datos migrados | Usuario, 2026-10-25 |
| R2 | **Datos:** una base desechable `wms_qa_preprod`, clonada de `wms_migracion`, que tiene los datos migrados del legacy, como staging. `wms_migracion`, `wmsdb` y las bases de grabación **no se modifican** | Usuario, 2026-10-25; `procesos/verificacion-local.md` §1 |
| R3 | **Ensayo de las migraciones:** a la copia se le aplican, con `dotnet ef database update --connection`, las migraciones que le falten hasta la última, `20261025152149_RelaxServicePriceActiveIndex`. Es el ensayo del despliegue de la fase 13 sobre datos reales. Se anotan cuáles se aplican y cuánto tardan. **Si alguna falla, la ronda se detiene**: es un hallazgo bloqueante para el despliegue | Plan P1 §16.1 |
| R4 | **Palancas de tiempo** autorizadas **solo en `wms_qa_preprod`**: mover fechas por SQL (facturas, períodos, convenios, precios) y reiniciar la API para que corran los jobs. Cada SQL va al informe, con la hora y los reinicios. Nunca en otra base | Usuario, 2026-10-25; `qa/00-plan-maestro.md` §3 y `qa/fase-06-facturacion.md` §4 |
| R5 | **Datos nuevos con prefijo `QA-PRE`**, sobre los maestros migrados (clientes, productos, ciudades, conductores, vehículos). Todo lo creado se anota en `qa/resultados/registro-datos-qa-preproduccion.md` | `qa/00-plan-maestro.md` §5.1 |
| R6 | **Sin datos de personas en los documentos** (DEC-007). Los informes usan códigos, números de depósito y los datos `QA-PRE`. Las capturas no deben mostrar nombres, documentos ni placas reales; si una evidencia los tiene, se describe en texto y no se guarda | DEC-007 |
| R7 | **Servicios externos locales:**<br>• correo, a un sumidero SMTP local (por ejemplo `axllent/mailpit`);<br>• S3, a `adobe/s3mock`;<br>• la TRM, la API pública de la DIAN (solo lectura); si no responde, se anota y se usa TRM manual;<br>• el QR: se decodifica la imagen del PDF con el detector de macOS (como en la fase 12). El escaneo en papel queda para la fase 13 | `procesos/verificacion-local.md` §3.7 |
| R8 | **Cuentas:** si la copia no tiene un Admin utilizable, se usa `Bootstrap:AdminPassword` (`B/Wms.Api/Common/Identity/BootstrapAdminSeeder.cs`) con una contraseña generada por el agente. Con ese Admin se crean por API las cuentas `qa.pre.<rol>` de los 6 roles y 2 multirol. Las contraseñas viven solo en el scratchpad del agente: nunca en `docs/`, en commits ni en la salida | DEC-007 |
| R9 | **Defectos:** serie `DEF-F11-029…`, con ficha según `qa/plantillas/defecto.md` y fila en `qa/resultados/defectos/INDICE.md`. Las severidades siguen `qa/00-plan-maestro.md` §2.2 | `procesos/qa-y-defectos.md` |
| R10 | **No se corrige nada.** Un defecto, aunque sea trivial, solo se registra. Un BLOCKER detiene únicamente el bloque afectado: los demás bloques siguen si no dependen de él | Usuario, 2026-10-25 |

---

## 3. Entorno

1. **Commits:** BE `57c94dd` y FE `cb2a4f7` en `develop`, con los árboles limpios (`git status`). Si no coinciden, detenerse.
2. **Postgres:**
   - Arrancar `wms-postgres-db` (puerto 5433).
   - Comprobar que existe `wms_migracion` y leer su `__EFMigrationsHistory`, en solo lectura.
   - Crear la copia con `CREATE DATABASE wms_qa_preprod TEMPLATE wms_migracion;` (exige que nadie esté conectado a `wms_migracion`).
   - Si `wms_migracion` no existe o no se puede clonar, detenerse y anotarlo.
3. **Migraciones (R3):**

   ```text
   dotnet ef database update --project Wms.Infrastructure --startup-project Wms.Api --connection "<cadena a wms_qa_preprod>"
   ```

   La cadena se arma con la de `appsettings.Development.json`, cambiando solo el nombre de la base. No se abren `.env*`. Después se anotan las migraciones aplicadas.
4. **API** (`dotnet run --project Wms.Api`, puerto 5281, Development). Las variables de entorno solo para esta sesión:
   - `ConnectionStrings` → `wms_qa_preprod`;
   - correo → sumidero local, y `Notifications:AdminEmails` → una dirección de prueba;
   - `Frontend:BaseUrl` = `http://localhost:3000`;
   - `DispatchGuides:VerificationKey` = una clave de prueba generada para la ronda;
   - `Backups` con un destino local temporal y otro S3 hacia `s3mock`;
   - `Bootstrap:AdminPassword` si hace falta (R8).
5. **Frontend:** `yarn dev` en el puerto 3000, con `NUXT_PUBLIC_API_BASE=http://localhost:5281/api/v1`.
6. **Navegador:** el integrado de la app, en la zona horaria de Colombia o anotando la que se use. Para los casos móviles, una emulación de 375 × 812.
7. **Configuración que falte en la copia:**
   - tarifas de `DEC-041` (T1–T4 y montacargas);
   - `INVENTORY_ADJUSTMENT_ADMIN_EMAIL`;
   - convenios QA.

   Se crea por la API o la pantalla, nunca por SQL, y se anota.

---

## 4. Bloques de ejecución

Van en este orden. Cada bloque anota casos, resultados y evidencias.

| Bloque | Contenido | Casos de referencia | Prioridad |
| --- | --- | --- | --- |
| **B0. Ensayo y humo** | R3 (migraciones sobre datos migrados) y el humo de `qa/fase-00-smoke.md`: el API responde, el login, el menú por rol | `fase-00-smoke.md` | P0 |
| **B1. Pantallas por rol** | Con cada cuenta `qa.pre.*`, abrir **todas** las páginas de su menú (`F/app/components/layout/AppMenu.vue`). Cada una carga sin error en consola ni 4xx/5xx inesperados, con los listados reales migrados (paginación, filtros, `all=true` en los selects). Las rutas fuera de su rol → «Acceso denegado» | `fase-09-roles-permisos.md`, `fase-10-ux-visual-errores.md` | P0 |
| **B2. Flujos de punta a punta** | E2E-01 a E2E-17 de `qa/fase-08-e2e.md`, empezando por los P0. Se hacen con datos `QA-PRE` sobre maestros migrados, e incluyen:<br>• un depósito con varios documentos y **un solo pesaje** (fase 5);<br>• «Solo báscula» sin cliente (fase 4);<br>• la orden con guía vigente (fase 2);<br>• la guía con QR verificada en la página pública (fase 11);<br>• el cliente con «sin salidas» (fase 3) | `fase-08-e2e.md` y los casos F3, F5 y F6 citados en el plan P1 §15.2 | P0/P1 |
| **B3. Casos nuevos del plan P1** | Todos los casos que el plan P1 agregó en las fases 1 a 12c (§15.2 del plan y F1-SRV-021, F6-ALM-019), incluidos los de QR y permisos (F5-GUI-0xx, F9-API-0xx) | `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md` §15.2 y §15C; `qa/fase-*.md` | P0/P1 |
| **B4. Pendientes del informe P1** | Los 31 casos `NO EJECUTADO` de `qa/resultados/P1-informe-2026-10-24.md`, con palancas de tiempo (R4) donde haga falta:<br>• F6-ALM-009 y 017;<br>• F6-REC-001…007;<br>• F6-TAR-001…010;<br>• F5-OC-007, 013 y 018;<br>• F3-SBA-003;<br>• F7-REP-003, 018, 019 y 025;<br>• F11-REG-021;<br>• FB-BAK-001…003.<br>FA-MIG-013 queda para el corte real | `P1-informe-2026-10-24.md` | P0/P1 |
| **B5. Datos migrados** | Sobre los depósitos vivos migrados:<br>• saldos e inventario general;<br>• kardex de 3 depósitos;<br>• diario de ingresos (formato legacy) y de salidas;<br>• pólizas;<br>• abandono y prórrogas;<br>• «Depósitos pendientes»;<br>• renovación de un período de un migrado con palanca;<br>• una orden, cargue y guía sobre un depósito migrado.<br>Se anota cualquier saldo o fecha incoherente, sin datos de personas | `fase-11-regresion-cierre.md` Anexo A; `fase-07-transversal.md` | P0/P1 |
| **B6. Permisos y API** | La matriz de `qa/resultados/F9-anexo-matriz-api.md`, con las políticas nuevas (`ExitBlockAccess`) y los endpoints retirados en la fase 1. La verificación pública del QR responde sin sesión, tiene el limitador (429) y no expone datos personales | `fase-09-roles-permisos.md` | P0 |
| **B7. Errores y UX** | Una muestra de `qa/fase-10-ux-visual-errores.md`:<br>• mensajes en español;<br>• doble envío;<br>• API caída;<br>• formatos de número y fecha;<br>• la página pública del QR en celular | `fase-10-ux-visual-errores.md` | P1 |

---

## 5. Registro

| Archivo | Contenido |
| --- | --- |
| **Nuevo** `qa/resultados/PRE-informe-2026-10-25.md` | Lo que lleva:<br>• entorno y commits;<br>• migraciones aplicadas y su tiempo;<br>• palancas usadas;<br>• tabla por bloque y caso (ID, prioridad, estado, tipo, observación);<br>• resumen por prioridad;<br>• defectos;<br>• veredicto |
| **Nuevo** `qa/resultados/registro-datos-qa-preproduccion.md` | Los datos `QA-PRE` creados (IDs, números de depósito, guías, facturas), sin contraseñas |
| `qa/resultados/defectos/DEF-F11-029.md…` e `INDICE.md` | Los defectos nuevos |
| `qa/resultados/evidencias/PRE/` | Evidencias sin datos de personas (R6): respuestas del API recortadas, PDF de datos `QA-PRE`, capturas de pantallas `QA-PRE` |
| `qa/README.md` | Fila del informe nuevo |
| `planes/registro-ejecucion-brechas-p1-2026-10-24.md` | Una sección «Ronda QA de preproducción», con el veredicto y el enlace al informe |

Estados de los casos: `PASA`, `FALLA` (con ficha DEF), `BLOQUEADO`, `NO EJECUTADO` (con motivo) y `OBSERVACIÓN`, según `qa/00-plan-maestro.md` §2.1.

---

## 6. Criterios de salida y veredicto

- 100 % de los P0 y al menos el 95 % de los P1 en un estado distinto de `NO EJECUTADO` (`qa/00-plan-maestro.md` §6.2).
- Cada `FALLA` tiene su ficha.
- Veredicto:

  | Veredicto | Condición |
  | --- | --- |
  | **GO** | Sin BLOCKER ni CRITICAL abiertos, y el ensayo de migraciones sin errores |
  | **GO con condiciones** | Sin BLOCKER; los CRITICAL o MAJOR abiertos, listados con su impacto en la operación de staging |
  | **NO GO** | Algún BLOCKER, una migración que falla, o un flujo P0 roto |

---

## 7. Cuándo detenerse

- Una migración falla en la copia (R3): se detiene **toda** la ronda.
- El entorno no arranca: API, frontend, base o Docker.
- Un BLOCKER que impide el resto de los bloques.
- Cualquier acción fuera de la copia desechable: otra base, staging, `.env*` o commits.

Al detenerse, se escribe el informe con lo hecho y el motivo, y se termina.

---

## 8. Limpieza al terminar

- Detener la API, el frontend, el sumidero SMTP y `s3mock`.
- Detener `wms-postgres-db`.
- **No borrar `wms_qa_preprod`:** queda para el re-test de los defectos. El usuario decide cuándo se borra.
- Se anota en el informe.
