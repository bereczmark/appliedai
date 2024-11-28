from functions import *

if __name__ == "__main__":
    client = initialize_openai_client()
    session_manager = ChatGPTSessionManager(client)

    # Step 1: Load the primary Python code
    code_snippets = []
    while True:
        file_path = input("Enter the path to the Python code file (or type 'done' to finish): ").strip()
        if file_path.lower() == "done":
            break
        try:
            code_snippet = read_python_code(file_path)
            code_snippets.append(code_snippet)
            print(f"Successfully loaded: {file_path}")
        except Exception as e:
            print(f"Error: {e}")

    if not code_snippets:
        print("No files were loaded. Exiting.")
        exit(1)

    # Step 2: Select language for documentation
    language = input("Select documentation language ('en' for English, 'hu' for Hungarian): ").strip().lower()
    if language not in ["en", "hu"]:
        print("Invalid language selection. Defaulting to English.")
        language = "en"

    # Step 3: Select documentation style
    style = input("Select documentation style ('descriptive' or 'personal'): ").strip().lower()
    if style not in ["descriptive", "personal"]:
        print("Invalid style selection. Defaulting to 'descriptive'.")
        style = "descriptive"

    # Step 4: Generate documentation in English with GPT-3.5 Turbo
    print("\nGenerating documentation in English...\n")
    try:
        documentation = generate_documentation(client, code_snippets, style)
        print("\nDocumentation:\n")
        print(documentation)
    except Exception as e:
        print(f"Error generating documentation: {e}")
        exit(1)

    # Step 5: Translate to Hungarian if needed
    if language == "hu":
        print("\nTranslating documentation to Hungarian...\n")
        try:
            documentation = translate_to_hungarian(client, documentation)
            print("\nTranslated Documentation:\n")
            print(documentation)
        except Exception as e:
            print(f"Error translating documentation: {e}")
            exit(1)

    # Step 6: Save the documentation to Word
    if input("\nDo you want to save the documentation in Word format? (yes/no): ").strip().lower() == "yes":
        output_file = input("Enter the name of the Word file (e.g., documentation.docx): ").strip()
        if not output_file.endswith(".docx"):
            output_file += ".docx"
        save_markdown_to_word(documentation, output_file)
    else:
        print("\nDocumentation not saved.")
