from database import query_db
res = query_db("SHOW COLUMNS FROM group_members LIKE 'status'")
print("group_members status:", res)
