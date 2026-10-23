Eres el implementador de la **Fase 1** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: Opus 5.5.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 1** y las tarjetas **CHG-01, CHG-02 y CHG-03**. Es el único alcance. Si algo choca con el plan, manda el plan; si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.

## Alcance
Implementa, en este orden y sin salirte de cada tarjeta:
- **CHG-01** Infraestructura de pruebas (proyecto `Wms.IntegrationTests` con Testcontainers/PostgreSQL y Vitest en el frontend).
- **CHG-02** Redacción de datos sensibles en la auditoría (DEF-F7-001), con su script `fase-01-auditoria.sql`.
- **CHG-03** Matriz de permisos por endpoint y por página (DEF-F9-001/002/004/005 y DEF-F7-005), incluida la inclusión de ForeignTrade en `TransportCatalogAccess`.

Cada cambio entrega: el código descrito, las pruebas automatizadas de su tarjeta y el cumplimiento de sus criterios Dado/Cuando/Entonces.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge.** El usuario hace los commits.
- **No edites ni generes migraciones** (`Wms.Infrastructure/Migrations`). Esta fase no requiere migración.
- Los scripts SQL van en `Backend/wms-api/scripts/saneamiento-qa/` con bloque de detección y bloque de corrección. **No los ejecutes contra ninguna base**; solo escríbelos.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes al usuario y textos de interfaz en español. Respeta la estructura por features y las convenciones del repositorio.
- No agregues funcionalidad fuera de las tarjetas. Si encuentras algo que falta o contradice el plan, **detente y repórtalo**; no lo resuelvas por tu cuenta.
- Regla «sin retrocesos»: antes de restringir una política, confirma qué pantallas llaman el endpoint y con qué roles; ningún rol puede perder una función que usa hoy.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` en verde y, con Docker, de `Wms.IntegrationTests` en verde (confirma primero que Docker corre).
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. Lint del frontend: no más de 296 errores y 0 en archivos nuevos.
5. Recorre los criterios de aceptación de las tres tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega y detención
Responde con: archivos creados/modificados por cambio, resultado de cada compuerta (con números), criterios sin verificar, cualquier desviación del plan y el mensaje de commit. **Detente ahí**: no avances a la Fase 2 ni marques la fase como completada; eso lo hace el usuario tras el checkpoint.
