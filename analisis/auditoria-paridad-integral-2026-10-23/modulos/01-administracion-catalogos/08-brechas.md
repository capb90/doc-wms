# 08 — Brechas · 01-administracion-catalogos

> **Fecha:** 2026-10-23. Antes de registrar cada brecha se buscaron fichas en `docs/qa/resultados/defectos/` (índice de 153), `docs/planes/migracion-staging/resultados/defectos/` (8) y los pendientes de `docs/contexto/estado.md` §4. Ninguna brecha de este registro tiene ficha `DEF-*`; donde hay una observación de QA se cita.
> **Totales:** 8 brechas · CRÍTICA 0 · ALTA 0 · MEDIA 1 · BAJA 7.

## BR-01-001 · Embalajes: no se pueden retirar y el borrado deja productos sin embalaje

- **ID funcional:** CF-L032 (y CF-L029…031 por el mismo catálogo).
- **Descripción:** el legacy da de baja el embalaje de forma lógica: deja de ofrecerse y los registros que lo usan lo conservan. En V2 solo existe el borrado físico.
- **Comportamiento esperado:** poder retirar un embalaje (desactivarlo) aunque esté en uso, sin perder el dato en los productos y depósitos que lo tienen.
- **Comportamiento actual:**
  - `DELETE administration/packaging-types/{id}` solo comprueba los productos de depósito (`Backend/wms-api/Wms.Application/Administration/PackagingTypes/Commands/DeletePackagingType/DeletePackagingTypeHandler.cs:22-28`) y responde 400 si hay alguno.
  - Si solo lo usan productos del catálogo, lo borra y la FK `products.packaging_type_id` con `SetNull` (`Backend/wms-api/Wms.Infrastructure/Persistence/Configurations/Product/ProductConfiguration.cs:34-38`) deja esos productos sin embalaje. La base hace el cambio, así que no queda fila en `audit_logs` por cada producto.
  - `PackagingType.Activate/Deactivate` existen (`Backend/wms-api/Wms.Domain/Entities/Administration/PackagingType.cs:42-52`) pero ningún comando las llama; `UpdatePackagingTypeRequest` no tiene `IsActive` (`Wms.Application/Administration/PackagingTypes/Commands/UpdatePackagingType/UpdatePackagingTypeCommand.cs:6`) y la pantalla no ofrece el estado (`Frontend/wms/app/pages/admin/packaging-types/index.vue:97-133`).
- **Capa:** backend y frontend. **Categoría:** PERSISTENCIA.
- **Evidencia legacy:** `bodegas-legacy/modulos/mod_embalajes/eliminarembalaje.php:57`; `listarembalajes.php:69`.
- **Impacto:** un embalaje obsoleto que ya se usó en depósitos queda para siempre en los selectores; uno usado solo en el catálogo se borra con pérdida silenciosa del embalaje por defecto de los productos.
- **Criticidad:** MEDIA — función secundaria (catálogo), pero con pérdida de datos no auditada y sin alternativa para retirar el valor.
- **Dependencias:** ninguna. Ya anotado como OBS-F1-005 (`docs/qa/resultados/F1-informe-2026-10-02.md:213`); el caso F1-EMB-003 no se ejecutó.
- **Acción recomendada:** exponer `isActive` en `PATCH packaging-types/{id}` y en la pantalla; bloquear el borrado (409) si lo usa cualquier producto del catálogo o de depósito.
- **Criterio de resolución:** (1) un embalaje en uso se desactiva y desaparece de `GET packaging-types?isActive=true`; (2) borrar un embalaje usado por un producto del catálogo responde 409 y el producto conserva `packagingTypeId`; (3) prueba en `Wms.Tests` o `Wms.IntegrationTests` de ambos casos.

## BR-01-002 · Catálogos legibles sin sesión

