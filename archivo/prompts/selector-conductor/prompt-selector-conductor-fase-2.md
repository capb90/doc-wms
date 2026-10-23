Eres el implementador de la **Fase 2 (frontend)** del selector de conductor del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5**. En Báscula y en la Recepción Directa de Bodega reemplazas el formulario completo del conductor por un select con buscador en el servidor, un botón «+» que registra en un modal y un botón lápiz que corrige en el mismo modal. Lo cubres con pruebas. **Solo frontend**: el backend ya quedó en la Fase 1 y no se toca.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que cita (`code_workspace/docs/contexto/contexto-negocio-wms-para-ia.md`).
2. **El plan cerrado** `code_workspace/docs/planes/plan-cerrado-selector-conductor-2026-10-08.md`, aprobado el 2026-10-08. Léelo entero; tu alcance es **§5 y §6**, con las decisiones **D6 a D19** de §2. §7 y §8 (QA y staging) son fases posteriores: no las ejecutes.
3. **El código que vas a tocar o imitar** (todo en `Frontend/wms`):
   - `app/features/entries/components/DriverForm.vue` (el formulario que va al modal), `CreateDriverDialog.vue` (no se toca; solo referencia de modal);
   - `app/features/entries/services/driver-service.ts`, `composables/useDrivers.ts`, `composables/useMutations.ts` (`useCreateDriver`, `useUpdateDriver`), `types/driver.ts`;
   - `app/features/weighbridge/components/CompleteEntryInfo.vue` (card «Camión y conductor»: `missingFields`, `ID_TYPE_LABELS`, `invalidFields`, foco al primer faltante);
   - `app/features/warehouse/components/ReceptionStepManualInfo.vue` (validación de las líneas 144-147) y `app/features/warehouse/utils/manual-reception.ts` (contrato que no cambia);
   - **patrón del select con búsqueda en el servidor:** `app/features/warehouse/components/WarehouseDepositSelect.vue`;
   - **patrón de prueba de componente:** `test/components/weighbridge/AdditionalDepositCollect.spec.ts`; la prueba existente `test/components/warehouse/ReceptionStepManualInfo.spec.ts`;
   - errores del API: `app/utils/api-error.ts` (`ApiError`, `normalizeApiError`, `claimApiError`) y un diálogo que ya lo use (`grep -rln claimApiError app`).

## Situación de partida
- Backend `develop` en **`3748ec6`** (Fase 1 commiteada). Ya existe:
  - `GET /drivers` con `search` (unaccent + ILIKE en nombres, apellidos, ambos órdenes y documento sin espacios) y `orderByName`, además de `isActive`, `pageIndex` y `pageSize`. La respuesta trae `data` y `pagination.totalCount`.
  - `POST /drivers` y `PATCH /drivers/{id}` bajo `DriverCatalogAccess`, que incluye a Warehouse.
- Frontend `develop`: el plan se escribió sobre `e01d81d`. Anota el hash con que empiezas (`git rev-parse --short HEAD`).
- Sin cambios de backend ni de esquema en esta fase.

## Reglas
1. Trabaja en `develop`. **No crees ramas ni hagas commits**: el usuario commitea al revisar.
2. No toques el backend, `CreateDriverDialog.vue`, `LoadingOrderForm.vue`, `pages/admin/drivers/index.vue`, `pages/operations/entries/index.vue` (Vigilancia, `DriverForm` comentado) ni `manual-reception.ts`.
3. **Contrato con los padres (D14).** `DriverPicker` emite exactamente lo que emitía `DriverForm`: `update:modelValue` con `Partial<IDriverFormData>` y `edited`. `getEntryInfo()` y `buildManualReceptionRequest()` no cambian.
4. `DriverForm.vue` solo gana props y un emit opcionales (§5.3). Con los valores por defecto se comporta igual que hoy.
5. **Si el código contradice el plan, no improvises.** Detente y pregunta, con todas las dudas en un solo mensaje. Casos concretos que exigen detenerse:
   - el truco de `filter-fields` (D8) no evita que PrimeVue oculte resultados del servidor;
   - Enter en el filtro del select dispara el «Guardar» de la ficha (§6).
6. Textos de UI en español, exactamente los del plan. Densidad de comentarios como el código vecino: cabecera JSDoc del componente y comentarios cortos con la decisión (`D8 —`, `D16 —`…).
7. **Autenticación en local.** Solo inicias sesión en `http://localhost:3000`, con las cuentas de prueba de `Frontend/wms/README.md`. No copies contraseñas a la salida ni a archivos.

## Pasos
1. **Línea base.** Antes de cambiar nada:
   - `yarn test` y anota el conteo;
   - `yarn lint -f json -o <scratchpad>/lint-base.json` y anota el total de errores (la última medición conocida es 279).
2. **Utilidades** (§5.1): crea `app/features/entries/utils/driver-option.ts` con las cinco funciones y el mapa `ID_TYPE_SHORT_LABELS`. En `CompleteEntryInfo.vue`, cambia `ID_TYPE_LABELS` por el mapa importado.
3. **Servicio** (§5.2): agrega `search?` y `orderByName?` a `IGetDriversQuery`.
4. **`DriverForm.vue`** (§5.3): `hideHeader`, `lockDocument`, `submitLabel`, `submitting` y el emit `found`.
5. **`DriverFormDialog.vue`** (§5.4): modos create y edit, la tabla de casos al enviar (D9 a D12). Reglas para las mutaciones:
   - `useUpdateDriver` recibe `{ id, data }` y ya muestra sus propios avisos: no agregues otro aviso de éxito;
   - el 409 de create se resuelve con `getDriverByDocument` (D11), sin aviso de error duplicado (`claimApiError`).
