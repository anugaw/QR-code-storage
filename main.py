from file_to_binary import start
from video_to_qr import videostart

def convert_file_to_binary():
    filename = input("Enter the filename to convert to binary: ")
    start(filename)

def convert_video_to_qr():
    name = input("Enter the video filename to convert to QR code: ")
    videostart(name)

def main():
    print("Welcome to the File and Video Converter!")

    while True:
        print("\nChoose an option:")
        print("1. Convert file to video")
        print("2. Convert video to file")
        print("3. Exit")

        choice = input("Enter the corresponding number: ")

        if choice == '1':
            convert_file_to_binary()
        elif choice == '2':
            convert_video_to_qr()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