- **ID funcional:** CF-L029, CF-L037 (también roles de sistema, roles de negocio e impuestos).
- **Descripción:** cinco lecturas tienen `[AllowAnonymous]`: `GET administration/system-roles`, `business-role`, `taxes`, `operation-modalities` y `packaging-types` (`Backend/wms-api/Wms.Api/Controllers/v1/AdministrationController.cs:40,51,63,111,133`).
- **Comportamiento esperado:** DEC-031: lecturas de catálogos para los flujos con `ActiveUser`. En el legacy toda página pedía sesión y permiso (`listarembalajes.php:8-9`, `listarmodalidades.php:8-9`).
- **Comportamiento actual:** responden sin token (confirmado en QA: F9-API-016, OBS-F9-001, `docs/qa/resultados/F9-informe-2026-10-03.md:98`).
- **Capa:** backend. **Categoría:** SEGURIDAD.
- **Impacto:** exposición de datos de configuración no sensibles (nombres de roles, impuestos, modalidades, embalajes). Ninguna pantalla pública los necesita: el login no los usa (`Frontend/wms/app/features/auth/services/auth-services.ts:11-23`).
- **Criticidad:** BAJA — sin datos personales ni de negocio sensibles.
- **Dependencias:** ninguna.
- **Acción recomendada:** quitar `[AllowAnonymous]`; queda el `[Authorize]` del controlador.
- **Criterio de resolución:** sin token, los cinco endpoints responden 401; con cualquier rol responden 200.

## BR-01-003 · Restos de «INTERMEDIARY» y «SIA» como código de rol

- **ID funcional:** transversal (CF-L061…064; consumidores de los módulos 04, 05 y 07).
- **Descripción:** DEC-011 dice que la agencia de aduanas es un solo rol, `CUSTOMS_AGENCY`, y que un «SIA» o «INTERMEDIARY» en el código es un bug.
- **Comportamiento esperado:** resolver la agencia solo por `CUSTOMS_AGENCY`.
- **Comportamiento actual:** `CustomsAgencyResolver` recorre `["CUSTOMS_AGENCY", "INTERMEDIARY", "IMPORT_AGENCY"]` y, si no encuentra, acepta un rol cuyo código o nombre contenga «SIA», «Agencia de aduanas» o «Intermediario» (`Backend/wms-api/Wms.Application/ForeignTrade/Common/Services/CustomsAgencyResolver.cs:16,40-44`). La documentación del endpoint de alta rápida dice «IMPORTER o INTERMEDIARY» (`Backend/wms-api/Wms.Api/Controllers/v1/WeighbridgeController.cs:987`), aunque el validador solo acepta `IMPORTER`, `CUSTOMS_AGENCY` y `EXPORTER` (`QuickCreateStakeholderValidator.cs:8`). Solo se siembra `CUSTOMS_AGENCY` (`Backend/wms-api/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:136-140`).
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** ninguno con los datos actuales; si alguien creara un rol con esos códigos o nombres, la guía, las etiquetas y el PDF del depósito lo tomarían como agencia.
- **Criticidad:** BAJA — latente.
- **Dependencias:** la cascada vino del plan de corrección (CHG en `docs/qa/plan-correccion-defectos.md:2058`), que no es fuente de decisión frente a DEC-011.
- **Acción recomendada:** dejar solo `CUSTOMS_AGENCY` (y ajustar `CustomsAgencyResolverTests`) o registrar la excepción como decisión en `docs/contexto/decisiones.md`.
- **Criterio de resolución:** `rg -n "INTERMEDIARY|IMPORT_AGENCY" Backend/wms-api/Wms.Application Backend/wms-api/Wms.Api` sin resultados en código de producción, o una DEC que lo autorice.

## BR-01-004 · Datos y validaciones de las fichas legacy sin destino ni decisión

- **ID funcional:** CF-L010, 011, 034, 035, 046, 047, 062, 063, 086, 087.
- **Descripción:** las decisiones del 2026-09-29 descartan representantes con %, marca, línea, clase y carrocería del vehículo, ocupación y fotos (DECISIONES_REVISION.md §3.7; plan-backend §A.3 GAP-023; MIGRATION_MATRIX filas 045–047). Otros datos que el legacy pedía no tienen destino en V2 ni decisión:
  - **Cliente:** dígito de verificación, ciudad, segundo teléfono; nombre en mayúsculas (`bodegas-legacy/modulos/mod_clientes/registrarcliente.php:83-104`).
  - **Transportadora:** sigla y ciudad (`mod_empresastransporte/registrarempresatransporte.php:64`).
  - **SIA:** ciudad (`mod_sias/registrarsia.php:57`).
  - **Persona/conductor:** licencia de conducción, email, dirección y ciudad; el legacy excluye NIT y deja el apellido opcional (`mod_personas/registrarpersona.php:83,106`).
  - **Vehículo:** número de motor, chasis y modelo (`mod_vehiculos/registrarvehiculo.php:82`).
