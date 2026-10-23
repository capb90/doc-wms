# Fase 11 — Regresión, re-test y cierre

> Lee antes `00-plan-maestro.md`. Se ejecuta sobre el **último build** con las correcciones de las fases anteriores.

## 1. Objetivo

Confirmar que los defectos corregidos están resueltos, que las correcciones no rompieron nada (regresión), que el camino crítico del negocio funciona de punta a punta en el build candidato, y emitir la recomendación go/no-go.

## 2. Criterios de entrada

1. Fases 0 a 10 con informe y checkpoint aprobado.
2. Lista de defectos con estado «Corregido» y el build donde se corrigió.
3. Commits del build candidato anotados (frontend y backend).
4. Base de datos: preferible recreada (decisión del usuario) para empezar desde cero con el dataset maestro; si no, datos QA existentes.

## 3. Bloques

### 3.1 Re-test de defectos (RET)

Para cada defecto «Corregido»:

| Paso | Acción |
|---|---|
| 1 | Re-ejecutar el caso que lo detectó con los mismos datos (o equivalentes). |
| 2 | Re-ejecutar los casos P0 del mismo bloque. |
| 3 | Marcar el defecto `Verificado` o `Reabierto` con evidencia. |

Prioridad: CRITICAL y BLOCKER primero; luego MAJOR; MINOR/TRIVIAL si hay tiempo.

### 3.2 Suite de regresión (REG)

Conjunto mínimo que cubre el camino crítico. Se ejecuta completo en cada build candidato. Duración objetivo: ½ día.

| ID | Caso de origen | Qué protege | P |
|---|---|---|---|
| F11-REG-001 | F0-LOG-001/002/005 | Login, ruta por rol, logout | P0 |
| F11-REG-002 | F0-NAV-003 | Todas las páginas del menú cargan | P0 |
| F11-REG-003 | F1-TER-001, F1-TER-005 | Alta de tercero y unicidad | P0 |
| F11-REG-004 | F1-SRV-002, F1-CNV-002 | Tarifas y convenios guardan | P0 |
| F11-REG-005 | F2-ING-001, F2-ING-004 | Ingreso y regla de un ingreso abierto | P0 |
| F11-REG-006 | F2-INT-001, F2-INT-004 | Ingreso llega a báscula / bodega | P0 |
| F11-REG-007 | F3-REG-001, F3-REG-002 | Registro IMP crea depósito y stock declarado | P0 |
| F11-REG-008 | F3-COB-001, F3-COB-007 | Cobro inmediato y por facturar | P0 |
| F11-REG-009 | F3-PES-001..004 | Pesajes y neto | P0 |
| F11-REG-010 | F3-REI-004..007 | Reingreso sin volver a pedir datos | P0 |
| F11-REG-011 | F3-MCA-001, F3-MCA-007 | Varios camiones y cierre de ingreso | P0 |
| F11-REG-012 | F3-TIQ-002, F3-TIQ-006 | Tiquete y consecutivo | P0 |
| F11-REG-013 | F3-SBA-001 | Solo báscula | P0 |
| F11-REG-014 | F4-REC-004, F4-REC-005 | Recepción sin mover stock | P0 |
| F11-REG-015 | F4-MON-003, F4-MON-007 | Montacargas con y sin IVA | P0 |
| F11-REG-016 | F4-CAR-001, F4-CAR-011 | Cargue y cierre del depósito | P0 |
| F11-REG-017 | F5-CNF-001, F5-CNF-002 | Confirmar y sus requisitos | P0 |
| F11-REG-018 | F5-LEV-001, F5-LEV-003 | Levantes y tope | P0 |
| F11-REG-019 | F5-OC-001, F5-OC-005..007 | OC y sus validaciones | P0 |
| F11-REG-020 | F5-GUI-002, F5-GUI-003 | Guía y saldos congelados | P0 |
| F11-REG-021 | F6-ALM-001, F6-TAR-001..004 | Factura de almacenamiento y resolución de tarifas | P0 |
| F11-REG-022 | F6-ACC-002..007 | N.º SIIGO y aprobación | P0 |
| F11-REG-023 | F6-PAG-001..003 | Pagos | P0 |
| F11-REG-024 | F6-TRM-002, F6-TRM-003 | TRM pendiente y manual | P0 |
| F11-REG-025 | F6-CAR-001, F6-CAR-009 | Bloqueo por mora | P0 |
| F11-REG-026 | F7-NOT-003 | Avisos a Comercio Exterior | P0 |
| F11-REG-027 | F9-API-010, F9-API-011 | Permisos de terceros y convenios | P0 |
| F11-REG-028 | F9-PAG-002..006 | Páginas por rol | P0 |
| F11-REG-029 | E2E-01 | Importación completa | P0 |
| F11-REG-030 | E2E-07 | Solo báscula completo | P0 |
| F11-REG-031 | Casos de cada defecto CRITICAL corregido | No reaparecen | P0 |

> Mantenimiento: cada defecto CRITICAL o BLOCKER corregido agrega su caso a esta suite (F11-REG-031 y siguientes).

### 3.3 Regresión dirigida por cambios (DIR)

Si entre la fase donde se probó un módulo y esta fase hubo commits en ese módulo, re-ejecutar los casos P0 y P1 del módulo afectado. Para decidirlo:

```bash
git log --oneline <commit-de-la-fase>..HEAD -- app/features/<modulo> app/pages/<ruta>
```

(y el equivalente en el backend por carpeta de feature). Anotar en el informe qué módulos cambiaron y qué casos se re-ejecutaron.

### 3.4 Pruebas automatizadas existentes (AUT)

