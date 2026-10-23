-- Palanca de tiempo F11 · S1 (SOLO base local wmsdb, contenedor wms-postgres-db). Patrón de f8_palanca_mora.sql.
-- Casos: DEF-F6-006 (F6-CAR-001/002/003), DEF-F6-005 (F6-CAR-005), REG-025 (F6-CAR-009, guía bloqueada).
BEGIN;
-- Emitidas: vencidas hace 2 días
UPDATE invoices SET due_date = now() - interval '2 days', updated_at = now()
 WHERE invoice_number IN ('QA-SIIGO-F11-0011',      -- QA Multirol (límite 0), PartiallyPaid 10.000 de 28.560
                          'QA-SIIGO-F11-0001',      -- QA Cliente Uno (sin límite), PartiallyPaid 250.000 de 496.670,28
                          'QA-SIIGO-F11-S1-0002');  -- QA Cliente Mora (límite 1.000), Approved 89.250 sin pagos
-- Borradores con vencimiento pasado (F6-CAR-005: un borrador no debe vencer)
UPDATE invoices SET due_date = now() - interval '2 days', updated_at = now()
 WHERE id IN ('568d8ac9-926e-404d-a12f-cdc1328b0771',                           -- BASCULA por facturar QA Cliente Consolidado 28.560 (Draft)
              '9457d5fe-355e-45b7-b3d8-f012328f45f7'); -- MONTACARGAS por facturar QA Cliente Uno 35.700 (Draft, S0)
COMMIT;