6. **`DriverPicker.vue`** (§5.5): el select con `filter-fields` (D8), la consulta paginada (D6), la etiqueta (D7), el pie, «+» y lápiz con `aria-label`, la precarga (D16), el país (D15) y la tabla de comportamiento. La precarga de D16 **no reemplaza** una selección que el operario haya hecho antes de que responda la consulta (§10 del plan).
7. **Padres** (§5.6):
   - en `CompleteEntryInfo.vue`, el picker en modo `compact` y los faltantes unificados en `driverId` (D17); comprueba que «Guardar» con conductor vacío lleve el foco a `#driverId [role='combobox']`;
   - en `ReceptionStepManualInfo.vue`, el picker y el mensaje de D18;
   - actualiza los comentarios de cabecera de ambos.
8. **Pruebas** (§5.7): `test/unit/entries/driver-option.spec.ts`, `test/components/entries/DriverPicker.spec.ts`, `test/components/entries/DriverFormDialog.spec.ts` y el ajuste de `ReceptionStepManualInfo.spec.ts`.
9. **Verificación** (§5.8):
   - `yarn test` todo verde, guardias incluidas;
   - lint igual o menor que la base;
   - `vue-tsc` limitado a los archivos tocados.
10. **Prueba manual en local** (§5.8 y §6). Necesitas el API en 5281 con el build `3748ec6` y el front en 3000. Con `bascula`:
    - toma un camión de la cola y busca por nombre, por documento y sin tildes;
    - registra uno con «+» (datos `QA-SEL`, documento `9000000001`), prueba «+» con ese mismo documento (D10) y corrige su teléfono con el lápiz;
    - guarda la ficha y verifica el conductor del ingreso;
    - recorre el flujo solo con teclado: Tab, escribir, Enter, Tab.

    Con `bodega`, en «Recepción Directa», elige un conductor, registra otro con «+» (`9000000002`) y comprueba el mensaje de D18 sin conductor. **No guardes la recepción.**

    Anota lo que viste. Si algo no se puede probar (sin camión en cola, sin API), dilo; no lo des por probado.

## Trampas conocidas (memoria del proyecto)
- **Lint**
  - `yarn lint` sin `-f json` no da un total cómodo: mide con el JSON.
  - La regla `vue/attributes-order` avisa si `locale` u otras props van antes de `id` o `v-model`.
- **Guardias de botones.** La guardia exige `label`, `aria-label` o `title` en cada `<Button>`; `v-tooltip` no da nombre accesible. Las guardias de `test/unit/guards` también prohíben `toLocale*`, `new Intl.*` y `<InputNumber>` sin `locale="es-CO"`.
- **Plantillas.** En las plantillas, los literales dentro de un atributo van con comillas simples (`'filterText'`). Una comilla doble dentro de `:attr="…"` rompe el parseo y tumba varias suites.
- **`vue-tsc`**
  - El tsconfig global se corta por errores ajenos. Usa vue-tsc 3 instalado en el scratchpad, con un tsconfig temporal que extienda `.nuxt/tsconfig.app.json` e incluya solo tus archivos.
  - Compara contra `HEAD` si dudas.
  - En macOS no hay `timeout`.
- **Archivos regenerados.** `yarn build` / `yarn generate` regeneran `app/components.d.ts`. Si cambia solo por eso, no lo incluyas en el resumen como cambio tuyo.
- **Mayúsculas y minúsculas.** El volumen `/Volumes/Dock` distingue mayúsculas: una copia en `/private/tmp` mezcla `app/features/Administration` y `administration`. Trabaja en el repositorio.
- **zsh**
  - Un patrón `--include=*.vue` sin comillas falla con «no matches found».
  - Un `grep $(...)` con la sustitución vacía se cuelga: pasa `</dev/null`.
- **Precarga asíncrona de `@primevue/forms`.** El formulario toma `initial-values` al montarse. Por eso el modal monta `DriverForm` con `v-if="visible"`: cada apertura es un formulario limpio.

## Entrega y detención
Al terminar, **detente** y entrega un resumen con:
1. el hash inicial y los archivos tocados y nuevos (`git status --short`);
2. los conteos de Vitest antes y después, con las pruebas nuevas por archivo;
3. los errores de lint antes y después, y el resultado de `vue-tsc` en tus archivos;
4. el resultado de la prueba manual, paso por paso: qué pasó y qué no se pudo probar;
5. lo que verificaste de §6: clics, Enter en el filtro, foco del modal y Esc;
6. las desviaciones del plan con su motivo, o «ninguna»;
7. un mensaje de commit propuesto, por ejemplo `feat(bascula,bodega): selector de conductor con alta y edición en modal`, que termine con la línea de coautoría de tu modelo.

**No empieces la Fase 3** hasta que el usuario commitee esta fase y la autorice.
