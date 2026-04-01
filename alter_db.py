from database import query_db
try:
    query_db("ALTER TABLE sessions MODIFY COLUMN status ENUM('pending', 'confirmed', 'cancelled', 'completed', 'rejected') DEFAULT 'pending'", commit=True)
    print("Success: Added 'rejected' to sessions status enum")
except Exception as e:
    print("Error:", e)
