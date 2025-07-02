import diary_elements
import existing_diaries

"""TODO:
- Add a separate folder to store diaries, rather than just one for diaries and existing lists.
- Add functionality to view all entries in a diary.
- Add functionality to search entries by tags.
- Add functionality to search entries by date.
- Add functionality to remove a diary.
    - Include a confirmation step before clearing.
    - Remove tags associated with the diary, unless they are in other diaries.
- Add functionality to remove all diaries.
    - Include a confirmation step before clearing.
- Add functionality to remove entries from a diary.
    - Include a confirmation step before removing an entry.
- Add functionality to alter a diary entry.
    - Edit content and tags.
- Add functionality to store epoch time for each entry.
- Add functionality to export diary entries to a text file.
    - Add functionality to import diary entries from a text file.
"""

def main():
    """Main function to run the diary application."""
    buffer = "-------------------------"

    print(buffer)
    print("Welcome to the Diary Application!")
    print(buffer)

    
    while True:
        print("What would you like to do?")
        print(buffer)
        print("1: Add a new diary or diary entry")
        print("2: View all diary entries")
        print(buffer)
        print("(To exit at any time, enter '-')")
        choice = input("Enter your choice (1-2): ")
        print(buffer)
        
        match choice:
            case '1':
                print("Existing diaries:")
                print(existing_diaries.print_formatted())
                print(buffer)

                diary_name = input("Enter the name of the diary you would like to create or add an entry to: ")
                if diary_name == '-':
                    print(buffer)
                    print("Exiting the diary application.")
                    print(buffer)
                    break

                existing_diaries.add(diary_name) # Won't add if it already exists
                diary = diary_elements.Diary(diary_name)

                content = input("Enter the content of your diary entry: ")
                if content == '-':
                    print(buffer)
                    print("Exiting the diary application.")
                    print(buffer)
                    break

                tags_input = input("Enter tags (separated by \", \"): ")
                if tags_input == '-':
                    print(buffer)
                    print("Exiting the diary application.")
                    print(buffer)
                    break

                tags = [tag for tag in tags_input.split(", ")] if tags_input else []
                entry = diary_elements.DiaryEntry(content, tags)
                diary.add_entry(entry)

                print(buffer)
                print(f"Diary entry added:\n{entry}")
                print(buffer)
            
            case '2':
                print("Existing diaries:")
                print(existing_diaries.print_formatted())
                print(buffer)

                diary_name = input("Enter the name of the diary you would like to view: ")
                if diary_name == '-':
                    print(buffer)
                    print("Exiting the diary application.")
                    print(buffer)
                    break

                if not existing_diaries.contains(diary_name):
                    print(buffer)
                    print(f"Diary '{diary_name}' does not exist. Please create it by adding a first entry.")
                    continue

                diary = diary_elements.Diary(diary_name)

                print(diary)
            
            case '-':
                print("Exiting the diary application.")
                print(buffer)
                break
            
            case _:
                print("Invalid choice. Please try again.")
                print(buffer)

if __name__ == "__main__":
    main()