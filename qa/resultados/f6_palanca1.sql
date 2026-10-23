-- Palanca de tiempo F6 (base local wmsdb, datos QA). 2026-10-02 ~20:35 -05
UPDATE invoices SET due_date = now() - interval '2 days'
 WHERE id IN ('b8f9c06d-45f6-4723-9d70-b881a190cb2c',  -- QA-SIIGO-0041 Mora 17.850 Approved sin pagos (CAR-001/003)
              'f1836b3f-d748-4dce-9b6a-55e70f521a3b',  -- QA-SIIGO-0011 Uno 501.865,34 Approved con pago parcial (CAR-002/006)
              '88a57db1-282d-4999-baa3-e4d05d211cb8',  -- QA-SIIGO-0013 Multirol 17.850 Approved, límite 0 (CAR-007)
              '1a95277b-eab3-4144-9ec8-b38d2ef6c56f'); -- QA-SIIGO-0014 Consolidado 1.068.660 Approved, límite 10M (CAR-004)
UPDATE invoices SET due_date = now() + interval '2 days'
 WHERE id = '92dd3690-ec82-4361-b8e4-514a0bfaafc9';      -- QA-SIIGO-0018 Uno Draft (CAR-011 aviso de vencimiento)
UPDATE storage_billing_periods SET limit_date = (now() - interval '1 day')::date
 WHERE id = '19651dae-3291-49c2-9d76-f2a4ff6076a6' AND status = 'Open';  -- BA00013 período semanal (ALM-015)
SELECT id, status, due_date, amount_paid FROM invoices WHERE id IN ('b8f9c06d-45f6-4723-9d70-b881a190cb2c','f1836b3f-d748-4dce-9b6a-55e70f521a3b','88a57db1-282d-4999-baa3-e4d05d211cb8','1a95277b-eab3-4144-9ec8-b38d2ef6c56f','92dd3690-ec82-4361-b8e4-514a0bfaafc9','89bcb58a-bf1d-4b62-a398-02bcf2316ee1','8299c9c7-104a-4c2b-a470-5014a80deb47','65da4c43-d169-456e-850d-c1d3a365d476');
SELECT name, financial_status FROM stakeholders WHERE name LIKE 'QA %' ORDER BY name;
