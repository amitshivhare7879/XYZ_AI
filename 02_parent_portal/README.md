# 02. Parent Portal — XYZ AI

The **Parent Portal** is designed for guardians to track their child's school life, attendance trends, exam report cards, and fee invoices, as well as request direct staff callbacks.

## Key Features
- **Multi-Child Switcher & Verified Ownership**: Parents can only view records of their linked children (e.g. Rahul Patel).
- **Caring & Patient Parent Assistant**: Provides detailed answers, proactively suggesting recent absence dates or fee receipts.
- **Full ERP Visibility**:
  - Attendance Breakdown (91.2% Overall, 8 absences)
  - Report Card (Mid-Term & Final grades in Math, Science, English, etc.)
  - Fee Invoices & Payment Receipts (Term 1 & Term 2)
- **3-State Escalation**: "Talk to Teacher" / "Contact School Management" with explicit confirmation before triggering.
- **3D Avatar & Voice**: Interactive speech synthesis with visemes.

## Running Locally
```bash
python -m http.server 3002 --directory 02_parent_portal
```
Visit: [http://localhost:3002](http://localhost:3002)
