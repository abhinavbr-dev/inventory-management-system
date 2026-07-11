# Inventory Management System — Backend Machine Test (Hancod)

A backend system for inventory management that lets a business configure its
stock outflow strategy — **FIFO**, **FEFO**, or **BATCH** — and correctly
deducts stock across multiple batches during a sale.

Built for the Hancod Backend Machine Test.

---

## Tech Stack

- **Framework:** FastAPI (Python)
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **API Docs:** Swagger UI (auto-generated via FastAPI at `/docs`)

---

## Features

- Per-business configurable inventory outflow strategy (FIFO / FEFO / BATCH),
  stored in the database
- Inventory inward (stock entry) as batches, with `purchase_price`,
  `manufacture_date`, and nullable `expiry_date`
- Sale API that deducts stock across multiple batches based on the
  business's configured strategy
- Strategy-pattern architecture — each outflow mode is an isolated class
  implementing a common interface, making it easy to add a new strategy
  (e.g. LIFO) without touching existing logic
- Transactional, atomic deductions — a sale either fully succeeds or fails
  with no partial stock corruption
- Stock integrity rules: no negative stock, sale fails cleanly on
  insufficient quantity

---

## Data Model

| Table               | Purpose                                                |
|----------------------|---------------------------------------------------------|
| `businesses`         | A business and its configured `inventory_strategy`     |
| `products`           | Product catalog (`name`, `sku`)                        |
| `inventory_batches`  | Stock batches per product (`batch_number`, `quantity`, `purchase_price`, `manufacture_date`, `expiry_date`) |
| `sales`              | One row per sale transaction                            |
| `sale_items`         | Per-batch deduction detail for a sale (product, batch, quantity) |

`sale_items` records every batch touched during a sale, not just a single
total — this makes partial/split batch consumption visible and auditable
directly in the database.

---

## Inventory Outflow Logic

### FIFO — First In First Out
- Batches sorted by `manufacture_date` ascending
- Oldest stock consumed first
- Expiry date is **not** considered in this mode

### FEFO — First Expiry First Out
- Batches sorted by `expiry_date` ascending
- **Expired batches are excluded** from consumption entirely
- Batches with a `null` expiry date are treated as always valid

### BATCH — Explicit Batch Selection
- Caller must specify `batch_number` in the sale request
- Deduction happens only from that batch
- If the specified batch has insufficient stock, the sale fails —
  it does **not** fall back to another batch

All three strategies implement a common interface
(`InventoryStrategyBase.process_sale(...)`), so adding a new strategy (e.g.
LIFO) only requires a new class — no changes to `SalesService` or the API
layer.

---

## Setup Instructions

### Prerequisites
- Python 3.x
- PostgreSQL running locally
- `pip`

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/abhinavbr-dev/inventory-management-system.git
cd inventory-management-system

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Create a .env file with your PostgreSQL connection string, e.g.:
# DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db

# 5. Run database setup
# (adjust to match how your project creates tables — Alembic migration
# or SQLAlchemy Base.metadata.create_all())

# 6. Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive
Swagger docs at `http://127.0.0.1:8000/docs`.

> 📸 *Screenshot: Swagger UI home page
> <img width="1920" height="1080" alt="Screenshot (198)" src="https://github.com/user-attachments/assets/6abacbf7-f422-44f3-96b9-3b5bcd535d29" />

---

## API Reference & Sample Requests

### 1. Configure Inventory Strategy
```
POST /business/{business_id}/inventory-config
```
```json
{ "out_mode": "FIFO" }
```
Valid values: `FIFO`, `FEFO`, `BATCH`

### 2. Add Inventory (Stock Inward)
```
POST /inventory/inward
```
```json
{
  "product_id": 1,
  "batch_number": "BATCH-A",
  "quantity": 10,
  "purchase_price": 100,
  "manufacture_date": "2025-01-01",
  "expiry_date": "2026-12-01"
}
```

### 3. Create Sale
```
POST /sales
```
```json
{
  "business_id": 1,
  "product_id": 1,
  "quantity": 15
}
```

For **BATCH** mode, `batch_number` is required:
```json
{
  "business_id": 3,
  "product_id": 2,
  "quantity": 15,
  "batch_number": "BATCH-X"
}
```

### 4. View Businesses / Products / Inventory
> 📸 *Screenshots: GET Businesses, GET Products, GET Inventory responses
> <img width="1771" height="763" alt="Screenshot 2026-07-11 023407" src="https://github.com/user-attachments/assets/9d443d47-2645-4027-abbb-a1d727d89331" />
<img width="1771" height="763" alt="Screenshot 2026-07-11 023407" src="https://github.com/user-attachments/assets/91419ffc-c636-4048-9d3b-fe231817c474" />
<img width="1771" height="763" alt="Screenshot 2026-07-11 023407" src="https://github.com/user-attachments/assets/11711538-f4ce-4761-85e1-7ec757f59087" />
---

