Eres el implementador de la corrección de **DEF-F11-001**, un defecto que encontró la sesión S0 del re-test de QA (fase 11) del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad baja: dos handlers del backend y sus pruebas). Las 12 fases del plan de corrección están completadas y con commit. **El re-test de QA está en curso sobre la base local: no la toques.**

## El defecto
- **Síntoma.** Después de `POST auth/change-password`, el token que entrega un login inmediato con la contraseña nueva recibe **401** en `GET user/me` durante unos 15 segundos. Después de ese tiempo responde 200. Pasa en el primer ingreso de cada usuario nuevo, que está obligado a cambiar la contraseña (F1-AUT-010).
- **Evidencia.** `docs/qa/resultados/evidencias/F11/S0-03-cache-sesion-15s.txt` y la fila del hallazgo en `docs/qa/resultados/F11-informe-S0-2026-10-05.md`.
- **Causa (confirmada en el código).** CHG-16 (Fase 4) introdujo `Wms.Infrastructure/Services/UserSessionGuard.cs`, que guarda 15 s en memoria `{IsActive, SecurityStamp}` del usuario. Los handlers que rotan el sello llaman `sessionGuard.Invalidate(user.Id)` para descartar esa copia: `LogoutHandler`, `ResetPasswordWithTokenHandler`, `ResetUserPasswordHandler`, `ManageUserActivationHandler`, `AssignRolesToUserHandler` y `RemoveRolesToUserHandler`. **Dos no lo hacen:**
  1. `Wms.Application/Auth/Commands/ChangePassword/ChangePasswordHandler.cs`: `ResetPasswordAsync` rota el sello y la caché conserva el viejo. Es el caso que vio QA.
  2. `Wms.Application/Users/Commands/UpdateUser/UpdateUserHandler.cs`: `SetUserNameAsync` y `SetEmailAsync` también rotan el sello en Identity. Si un administrador cambia el usuario o el correo de alguien, esa persona tiene la misma ventana de 15 s al volver a entrar. Es la misma causa y se corrige en esta tarea.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (en especial 4.0.2 migraciones y 4.0.10 «Sin retrocesos funcionales») y la tarjeta **CHG-16**.
3. `UserSessionGuard.cs`, `Wms.Api/Common/Identity/WmsAuthentication.cs` (la validación del sello en cada petición), los seis handlers que ya invalidan (copia su forma y su comentario) y `Wms.IntegrationTests/Security/SessionRevocationTests.cs`.
4. En el frontend, solo para entender el flujo, sin modificarlo: `app/pages/auth/change-password.vue`, `app/features/auth/composables/useChangePassword.ts` y el interceptor de 401 de `app/plugins/api-client.ts`.

## Alcance (cerrado)
1. **`ChangePasswordHandler`:** inyecta `IUserSessionGuard` y llama `sessionGuard.Invalidate(user.Id)` al final, después del `UpdateAsync` que pone `MustChangePassword = false`. Agrega un comentario en el estilo de los demás (`// CHG-16 / DEF-F11-001 — …`).
2. **`UpdateUserHandler`:** si se cambió el usuario o el correo (y no hubo errores), llama `sessionGuard.Invalidate(userFromDb.Id)` antes del `return`. Si solo cambia el perfil (nombre, identificación o teléfono), no invalides: esos cambios no rotan el sello.
3. **Pruebas de integración** en `SessionRevocationTests.cs` (un `[Fact]` por caso). Cada prueba debe **calentar la caché** con una petición del token viejo antes del cambio; si no, pasaría aunque falte la corrección:
   - `ChangePassword_NewLoginTokenWorksImmediately`: login → `GET user/me` (200, calienta la caché) → `POST auth/change-password` (204) → login con la contraseña nueva → `GET user/me` con el token nuevo **en el acto** → 200.
   - `ChangePassword_OldTokenGets401_RefreshKeepsSession`: tras el cambio, el token viejo recibe 401 en el acto, y `POST auth/refresh-token` con la sesión vieja responde 200 con un token que pasa en `user/me`. **Esta prueba protege la sesión abierta del usuario** (ver «Sin retrocesos»).
   - `UpdateUsername_NewLoginTokenWorksImmediately`: el usuario entra y calienta la caché → un Admin le cambia el nombre de usuario → el usuario entra con el nombre nuevo → `GET user/me` → 200 en el acto. Si `WmsApiFactory.LoginAsync` no permite entrar con otro nombre de usuario, usa el endpoint de login directamente.
   - **Comprueba que las pruebas fallan sin la corrección:** escríbelas primero, córrelas en rojo (la primera y la tercera deben dar 401) y después aplica el cambio. Reporta ese rojo con la salida resumida.
