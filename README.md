# Glucose Tracker API

## How to Run the Project


Follow these steps to set up and run the project:

1. **Make Migrations:**
    ```bash
    make makemigrations
    ```

2. **Create a Superuser (optional but recommended for admin access):**
    ```bash
    make createsuperuser
    ```

3. **Start the Docker Containers:**
    ```bash
    make up
    ```

The application should now be running on `http://127.0.0.1:8000/`.

---

## How It Works

### **Filtering**

- Get records for a specific user:
  ```sh
  GET /api/v1/levels/?user_id=<UUID>
  ```
- Get records in a specific time range:
  ```sh
  GET /api/v1/levels/?start=2024-01-01T00:00:00&stop=2024-02-01T00:00:00
  ```

### **Sorting (Optional)**

- Get records sorted by timestamp (latest first):
  ```sh
  GET /api/v1/levels/?ordering=-timestamp
  ```

### **Pagination (Optional)**

- Limit the response to 5 items:
  ```sh
  GET /api/v1/levels/?limit=5
  ```

### **Retrieve a Single Record**

- Get a specific glucose record by ID:
  ```sh
  GET /api/v1/levels/<id>/
  ```

---

## **Uploading Data via CSV File**

Use the following command to upload glucose data via a CSV file:

```sh
curl -X POST -F "file=@path/to/your/file.csv" http://127.0.0.1:8000/upload-glucose/
```

Replace `path/to/your/file.csv` with the actual path to your CSV file.

---

## **Populate Glucose Data (Bulk Upload)**
You can also populate glucose data in the database via an API endpoint. This is helpful for bulk uploads, especially when working with a set of glucose records.
```sh
POST /api/v1/levels/populate/
```
To upload data via this endpoint, send a JSON array of glucose records in the request body. Example:
```sh
curl -X POST -H "Content-Type: application/json" -d '[
  {
    "user_id": "e09bb0f0-018b-429b-94c7-62bb306a0136",
    "timestamp": "2024-03-28T09:00:00",
    "record_type": 1,
    "glucose_value_trend": 120,
    "glucose_scan": 125
  },
  {
    "user_id": "d06bb0f0-018b-429b-94c7-62bb306a0137",
    "timestamp": "2024-03-29T10:15:00",
    "record_type": 0,
    "glucose_value_trend": 130,
    "glucose_scan": 135
  }
]' http://127.0.0.1:8000/api/v1/levels/populate/
```
This will add multiple glucose records to the database at once.


## **Contributing**

1. **Format Code** before committing:
   ```sh
   make format
   ```
2. **Run Tests**:
   ```sh
   make test
   ```