## Demo Walkthrough (as tested)

### FIFO
- Business: `ABC Pharmacy` (business_id: 1), strategy: `FIFO`
- Product: `Vitamin C` (product_id: 1) with batches A (oldest), B (newest), C (mid, expired)
- Sale of 15 units → deducted 10 from BATCH-A, 5 from BATCH-C; BATCH-B untouched
- Confirms outflow ignores expiry and strictly follows purchase order

> 📸 *Screenshots: Inventory before FIFO → POST Sale response → Inventory after FIFO*
> <img width="1771" height="763" alt="Screenshot 2026-07-11 023407" src="https://github.com/user-attachments/assets/6c6ace5b-ac59-490c-bb30-6e273309eb83" />
<img width="1759" height="395" alt="Screenshot 2026-07-11 030230" src="https://github.com/user-attachments/assets/b8f10b72-5352-443d-8987-88df8451deeb" />
<img width="1766" height="934" alt="Screenshot 2026-07-11 030340" src="https://github.com/user-attachments/assets/09b68fb7-462e-4b8f-95de-0b76a033945b" />


### FEFO
- Business: `MediCare Pharmacy` (business_id: 2), strategy: `FEFO`
- Product: `Paracetamol 500mg` (product_id: 2) with batches D, E (soonest valid expiry), F (expired)
- Sale of 15 units → deducted 10 from BATCH-E, 5 from BATCH-D; BATCH-F (expired) untouched
- Confirms expired batches are correctly excluded from consumption

> 📸 *Screenshots: Inventory before FEFO → POST Sale response → Inventory after FEFO*
> <img width="1771" height="939" alt="Screenshot 2026-07-11 030756" src="https://github.com/user-attachments/assets/68ee488a-f8c2-4714-9417-3fd58566d00d" />
<img width="1770" height="381" alt="Screenshot 2026-07-11 032657" src="https://github.com/user-attachments/assets/c4ab26f2-19c5-4b10-9b65-d591b6550aa6" />
<img width="1762" height="899" alt="Screenshot 2026-07-11 032855" src="https://github.com/user-attachments/assets/89d3f22d-a618-441c-9673-b1366451417c" />


### BATCH
- Business: `Central Warehouse` (business_id: 3), strategy: `BATCH`
- Product 2 with batches X (20 units) and Y (5 units)
- Successful sale: 15 units from BATCH-X only, BATCH-Y untouched
- Failure case: requesting 10 units from BATCH-Y (only 5 available) fails with a 400 error, proving stock integrity is enforced rather than silently falling back to another batch

> 📸 *Screenshots: Inventory before Batch → POST Sale (success) → POST Sale (failure case) → Inventory after Batch*
<img width="1766" height="891" alt="Screenshot 2026-07-11 033155" src="https://github.com/user-attachments/assets/6d1350e0-0a68-4e2f-a74f-0d07483f1c5e" />
<img width="1767" height="406" alt="Screenshot 2026-07-11 033450" src="https://github.com/user-attachments/assets/95963339-e206-4a28-a0ce-72436f996558" />
<img width="1764" height="897" alt="Screenshot 2026-07-11 033619" src="https://github.com/user-attachments/assets/c401f316-de7b-4d77-a7f6-f091a664e482" />

### Database Verification
```sql
SELECT * FROM sales;
SELECT * FROM sale_items;
```
Confirms every sale has matching per-batch deduction rows recorded in
`sale_items`, proving partial batch consumption is persisted, not just
returned transiently in the API response.

> 📸 *Screenshot: final `sales` and `sale_items` table dumps*
> <img width="1920" height="1080" alt="Screenshot (200)" src="https://github.com/user-attachments/assets/7303408b-9265-41c1-9fed-30129f32cbd6" />


---

## Assumptions Made

- Each sale request handles a single product; the schema does not currently
  support multiple product line items within one sale transaction
- A batch with `expiry_date = null` is treated as never expiring
- The inventory strategy applied to a sale is always whatever is currently
  stored for that sale's `business_id`
- No authentication was implemented, per the assignment's explicit scope
  (auth was listed as not being evaluated)
- No frontend was built — this is an API-only implementation, tested via
  Swagger UI
---

## Author

**Abhinav B R**
GitHub: [abhinavbr-dev](https://github.com/abhinavbr-dev)
LinkedIn: [abhinavbr-dev](https://linkedin.com/in/abhinavbr-dev)
