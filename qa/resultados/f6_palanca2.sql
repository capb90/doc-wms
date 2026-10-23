-- Palanca 2 (2.º reinicio) 2026-10-02 ~20:47 -05
UPDATE storage_billing_periods SET limit_date = DATE '2026-10-01'
 WHERE id = '19651dae-3291-49c2-9d76-f2a4ff6076a6' AND status = 'Open';  -- BA00013 (ALM-015)
SELECT id, limit_date, status FROM storage_billing_periods WHERE id = '19651dae-3291-49c2-9d76-f2a4ff6076a6';
SELECT id, status, amount_paid, due_date FROM invoices WHERE id IN ('b8f9c06d-45f6-4723-9d70-b881a190cb2c','88a57db1-282d-4999-baa3-e4d05d211cb8');
