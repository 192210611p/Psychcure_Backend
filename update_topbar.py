import os
import re

files_to_modify = {
    "MyGroupsScreen.kt": "My Groups",
    "BrowseGroupsScreen.kt": "Browse Groups",
    "BookCounselorScreen.kt": "Book Appointment",
    "StudentSessionsScreen.kt": "My Sessions",
    "SelfHelpToolsScreen.kt": "Self-Help Tools"
}

dir_path = r"C:\Users\pavithra\AndroidStudioProjects\MINDCARE\app\src\main\java\com\simats\psychcure"

def update_file(filepath, title):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if we need to add Brush import
    if "import androidx.compose.ui.graphics.Brush" not in content:
        content = content.replace("import androidx.compose.ui.graphics.Color", 
                                  "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.Brush")
    
    # We want to replace the TopAppBar with our Box wrapped version.
    # Because TopAppBar takes multiple lines, it's easiest to regex replace the TopAppBar block.
    # Or just find `topBar = { ... TopAppBar(...) }` and replace it entirely.
    
    # Find the block inside topBar = { ... }
    # Let's just find TopAppBar { ... } until the end of the topBar = { block
    
    pattern = re.compile(
        r'topBar\s*=\s*\{\s*TopAppBar\(\s*title\s*=\s*\{\s*Text\("[^"]*",\s*fontSize\s*=\s*([0-9]+)\.sp,\s*fontWeight\s*=\s*FontWeight\.[^,]+,\s*color\s*=\s*[^\})]+\)\s*\},[^)]+\)\s*\}', 
        re.DOTALL
    )
    
    replacement = f"""topBar = {{
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        brush = Brush.horizontalGradient(
                            colors = listOf(
                                MaterialTheme.colorScheme.primary,
                                MaterialTheme.colorScheme.secondary
                            )
                        )
                    )
            ) {{
                TopAppBar(
                    title = {{
                        Text(
                            "{title}",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }},
                    navigationIcon = {{
                        IconButton(onClick = onBackClick) {{
                            Icon(
                                imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                                contentDescription = "Back",
                                tint = Color.White
                            )
                        }}
                    }},
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
                )
            }}
        }}"""

    new_content = pattern.sub(replacement, content)
    
    # if no replacement happened, maybe the signature was slightly different, let's try a softer approach
    if new_content == content:
        # Try a more relaxed pattern
        pattern2 = re.compile(r'topBar\s*=\s*\{\s*TopAppBar\(.*?\)\s*\}', re.DOTALL)
        new_content = pattern2.sub(replacement, content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")
    else:
        print(f"Could not apply to {os.path.basename(filepath)}")

for root, _, files in os.walk(dir_path):
    for file in files:
        if file in files_to_modify:
            filepath = os.path.join(root, file)
            update_file(filepath, files_to_modify[file])