- **Comportamiento actual:** `Stakeholder` guarda nombre, tipo y número de documento, matrícula mercantil, estado comercial y UAP (`Backend/wms-api/Wms.Domain/Entities/Stakeholder/Stakeholder.cs:42-58`); dirección, teléfono y país van en contactos (`StakeholderContactInfo.cs:7-16`). `Driver` guarda nombres, apellidos, documento, país y teléfono (`Backend/wms-api/Wms.Domain/Entities/Logistics/Driver.cs:8-17`) y acepta NIT (`CreateDriverValidator.cs:22-25`). `Vehicle` guarda placa, transportadora, país y tipo (`Vehicle.cs:10-17`). La migración (F6-02) solo exporta las columnas que V2 guarda (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` §C.6, F6-02).
- **Capa:** backend, frontend y persistencia. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** pérdida de información de referencia de los maestros; ningún flujo V2 la usa hoy. Si un documento externo (factura, guía, reporte para la DIAN) necesita el DV o la ciudad del cliente, no se puede imprimir.
- **Criticidad:** BAJA — sin efecto en procesos esenciales.
- **Dependencias:** ninguna.
- **Acción recomendada:** confirmar con el negocio; si no hacen falta, registrarlo como decisión (y cerrar la brecha como `DIFERENCIA_INTENCIONAL`).
- **Criterio de resolución:** una decisión escrita que cubra cada dato listado, o los campos agregados a la entidad, el formulario y la importación.

## BR-01-005 · Placa única sin país

- **ID funcional:** CF-L086, CF-L087, CF-L247.
- **Descripción:** en el legacy un vehículo se identifica por placa **y país** (`bodegas-legacy/modulos/mod_vehiculos/consultarplaca.php:9-21`; aviso en `registrarvehiculo.php:159-176`). V2 tiene índice único solo por placa (`Backend/wms-api/Wms.Infrastructure/Persistence/Configurations/Logistics/VehicleConfiguration.cs:25`; `CreateVehicleHandler.cs:21-27`) y la búsqueda de báscula es por placa (`WeighbridgeCatalogController.cs:49`).
- **Comportamiento esperado:** el que decida el negocio. En la frontera (Ipiales) circulan vehículos colombianos y ecuatorianos.
- **Comportamiento actual:** el segundo vehículo con la misma placa y otro país recibe 409 «La placa … ya existe.».
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** caso borde: un camión no se podría registrar con su país real; el operario tendría que alterar la placa. La migración rechazó 49 vehículos por placa inválida, no por duplicado (`docs/planes/migracion-staging/resultados/informe-fase-3.md:110`), así que no hay evidencia de que ocurra en los datos.
- **Criticidad:** BAJA — escenario específico, sin casos observados.
- **Dependencias:** relacionada con DEF-F1-005 (placa duplicada por mayúsculas; Verificado), que es otra cosa.
- **Acción recomendada:** confirmar con el negocio; si aplica, índice único (placa, país) y búsqueda por placa + país.
- **Criterio de resolución:** decisión escrita, o dos vehículos con la misma placa y distinto país se crean y la búsqueda de báscula distingue el país.

## BR-01-006 · Desactivar maestros con registros asociados no se bloquea ni se advierte

- **ID funcional:** CF-L012, CF-L036, CF-L048, CF-L088.
- **Descripción:** el legacy impide «eliminar» (baja lógica) un cliente con convenio, factura, recibo o representante, una transportadora con vehículos, una persona que conduce en pesajes y un vehículo con pesajes o empresa (`ComprobarRelacion`, `bodegas-legacy/includes/funciones.php:18-34`; `eliminarcliente.php:20`, `eliminarempresatransporte.php:20`, `eliminarpersona.php:20`, `eliminarvehiculo.php:20`; mensaje 8 en `bodegas-legacy/aut_mensaje_error.inc.php:17`).
- **Comportamiento actual:** V2 desactiva siempre (`UpdateStakeholderHandler.cs:46-54`; `PATCH drivers/{id}` y `PATCH vehicles/{id}` con `isActive`).
- **Capa:** backend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** un cliente con depósitos vivos o convenio activo puede quedar inactivo y dejar de aparecer en los selectores de báscula y Comercio Exterior. La historia se conserva. No se revisó qué hacen los jobs de facturación con un cliente inactivo (módulo 06).
- **Criticidad:** BAJA — la baja es reversible y no borra datos.
- **Dependencias:** módulo 06 (efecto en facturación de un cliente inactivo).
- **Acción recomendada:** decidir con el negocio entre bloquear (409) o advertir al desactivar un tercero con depósitos abiertos o convenio activo.
- **Criterio de resolución:** decisión escrita, o desactivar un cliente con un depósito `Confirmed` responde 409/advertencia según lo decidido, con prueba.

## BR-01-007 · Bodegas: sin alta en cuadrícula y con borrado físico

- **ID funcional:** CF-L090, CF-L092 (relacionado con CF-L171 del módulo 03).
- **Descripción:** el legacy crea una bodega con `filas × columnas` secciones libres (RN-043, `bodegas-legacy/modulos/mod_bodegas/registrarbodega.php:87-133`) y la da de baja de forma lógica con todas sus secciones (`eliminarbodega.php:88-104`). MIGRATION_MATRIX lo marcó COMPORTAMIENTO DIFERENTE y F4-01 solo construyó ubicar, mover y liberar.
- **Comportamiento actual:** las ubicaciones se crean una a una (`WarehouseController.cs:910-920`); no hay tipo ni uso; el borrado es físico y se bloquea si hay almacenamientos (`DeleteWarehouseLocationHandler.cs:15-27`) o mercancía ubicada (FK `Restrict`, `WarehouseStorageProductPlacementConfiguration.cs:36-39`). La alternativa lógica es «No disponible».
- **Capa:** backend y frontend. **Categoría:** REGLAS_NEGOCIO.
- **Impacto:** productividad del Admin al dar de alta una bodega nueva; ningún dato se pierde (el borrado físico solo ocurre sin uso y queda auditado).
- **Criticidad:** BAJA.
- **Dependencias:** ninguna. DEF-MIG-008 (Verificado) trató la migración de ubicaciones, no esta diferencia.
- **Acción recomendada:** confirmar con el negocio si hace falta el alta en lote; si no, registrar la decisión.
- **Criterio de resolución:** decisión escrita, o un endpoint que cree N ubicaciones con un patrón (pasillo, filas, columnas) con prueba.

## BR-01-008 · El cambio de contraseña no pide la contraseña actual

- **ID funcional:** CF-V002 (relacionado con CF-L097; RN-076).
- **Descripción:** el legacy actualiza la contraseña solo si la anterior coincide (`bodegas-legacy/modulos/mod_usuarios/cambiarcontrasena.php:45-66`). V2 la cambia con un token de restablecimiento generado en el servidor, sin pedir la actual (`Backend/wms-api/Wms.Application/Auth/Commands/ChangePassword/ChangePasswordHandler.cs:39-43`; `ChangePasswordCommand(string NewPassword)`).
- **Comportamiento esperado:** pedir la contraseña actual en el cambio voluntario (el cambio obligatorio del primer ingreso puede seguir sin ella).
- **Comportamiento actual:** quien tenga una sesión abierta ajena puede fijar una contraseña nueva.
- **Capa:** backend y frontend. **Categoría:** SEGURIDAD.
- **Impacto:** toma de cuenta a partir de una sesión desatendida.
- **Criticidad:** BAJA — exige un token válido; el acceso está fuera de la paridad (DEC-030), pero no hay decisión sobre este punto.
- **Dependencias:** OBS-F1-007 (`docs/qa/resultados/F1-informe-2026-10-02.md:215`); no hay ficha DEF.
- **Acción recomendada:** agregar `currentPassword` cuando `mustChangePassword` es falso y validarlo con `CheckPasswordAsync`.
- **Criterio de resolución:** `POST auth/change-password` sin la contraseña actual correcta responde 400 para un usuario que no está obligado a cambiarla; prueba de integración.

## Diferencias con decisión (no son brechas)

Van como `DIFERENCIA_INTENCIONAL` en la matriz: acceso, usuarios y permisos (DEC-030, plan-backend §A.3); catálogos fijos de documentos comerciales, modalidades, requisitos, naturaleza, tipos de bodega y tipos de identificación (DECISIONES_REVISION.md §3.6, plan-frontend §A.3); resoluciones (DEC-024, DEC-012); prefijos (plan-backend §A.3, DEC-012); unidades de carga como maestro (DEC-014, GAP-023); vehículos por convenio (GAP-018); representantes, marca y carrocería, ocupación y fotos (DECISIONES_REVISION.md §3.7); alerta de TRM (DEC-023).

**Riesgo anotado sin brecha:** con los tipos de identificación fijos, 8 conductores con cédula de extranjería y 2 transportadoras (62 vehículos en cascada) no se migraron (`docs/planes/migracion-staging/resultados/informe-fase-3.md:106-111`). La decisión se cumple; conviene que el negocio confirme que esos conductores pueden registrarse con pasaporte.