| ID | Caso | Pasos | Resultado esperado | P |
|---|---|---|---|---|
| F11-AUT-001 | Pruebas del backend | En local: `dotnet test` en `Backend/wms-api`. | Todas pasan; anotar total y fallos. | P1 |
| F11-AUT-002 | Build del frontend | `yarn build` en `Frontend/wms`. | Código 0. | P1 |
| F11-AUT-003 | Lint del frontend | Contar errores de lint (procedimiento del §B.6 del plan de paridad). | No supera el tope registrado (296 al 2-oct-2026). | P3 |

> El ejecutor solo **ejecuta** estas herramientas; no corrige código ni lint.

### 3.5 Staging (STG)

Si el build se desplegó en staging: ejecutar F0 completo, F11-REG-001..013 y E2E-01 en staging. Anotar diferencias con local (correo en Mailtrap, sin Swagger, backups deshabilitados en staging según `compose.staging.yaml`).

## 4. Informe final del QA

Además del informe de fase, entregar `resultados/informe-final.md` con:

1. Alcance ejecutado (fases, fechas, builds, ambientes).
2. Métricas: casos por fase y estado; defectos por severidad, módulo y estado; tasa de reapertura.
3. Riesgos del §9 del plan maestro: tabla final confirmado/descartado.
4. Defectos abiertos con impacto y recomendación (corregir antes del corte / aceptar / posponer).
5. Tiempos de báscula medidos frente a la meta.
6. Decisiones de negocio pendientes que salieron del QA (p. ej., efectivo y cambio en báscula, mínimo antes/después de IVA, quincenal 14 vs 15, etiqueta nacionalizada con levante parcial, Vigilancia en Bodega).
7. **Recomendación go/no-go** para el corte del legacy con condiciones.

## 5. Criterios de salida (= criterios de «terminado» del QA)

- Suite REG 100 % ejecutada sobre el build candidato, sin FALLA en P0.
- Cero BLOCKER y cero CRITICAL abiertos, o CRITICAL aceptados por escrito por el usuario.
- Informe final entregado.

---

## Anexo A — Verificación de la migración legacy (opcional, por API, solo Admin)

Se ejecuta solo si el usuario va a hacer el corte con datos migrados (fase 6 del plan de paridad, DF3: sin pantallas). Ambiente local o un staging dedicado; **nunca** contra la base de producción.

| ID | Caso | Pasos | Resultado esperado | P |
|---|---|---|---|---|
| FA-MIG-001 | Simulación | `POST administration/legacy-import/{entity}` con `dryRun=true` para cada entidad en el orden del corte: ciudades, embalajes, cuadrillas, ubicaciones, clientes, agencias, transportadoras, vehículos, conductores, productos, depósitos, levantes. | Resultado por fila con errores; nada persistido (el lote queda como bitácora). | P1 |
| FA-MIG-002 | Dependencias en simulación | Simular depósitos sin haber cargado de verdad los maestros. | Anotar: la simulación de dependientes requiere maestros cargados. | P2 |
| FA-MIG-003 | Carga real | `dryRun=false` en orden. | Filas válidas guardadas aunque otras fallen; `GET legacy-import/batches/{id}` con errores (hasta 1000). | P1 |
| FA-MIG-004 | Idempotencia | Cargar el mismo archivo otra vez. | Filas omitidas (por `legacy_id_map`); sin duplicados. | P1 |
| FA-MIG-005 | Codificación y separadores | Archivos en UTF-8 y Windows-1252; con `;`, `,` y tabulador. | Tildes y ñ correctas. | P2 |
| FA-MIG-006 | Límites | Archivo vacío; > 50.000 filas; entidad inválida. | Rechazos controlados. | P2 |
| FA-MIG-007 | Conciliación | `POST legacy-import/reconciliation` con el CSV del corte. | Ok / Difference / NotMigrated por depósito; no escribe. | P1 |
| FA-MIG-008 | Apertura de facturación | `POST legacy-import/open-billing` antes y después de configurar tarifas. | Opened / Skipped / Failed por depósito; tras configurar, Opened. | P1 |
| FA-MIG-009 | Verificación en la UI por rol | Con cada rol, abrir los depósitos migrados (CE), inventario (Bodega), facturas (Facturación), reportes. | Datos visibles y coherentes; depósitos migrados en Confirmed; no admiten devolver a Borrador ni corregir fecha (sin camiones); saldos de guía sin salidas previas a la migración (anotar). | P1 |
| FA-MIG-010 | Número legacy | Buscar un depósito por su número legacy. | Anotar: el número legacy no se expone en ningún DTO (§G.12). | P3 |

## Anexo B — Respaldos (opcional, por API, solo Admin)

| ID | Caso | Resultado esperado | P |
|---|---|---|---|
| FB-BAK-001 | CRUD de destinos Local y S3; nombre duplicado (409). | Correcto. | P2 |
| FB-BAK-002 | Prueba de conexión del destino. | Éxito o error claro. | P2 |
| FB-BAK-003 | `POST backups/run` (202) y uno concurrente (409 «Ya hay un respaldo en curso.»). | Correcto; `GET backups/runs` lista la corrida. | P2 |
| FB-BAK-004 | Sin destinos activos. | Corrida fallida con aviso a Admin. | P3 |
| FB-BAK-005 | Restauración en una base aparte siguiendo `Backend/wms-api/deploy/staging/README.md`. | La base restaurada abre y los datos QA están. | P2 |
| FB-BAK-006 | Staging: respaldo programado. | Anotar: `Backups__Enabled` no está en `compose.staging.yaml` (job apagado en staging). | P2 |
