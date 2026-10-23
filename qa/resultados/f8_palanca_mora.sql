-- F8 E2E-12: vencer factura aprobada de QA Cliente Mora (base local)
SELECT i.invoice_number, i.status, i.total, i.pending_amount, i.due_date FROM invoices i JOIN stakeholders s ON s.id=i.customer_id WHERE s.name='QA Cliente Mora SAS' AND i.invoice_number='QAE-SIIGO-003';
UPDATE invoices SET due_date = now() - interval '2 days' WHERE invoice_number='QAE-SIIGO-003';
SELECT invoice_number, due_date FROM invoices WHERE invoice_number='QAE-SIIGO-003';
