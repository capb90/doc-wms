-- Palanca de tiempo F11 · S3 (SOLO base local wmsdb, contenedor wms-postgres-db). Patrón de f6_palanca1.sql.
-- Caso: DEF-F6-018 (F6-JOB-002, F6-CAR-011): un solo aviso de vencimiento por factura aunque el job corra varias veces.
-- Acerca el vencimiento de dos facturas aprobadas con saldo a 2 días (ventana del job: 3 días).
BEGIN;
UPDATE invoices SET due_date = now() + interval '2 days', updated_at = now()
 WHERE invoice_number IN ('QA-SIIGO-F11-S3-TRM',   -- almacenamiento 2026BA00015 (QA Cliente Uno), Approved 497.658 sin pagos
                          'QA-SIIGO-F11-0002');    -- almacenamiento 2026EXP00001 (QA Cliente Uno), Approved 178.500 sin pagos
COMMIT;
