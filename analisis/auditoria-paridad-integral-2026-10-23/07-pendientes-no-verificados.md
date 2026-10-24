# 07 — Pendientes y puntos no verificados

> **Fecha:** 2026-10-23. Lo que esta auditoría estática **no pudo cerrar**, y por qué. Ninguna capacidad quedó en `NO_VERIFICADO` en la paridad integral, pero eso no equivale a funcionamiento validado: ver §5.

## 1. Brechas deducidas del código que hay que confirmar ejecutando

Son brechas registradas cuya existencia se infiere de leer el código. Una prueba las confirma o las descarta antes de corregirlas.

| Brecha | Qué se infiere | Por qué no se cerró | Prueba que la cierra |
| --- | --- | --- | --- |
| BR-06-004 (ALTA) | Un servicio complementario sin tarifa revierte la confirmación del depósito | QA no logró crear la configuración (F6-ALM-014 «NO APLICA», `docs/qa/resultados/F6-informe-2026-10-02.md:169`) | `09-recomendaciones-qa.md` QA-02 |
| BR-02-006 (ALTA) | La corrección del pesaje 3 o siguientes modifica el 2; neto mal recalculado en multidepósito | F3-COR-006 nunca se ejecutó | QA-04 |
| BR-05-002 (MEDIA) | Sobrerreserva del tope de lo nacionalizado con dos órdenes simultáneas | Exige concurrencia real | QA-05 |
| BR-05-007 (MEDIA) | `fromDate`/`toDate` de levantes llegan nulos (instante ISO contra `DateOnly`) | Depende del model binding en ejecución; F5-REL-001 solo probó el filtro por levante | QA-11 |
| BR-08-014 (MEDIA) | Con más de 15 avisos, el panel no muestra los nuevos | F7-NOT-006 no probó el orden | QA-14 |
| BR-06-001 (ALTA) | Un convenio programado nunca se activa | El orquestador verificó la ausencia de la transición en código; falta el efecto en la factura | QA-03 |

## 2. Dependen de datos reales (`db_legacy/` quedó fuera por restricción)

| Tema | Brecha o fila | Qué falta saber |
| --- | --- | --- |
| Uso real de las variantes legacy: entrada con productos del catálogo (Alt+N), «vehículo con varios documentos», repesajes múltiples, otros servicios en el cobro | `CF-L103.b`, `CF-L103.c`, `CF-L114`, `CF-L116.d` (módulo 02) | Si la operación las usaba. Condiciona BR-02-013 y BR-02-015 |
| `cliente.sinsalidas` | `CF-LX05-01`, BR-05-004 | Si había clientes con salidas bloqueadas. Ya decidido construir la marca (DEC-052); el dato solo sirve para migrarla |
| Seriales por unidad, volumen y condiciones, etiqueta por vehículo | `CF-L138`, `CF-L139`, `CF-L124` | Uso fuera de Colmotores. La etiqueta por vehículo (BR-04-012) ya no se construye (DEC-051) |
| Depósitos vivos con número repetido entre años | BR-08-005 | Cuántos hay en el volcado del corte real |
| Operaciones abiertas al corte | BR-08-004 | Órdenes, guías y pesajes en curso (`ROADMAP.md` 0.1) |
| Modelos de vehículo de Colmotores en el catálogo de productos migrado | Módulo 08 §6 | La consulta de productos no filtra al importador 70 |
| Prefijos que precargaba `campoprefijo` | `CF-L095`, `CF-L096` | Qué campos precargaba |
| Permisos legacy por usuario (tabla `permisos`) | Módulos 01 y 06 | Quién usaba convenios, tarifas y tasas |
| Horario real de `cron.php` | `CF-L234`, `CF-LX08-01` | No hay crontab en el checkout. Dos `INSERT` usan `$_SESSION` y fallarían sin sesión |
| Uso del portal por las agencias de aduanas | BR-08-008 | Cerrado por DEC-054: no hay acceso externo |
| Diarios y póliza entregados firmados a la DIAN | BR-07-004, 006 | De esto depende su criticidad. El diario de ingresos con firmas ya se decidió (DEC-054, BR-07-002) |
| Equivalencia FOB/CIF | `CF-L124`, `CF-L202.b`, `CF-L215` | Pendiente n.º 8 de `docs/contexto/estado.md` §4; `docs/analisis/revision-fob-cif-migracion-v2-2026-10-08.md` |

