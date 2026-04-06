import os

dir_path = r"C:\Users\pavithra\AndroidStudioProjects\MINDCARE\app\src\main\java\com\simats\psychcure"

for root, _, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".kt"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content.replace("com.example.psychcure", "com.simats.psychcure")
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed package name in {file}")
