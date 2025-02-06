import os

# Define the project structure
project_structure = {
    "healthcare_assistant/app/static": [],
    "healthcare_assistant/app/templates": [],
    "healthcare_assistant/app": [
        "__init__.py",
        "models.py",
        "routes.py",
        "nlp_processing.py",
        "tensorflow_model.py",
        "database.py",
    ],
    "healthcare_assistant": [
        "main.py",
        "config.py",
        "README.md",
        "requirements.txt"
    ]
}

# Function to create directories and files
def create_structure():
    for folder, items in project_structure.items():
        os.makedirs(folder, exist_ok=True)  # Ensure directory exists
        for item in items:
            file_path = os.path.join(folder, item)
            with open(file_path, "w") as f:
                f.write("")  # Create an empty file
    
    print("✅ Project structure created successfully!")

# Run the function
if __name__ == "__main__":
    create_structure()
