-- F11-S5 · Palanca de tiempo para el abandono (F5-ABA-001 a 003). SOLO BASE LOCAL (wmsdb en wms-postgres-db).
-- Se ejecuta el 2026-10-06 con el API corriendo; no hace falta reiniciarlo: el listado de abandono calcula los días al consultar.
-- Depósitos QA de importación sin nacionalizar:
--   2026BA00015 (QAJ101, fecha de ingreso original 2026-10-03 14:30:00+00) → hace 25 días (EnAlerta: plazo 30, alerta desde 20).
--   2026BA00003 (fecha de ingreso original 2026-10-05 22:41:12.002939+00) → hace 35 días (EnAbandono).

-- 1) Aplicar
UPDATE warehouse_storages SET entry_date = now() - interval '25 days'
 WHERE warehouse_storage_number = '2026BA00015';
UPDATE warehouse_storages SET entry_date = now() - interval '35 days'
 WHERE warehouse_storage_number = '2026BA00003';

-- 2) Restaurar al terminar los casos
-- UPDATE warehouse_storages SET entry_date = '2026-10-03 14:30:00+00' WHERE warehouse_storage_number = '2026BA00015';
-- UPDATE warehouse_storages SET entry_date = '2026-10-05 22:41:12.002939+00' WHERE warehouse_storage_number = '2026BA00003';
-- La prórroga que registra F5-ABA-003 es irreversible por diseño: queda en 2026BA00015 (extension_registered_at).

-- F11-S5 · Palanca de tiempo para los jobs de facturación (F6-ALM-015 y F6-CAR-004). SOLO BASE LOCAL.
-- Requiere un reinicio del API (lo hace el usuario) para que corran StoragePeriodAutoCloseJob y OverdueDetectionJob.
-- 3) Período vencido de 2026BA00040 (QA Cliente REG F11, PER_VEHICLE, período 06/10–06/11, límite original 2026-11-09):
UPDATE storage_billing_periods SET limit_date = (now() - interval '2 days')::date
 WHERE id = '55cca7d0-6140-454b-9286-bec603e0f030' AND status = 'Open';
-- 4) Factura vencida de QA Cliente Consolidado (límite de crédito 10.000.000): QA-SIIGO-F11-S4-0010, PartiallyPaid, pendiente 360,
--    vencimiento original 2026-10-21 14:45:54.270068+00:
UPDATE invoices SET due_date = now() - interval '2 days' WHERE id = '15428832-8aaa-4b53-8ec7-93c1ca7e9d2a';
-- Restauración tras el caso: se paga el saldo de 360 (la factura queda Paid y el cliente vuelve a Active) y se repone el vencimiento:
-- UPDATE invoices SET due_date = '2026-10-21 14:45:54.270068+00' WHERE id = '15428832-8aaa-4b53-8ec7-93c1ca7e9d2a';