## 3. No se resuelven con código

| Tema | Fuente | Estado |
| --- | --- | --- |
| **PRF-002:** báscula ≤ 30 s con un operario (DEC-010, DF2, F1-09) | `docs/qa/resultados/informe-final.md`; `estado.md` §4 n.º 1 | Única condición del GO; pendiente |
| Rol de Vigilancia al operario de báscula | `BASCULA_PARITY.md` §6; `DECISIONES_REVISION.md` §3.1 | Configuración de usuarios. El efecto lateral descrito («ve Bodega completa») ya no existe en código (módulo 03) |
| Tarifas T1–T4 y del montacargas | `DEC-041` | Datos de configuración en staging, no código |
| Política de respaldo de producción y destino S3 | BR-08-001; `ROADMAP.md` 0.3 | Decisión de despliegue |
| Almacenamiento, instancias y dominio de producción | Módulo 08 §6 | Sin definir; condiciona BR-08-001, 002 y 012 |
| Publicación de los videos y aprobación de F7 | `estado.md` §4 n.º 10, §7 | Configuración del bucket |
| Prorrateo del almacenamiento (`DEC-025`) y mínimos (WMS-32) | `estado.md` §6 | Decisión del cliente abierta |

## 4. Código en disco que no está desplegado ni probado

Según `docs/contexto/estado.md` §3, staging corre BE `044be08` / FE `4ca4e0a`. Esta auditoría leyó el código posterior. Lo que trae no tiene QA registrado:

| Commit (según documentación) | Contenido | Capacidades afectadas |
| --- | --- | --- |
| BE `83de58a` (con la migración `20261008230241_AddForkliftUseEntryLog`) | Borrar productos declarados sin movimientos; montacargas con camión; recepción informativa con todos los camiones | `CF-V032`, `CF-V033`, `CF-L127`, `CF-L128` |
| BE `2eeaaad` | Producto y cantidad en el historial de guías; cambio del modo de pago de la guía; anulación por repesaje; unidad de carga al crear la orden | `CF-V055`, `CF-L163`, `CF-L105`, `CF-L154` |
| FE `f686f63`, `7ef72da`, `676ecb2`, `704dcef`, `0091e53`, `5a063a3`, `146e26d` | Contraparte de los fixes y centro de ayuda | `CF-V083` y las anteriores |

Además, varias fases de QA corrieron sobre builds anteriores al corte auditado: F3 y F6 sobre BE `191d4b1` / FE `a5289ce` (2026-10-02), con re-test parcial en F11. Una fila «Validada» confirma que la función se ejecutó en ese build, no en el actual.

## 5. Validación pendiente por capacidad

| Grupo | Cantidad | Dónde |
| --- | ---: | --- |
| Capacidades legacy evaluables sin ninguna ejecución documentada | 97 de 221 | `04-matriz-global.csv`, columna «Validación mediante ejecución» = «No ejecutada en esta auditoría» |
| Capacidades evaluables con ejecución, pero en `PARCIAL` (QA probó la función, no la diferencia) | 57 | Ídem |
| `SOLO_V2` sin ejecución documentada | 12 de 68 | Ídem, filas con «Clasificación V2» = `SOLO_V2` |
| Filas con confianza `MEDIA` | 52 de 410 | Columna «Confianza de la evaluación». Ninguna `BAJA`. La mayoría por depender de datos (§2) o de otro módulo |

## 6. Dependencias entre módulos, ya cerradas

Se registran para que no se busquen de nuevo:

| Fila | Dejada por | Cerrada por |
| --- | --- | --- |
| `CF-L172.c` | 03 (`NO_VERIFICADO`) | 07 (`PARCIAL`, BR-07-010) |
| F1-04 y F1-07 | 02 | 04 |
| F1-06 | 04 | 02 |
| F2-10 y P6(a) | 04 | 07 |
| F3-01 | 05 | 03 |
| F4-07 | 05 | 02 |
| F6-02 | 01 | 08 |
| Informes de facturación (cálculo y pantalla) | 07 | 06, filas `CF-L206` y `CF-L207` |

Abierta: el efecto de desactivar un cliente con convenio sobre los jobs de facturación. El módulo 01 lo dejó al 06, y el 06 no lo trató explícitamente: va a QA-15 de `09-recomendaciones-qa.md`.