4. **Ficha del defecto:** crea `docs/qa/resultados/defectos/DEF-F11-001.md` con `docs/qa/plantillas/defecto.md`. Usa severidad MINOR, módulo «Autenticación / Seguridad», casos F11-S0-02 y F1-AUT-010, y estado **Corregido**. En el Historial pon una fila «Detectado» (2026-10-05, S0, «Claude (QA)») y otra «Corregido» con el resumen y «commits: pendiente». La pista técnica es la causa de arriba. No modifiques el informe de S0 ni las demás fichas.

**Fuera de alcance (decidido, no lo reabras):**
- **No revoques los refresh tokens en `ChangePasswordHandler`.** El frontend sigue en la misma sesión después del cambio. Con la corrección, su siguiente petición recibe 401 y el interceptor la renueva con el refresh token. Si se revocara, el usuario quedaría expulsado justo después de cambiar la contraseña. Es una regresión (regla 4.0.10).
- No cambies la duración de la caché (15 s), `UserSessionGuard`, `SessionValidityRules`, `RefreshTokenHandler`, el contrato del endpoint (sigue respondiendo 204 sin cuerpo) ni el frontend.

## Sin retrocesos (regla 4.0.10)
- **El usuario que cambia su contraseña no puede quedar fuera de su sesión.** La prueba `ChangePassword_OldTokenGets401_RefreshKeepsSession` lo demuestra en el API. Además, revisa en el código del interceptor que un 401 con refresh token disponible renueva el token y no cierra sesión. Explica en la entrega, en dos o tres líneas, por qué el flujo de `/auth/change-password` → inicio del rol sigue funcionando.
- Las tres pruebas existentes de `SessionRevocationTests` y las de `PasswordPolicyTests` pasan sin editarlas.

## Base de datos y entorno
- **No uses la base local ni el API local**: tienen el dataset del re-test de QA (S1 en adelante). No crees usuarios ni cambies contraseñas ahí y no reinicies el API. Las pruebas de integración usan su propio PostgreSQL con Testcontainers (Docker activo).
- No hay migración: el modelo no cambia. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Si algo lo exigiera, detente y repórtalo; nunca edites archivos generados.

## Restricciones (obligatorias)
- Trabaja en `develop`. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies contraseñas ni secretos (las pruebas usan las contraseñas de prueba que ya genera `WmsApiFactory`). No toques producción ni `infra/`.
- Textos y comentarios en español. Respeta la estructura por features.
- Nada fuera del alcance anterior. Si el código real contradice este prompt, adapta a lo que hay sin cambiar el comportamiento pedido y anótalo; si el comportamiento cambia, detente y repórtalo.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` (1518 hoy) y `Wms.IntegrationTests` (229 hoy, más las 3 nuevas) en verde.
3. `has-pending-model-changes` sin cambios.
4. El frontend no se toca: no hace falta `yarn lint` ni `yarn test`. Confirma con `git status` que `Frontend/wms` solo tiene la ficha nueva (y este prompt, que no es tuyo).

## Entrega
Responde con:
1. Los archivos modificados o creados.
2. La salida resumida de las pruebas nuevas **en rojo** (antes de la corrección) y en verde (después).
3. El resultado de cada compuerta, con números.
4. La explicación de por qué la sesión abierta sobrevive al cambio de contraseña.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(qa-f11): invalidar la caché de sesión al cambiar la contraseña o el usuario (DEF-F11-001)`, con una línea por cambio.
   - **Frontend (solo documentación):** `docs(qa-f11): ficha DEF-F11-001 corregida`. Indica que `docs/archivo/prompts/qa/prompt-def-f11-001.md` puede ir en el mismo commit.
   - Los dos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La verificación del defecto en la interfaz la hace QA en la S2 (F1-AUT-010) después de reiniciar el API con este cambio.
