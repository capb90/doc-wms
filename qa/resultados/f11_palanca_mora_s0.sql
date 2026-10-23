-- F11 S0 (2026-10-05): palanca de mora, solo base local wmsdb (contenedor Docker wms-postgres-db).
-- Mismo patrón que f8_palanca_mora.sql. Vence la factura aprobada de QA Cliente Mora SAS (límite de crédito 1.000)
-- para que el job OverdueDetectionBackgroundService la marque Overdue y bloquee al cliente en su siguiente corrida.
SELECT i.invoice_number, i.status, i.total, i.pending_amount, i.due_date
  FROM invoices i JOIN stakeholders s ON s.id = i.customer_id
 WHERE s.name = 'QA Cliente Mora SAS' AND i.invoice_number = 'QA-SIIGO-F11-0010';
UPDATE invoices SET due_date = now() - interval '2 days' WHERE invoice_number = 'QA-SIIGO-F11-0010';
SELECT invoice_number, status, due_date FROM invoices WHERE invoice_number = 'QA-SIIGO-F11-0010';
