from functions import *

if __name__ == "__main__":
    client = initialize_openai_client()
    session_manager = ChatGPTSessionManager(client)

    # load Python code
    code_snippets = []
    print("\nYou can load multiple Python code files to generate documentation.")
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

    # select language for documentation
    language = input("Select documentation language ('en' for English, 'hu' for Hungarian): ").strip().lower()
    if language not in ["en", "hu"]:
        print("Invalid language selection. Defaulting to English.")
        language = "en"

    # select documentation style
    style = input("Select documentation style ('descriptive' or 'personal'): ").strip().lower()
    if style not in ["descriptive", "personal"]:
        print("Invalid style selection. Defaulting to 'descriptive'.")
        style = "descriptive"

    # add user-defined additional requests
    print("\nYou can add additional custom requests to guide the documentation generation.")
    print("For example: 'Explain how the code can be optimized for performance' or 'Include best practices for using this code'.")
    print("Enter 'done' when you are finished adding requests.")
    additional_requests = []
    while True:
        user = input("Type 'done' if no request, press enter to submit request: ").strip()
        if user.lower() == "done":
            break
        user_request = custom_input("Enter Addition(type 'END' to submit):")
        additional_requests.append(user_request)

    # generate documentation in english
    print("\nGenerating documentation in English...\n")
    try:
        documentation = generate_documentation(client, code_snippets, style, additional_requests)
        print("\nDocumentation:\n")
        print(documentation)
    except Exception as e:
        print(f"Error generating documentation: {e}")
        exit(1)

    # translate to hun
    if language == "hu":
        print("\nTranslating documentation to Hungarian...\n")
        try:
            documentation = translate_to_hungarian(session_manager, documentation)
            print("\nTranslated Documentation:\n")
            print(documentation)
        except Exception as e:
            print(f"Error translating documentation: {e}")
            exit(1)

    # save the documentation to Word
    if input("\nDo you want to save the documentation in Word format? (yes/no): ").strip().lower() == "yes":
        output_file = input("Enter the name of the Word file (e.g., documentation.docx): ").strip()
        if not output_file.endswith(".docx"):
            output_file += ".docx"
        save_markdown_to_word(documentation, output_file)
    else:
        print("\nDocumentation not saved.")
