# 🚀 Purchase Order Multi-Level Approval Module

This Odoo module adds a dynamic, three-tier approval workflow to Purchase Orders based on configurable thresholds in the company settings. 
Approval requests are automatically emailed to the appropriate manager—Purchase, Finance, or Director—based on the total order value.

---

## 📦 Features

✅ Dynamic three-level approval flow:
- **Purchase Manager**
- **Finance Manager**
- **Director**

✅ Email notification system with:
- Only **one template**
- Dynamically resolved recipient and role  
- Email context set from Python code

✅ Tracks:
- Who approved at each level
- When approvals were made
- Who refused and why

✅ New approval states:
- `waiting finance approval`
- `waiting director approval`

---

## ⚙️ Setup Instructions

### 1. Approval Limits

Navigate to:
Settings → Companies → Your Company

Set:
- `Manager Approval Limit`
- `Finance Manager Approval Limit`
- `Director Approval Limit`

### 2. Assign Managers in Purchase Order

Open a Purchase Order and assign:
- `Purchase Manager`
- `Finance Manager`
- `Director Manager`

---

## 📨 Email Template

Only one template is used for all notifications:
- **ID**: `email_template_po_approval_notification`

Context fields injected from backend:
- `manager_email` – recipient
- `manager_role` – role name

### Template Example

```html
<p>Dear <t t-out="ctx.get('manager_role')"/> ,</p>
<p>The Purchase Order <strong><t t-out="object.name"/></strong> requires your approval.</p>
<p>Total Amount: <strong><t t-out="object.amount_total"/></strong></p>
<p>Thank you.</p>
