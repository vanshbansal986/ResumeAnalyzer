CONFIG_FILE_PATH = "config.yaml"

dtype_map = {
    "name": str,
    "phone": str,
    "university": str,
    "year_of_study": str,  # Force as string to avoid Excel interpreting it as a number
    "course": str,
    "cgpa": str,  # Treat as string to retain exact formatting
    "Key Skills": str,  # Will be stored as a single string
    "Gen AI Experience Score": int,
    "AI/ML Experience Score": int,
    "supporting_info": str,
}