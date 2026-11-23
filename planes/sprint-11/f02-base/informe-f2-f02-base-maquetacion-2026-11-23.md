# Informe — F02 «Base transversal», parte 2 · Maquetación (fase 2, sprint 11)

> **Plan:** [plan-cerrado-f2-f02-base-2026-11-21.md](plan-cerrado-f2-f02-base-2026-11-21.md) (§8). **Prompt:** [prompt-f2-f02-base-maquetacion-2026-11-21.md](prompt-f2-f02-base-maquetacion-2026-11-21.md).
> **Rama:** FE `f2/f02-base`, desde `fase-2` `3aa6e3c` (`develop` no había avanzado: ya estaba en `fase-2`).
> **Cómo se verificó:** `yarn dev` con la sesión simulada (`NUXT_PUBLIC_MOCK_SESSION=true`, `?roles=…`) y `NUXT_PUBLIC_API_BASE` apuntando a un puerto cerrado, para que ninguna pantalla vieja llegue al backend de F01. Los casos QA se recorren contra los datos simulados; se verifican de nuevo en I-01 contra el backend real (plan §6).
> **Datos:** ficticios, como los de los wireframes (`DEC-007`).

Cada fase informa las compuertas de `PM/` §6.2 con las cifras antes y después, los casos QA de la fase y una captura de cada pantalla (carpeta [evidencias/](evidencias/)).

---

## Fase 1 · Base y componentes

**Commit FE:** `d389685` — `feat(base): componentes compartidos, datos simulados y guardias del patrón de listado (DEC-080, F02)`.

### Qué quedó

| Pieza | Archivos (`Frontend/wms/`) |
| --- | --- |
| Contratos | `app/shared/contracts/api.ts`; `app/features/stakeholders/contracts/stakeholder.ts`; `app/features/billing/contracts/billing-recipient.ts` (copiados de `P01/` §2.3; tipos con `z.infer`) |
| Ayudas simuladas (D10) | `app/shared/mocks/list.ts` (`paginate`, `sortBy`, `filterBy`, `listQuery`), `delay.ts`, `problem.ts`, `store.ts`, `session.ts` |
| Sesión simulada (D10) | `app/plugins/mock-session.client.ts`; `runtimeConfig.public.mockSession` en `nuxt.config.ts`; el marco no llama al API con ella activa: `auth-init.client.ts`, `useCurrentUser.ts` (`user/me`), `signalr.client.ts`, `useNotifications.ts` y `api-client.ts` (conexión) |
| Componentes (§2.2) | `AppDataTable.vue`, `AppSearchSelect.vue`, `AppDetailDrawer.vue`, `AppCrudDialog.vue`, `AppChargeForm.vue`, más `AppFormField.vue` (etiqueta encima y error, AF-131); tipos en `app/types/app-table.ts` y `app/types/app-search-select.ts`; mensajes de Zod en español en `app/shared/utils/zod-messages.ts` |
| Fuente de terceros | `app/features/stakeholders/services/stakeholder.source.ts`, `mocks/stakeholder.mock.ts`, `mocks/data/stakeholders.ts` (la usa la galería; la página de Terceros llega en la fase 4) |
| Galería (D20) | `app/pages/dev/components.vue` (solo `yarn dev`, Admin; 404 fuera de desarrollo) |
| Guardias | `test/unit/guards/list-pattern.spec.ts` (D14, reemplaza `page-header.spec.ts`, borrado con `rm`), `mock-sources.spec.ts` (D15), reglas de D17 en `source-guards.spec.ts`; listas en `list-pattern-routes.ts` y `menu-routes.ts` |
| Tema | H-081: el encabezado de `Dialog` no se encoge y el contenido se desplaza bajo él (`app/assets/styles.scss`) |

Decisiones de detalle, sin cambiar ninguna Dn:

- `AppFormField` es un sexto componente pequeño (etiqueta + control + error) para no repetir el marcado en cada modal; lo cubren las guardias D15 y D17 como a los otros cinco.
- Los esquemas del contrato no traen mensajes: `AppCrudDialog` valida con `zodResolver(esquema, { error: zodErrorEs })`, que da los mensajes en español sin cambiar los esquemas.
- `AppSearchSelect` muestra «Mostrando 20 de 27 · desplace para cargar más» con 20 por página (D12); el wireframe dibuja 3 filas como ejemplo. Gana D12 (`DEC-002`).
- `AppChargeForm` acepta `defaultPaymentMethod` (por defecto «Efectivo») solo para que la galería muestre la variante «con otro método» de P-TR-09.
- La guardia D14 admite `F02` como feature de `PENDING` mientras dura la maquetación; la fase 5 la deja sin ninguna.
- Configuración local de `yarn dev` con la sesión simulada en `.claude/launch.json` (`wms-dev-maquetacion`, puerto 3020).

### Compuertas

| Compuerta | Antes (`3aa6e3c`) | Después (`d389685`) |
| --- | --- | --- |
| `yarn build` | código 0 | código 0 |
| `yarn test` | 113 archivos · 608 pruebas, en verde | 122 archivos · 668 pruebas, en verde |
| `yarn lint` | 276 errores · 396 avisos | 276 errores · 396 avisos; 0 en archivos nuevos |
| Sin llamadas reales (D15) | — | `mock-sources.spec.ts` en verde |
| Datos simulados con su esquema (D16) | — | `test/unit/stakeholders/mocks.spec.ts` en verde |
| Rutas nuevas en el menú | — | ninguna |

### Casos QA de la fase (contra los simulados)

| ID | Resultado | Evidencia |
| --- | --- | --- |
| QA2-F02-013 | PASA en la galería: etiquetas encima en el modal a dos columnas, en el alta rápida y en el cobro; sin `FloatLabel` ni `IftaLabel` (guardia D17). Los modales de las páginas se recorren en las fases 3 a 5 | [f1-02](evidencias/f1-02-selector-alta-rapida.jpg), [f1-04](evidencias/f1-04-modal-dos-columnas-error-api.jpg) |
| QA2-F02-014 | PASA: «impor» busca tras la espera, muestra 20 con su NIT y «Mostrando 20 de 27 · desplace para cargar más»; al desplazarse carga los 7 restantes («Mostrando 27 de 27») | [f1-01](evidencias/f1-01-selector-busqueda.jpg) |
| QA2-F02-015 | PASA: «+» › «Importadora Nueva» la crea y queda elegida | [f1-02](evidencias/f1-02-selector-alta-rapida.jpg), [f1-03](evidencias/f1-03-selector-elegido-y-cobro.jpg) |
| QA2-F02-016 | PASA: Efectivo por defecto; con Transferencia aparece «Referencia» y al volver a Efectivo desaparece; nunca hay «Nota» | [f1-03](evidencias/f1-03-selector-elegido-y-cobro.jpg) |
| QA2-F02-017 | PASA: «Tercero registrado» › «+» crea «Cliente Nuevo Ejemplo» y lo deja elegido; «Cobrar» emite un `BillingRecipientInput` válido | [f1-03](evidencias/f1-03-selector-elegido-y-cobro.jpg) |
| QA2-F02-021 | PASA en la galería (adelantado de la fase 2): con el error simulado, la alerta se ve completa bajo el encabezado y el error del campo va en «Código» | [f1-04](evidencias/f1-04-modal-dos-columnas-error-api.jpg) |
| QA2-F02-026 | PASA: guardias `list-pattern` y `mock-sources` en verde | `yarn test` |

Drawer de P-TR-03 en la galería: [f1-05](evidencias/f1-05-drawer-detalle.jpg).
