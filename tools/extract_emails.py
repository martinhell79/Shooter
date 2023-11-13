# Function to extract and collect unique emails from a list of files
def extract_unique_emails(file_names):
    unique_emails = set()  # Use a set to store unique emails

    for file_name in file_names:
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.strip().split('\ ')
                if len(parts) >= 3:  # Ensure there are at least 3 parts (points, name, email)
                    email = parts[2].strip()
                    unique_emails.add(email)
    unique_emails.remove('Anonymous')
    return list(unique_emails)

# Function to write unique emails to a new file with a specified separator
def write_unique_emails_to_file(unique_emails, output_file, separator):
    with open(output_file, 'w') as file:
        for email in unique_emails:
            file.write(email + separator)

if __name__ == "__main__":
    # Specify the list of input file names and the output file name
    input_files = ['highscores-day1.txt', 'highscores-day2.txt', 'highscores-day3.txt']  # Add your file names here
    output_file = 'unique_emails.txt'  # Change to your desired output file name

    # Specify the separator used in the output file
    output_separator = ';'  # Change to your desired separator (e.g., '\n' for new line)

    # Extract and collect unique emails
    unique_emails = extract_unique_emails(input_files)

    # Write unique emails to the output file with the specified separator
    write_unique_emails_to_file(unique_emails, output_file, output_separator)

    print(f"Unique emails written to '{output_file}' with separator '{output_separator}'. (There are {len(unique_emails)} emails)")
