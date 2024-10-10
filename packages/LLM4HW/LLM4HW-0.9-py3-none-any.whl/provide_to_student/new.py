import fnmatch
from openai import OpenAI
import sys
import re
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import font as tkfont
from tkinter import Toplevel, Label, Button, Frame, Entry, messagebox, Scrollbar
import threading
# from tkhtmlview import HTMLLabel

from tkinter import Toplevel, Label, Button, Frame, Entry, OptionMenu, StringVar
import requests
import uuid
import socket
from urllib.parse import urlparse

# Global variable to maintain code block state across function calls
in_code_block = False
user_choice = "123"

# Load environment variables from the .env file
load_dotenv()

# Get the value of the environment variable
account_record = os.getenv('LLM4HW_ACCOUNT')

uuid_check = ""

# Constants
directory_path = r'D:\chip chat\new_structure'

def fetch_response(dialog, response_data):
    """ Function to fetch the response from the server and display it in the dialog window."""
    try:
        content = response_data
        dialog.response_text.configure(state='normal')
        dialog.response_text.insert(tk.END, "AI: ", "question") # Insert the AI label

        insert_content_word_by_word(dialog, content)
    except requests.RequestException as e:
        messagebox.showerror("Network Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))


def insert_content_word_by_word(dialog, content, word_list=None, index=0):
    """ Function to insert the content word by word into the dialog window."""
    global in_code_block
    if word_list is None:
        word_list = content.split()  # Split content into words preserving whitespace and code indicators.

    if index < len(word_list):
        current_word = word_list[index]
        # Keywords that should trigger a new paragraph
        keywords = ["In", "As", "When", "However", "Therefore", "To", "For"]
        if current_word in keywords:
            current_word = current_word.replace(current_word, "\n\n" + current_word)

        # Check if the current word contains triple backticks indicating a switch
        elif '``' in current_word:
            in_code_block = not in_code_block  # Toggle the in_code_block state
            current_word = current_word.replace('```', '\n').replace('``', '').replace(' `', '').replace('` ', '')
        dialog.response_text.configure(state='normal')

        # Apply font based on the current state
        if in_code_block:
            keywords = [";"]
            for keyword in keywords:
                if keyword in current_word:
                    current_word = current_word.replace(current_word, current_word + "\n")
            # Ensure the 'code' tag is configured for monospace font
            dialog.response_text.tag_configure("code", font=('Courier New', 10, 'bold'))
            dialog.response_text.insert(tk.END, current_word + ' ', "code")
        else:
            dialog.response_text.insert(tk.END, current_word + ' ', "response")

        dialog.response_text.configure(state='disabled')
        dialog.response_text.see(tk.END)  # Scroll to the end

        # Recursively call itself with the new index and the current state of in_code_block
        dialog.after(200, insert_content_word_by_word, dialog, content, word_list, index + 1)


def on_closing(root, dialog):
    """ Function to handle the closing of the dialog window. """
    help = messagebox.askyesnocancel("Quit", "Thanks for trying the tool\nWas the generated answer helpful?\n(Cancel to abort quit)")
    send_finish(help)
    dialog.destroy()
    root.quit()
    root.destroy()


def create_dialog(root, error_line, error_code, error_message):
    """
    Function to create the dialog window for displaying the response and asking follow-up question
    """
    # Create the dialog
    dialog = Toplevel(root)
    dialog.title("LLM Generated Response")
    dialog.geometry("700x500") # Set the size of the dialog window

    # Center the dialog
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    dialog.deiconify()  # Show the dialog

    # Intercept the close button
    dialog.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, dialog))

    bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
    normal_font = tkfont.Font(family="Helvetica", size=10)
    # change difference between question and response
    question_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
    response_font = tkfont.Font(family="Courier", size=10)  # Different style for responses

    warning_label = Label(dialog, text="WARNING: AI GENERATED RESPONSE FOLLOWS", font=bold_font)
    warning_label.pack(pady=(10, 2), padx=10, fill=tk.X)

    response_frame = Frame(dialog)
    response_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)

    response_text = tk.Text(response_frame, font=normal_font, wrap='word', height=15, width=50)
    response_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure tags
    response_text.tag_configure("question", font=question_font)
    response_text.tag_configure("response", font=normal_font)

    # Initial text insertions
    response_text.configure(state='normal')
    response_text.insert(tk.END, "User: ", "question")
    response_text.insert(tk.END, "Can you help with my compilation error?", "response")
    response_text.insert(tk.END, '\n----------------------------------------------------------------------\n\n', "response")
    response_text.configure(state='disabled')


    scrollbar = tk.Scrollbar(response_frame, command=response_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    response_text.configure(yscrollcommand=scrollbar.set, state='disabled')
    # response_text.insert(tk.END, dialog.response_text)
    dialog.response_text = response_text  # Assign the text widget to a property of dialog for easy access

    # Middle Frame for follow-up question
    middle_frame = Frame(dialog)
    middle_frame.pack(pady=(10, 0), padx=10, fill=tk.X)
    
    follow_up_label = Label(middle_frame, text="Ask follow up question:", font=("Arial", 16))
    follow_up_label.pack(side=tk.LEFT, padx=10)
    
    follow_up_entry = Entry(middle_frame, font=("Arial", 14), width=30)
    follow_up_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
    
    send_button = Button(middle_frame, text="Send", command=lambda: send_message(dialog, follow_up_entry, error_message, error_line, error_code, dialog))
    send_button.pack(side=tk.LEFT, padx=10, anchor='w')
    dialog.update_idletasks()
    dialog.deiconify()  # Show the dialog

    return dialog


def send_message(root, follow_up_entry, error_message, error_line, error_code, dialog):
    """
    Function to send the follow-up question to the server and display the response.
    """
    # Get the follow-up question from the entry widget
    follow_up_question = follow_up_entry.get()
    follow_up_entry.delete(0, tk.END)  # Clear the entry widget

    # Process the follow-up question
    if follow_up_question:
        dialog.response_text.configure(state='normal')
        dialog.response_text.insert(tk.END, '\n\n----------------------------------------------------------------------\n', "response")
        dialog.response_text.insert(tk.END, "User: ", "question")  # Display the question
        dialog.response_text.insert(tk.END, follow_up_question, "response")  # Display the question
        dialog.response_text.insert(tk.END, '\n----------------------------------------------------------------------\n\n', "response")
        dialog.response_text.configure(state='disabled')
        response = send_response(error_message, error_line, error_code, follow_up_question)
        thread = threading.Thread(target=fetch_response, args=(root, response[0]))
        thread.start()
    else:
        messagebox.showinfo("Info", "Please enter a follow-up question.")


def find_errors_in_files(directory_path):
    # This should be expanded to handle real error detection logic
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.startswith("ERROR:"):
                            return line
            except Exception as e:
                # print(f"Could not read file {file_path}: {e}")
                continue
    return None  # Return None if no error is found

def find_errors_code(error_message):
    pattern = r'\[([^\]]*?\.(?:vhd|vhdl|v)):(\d+)\]'
    match = re.search(pattern, error_message)
    if match:
        file_path, line_number = match.groups()
        line_number = int(line_number)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for current_line_number, line in enumerate(file, start=1):
                    if current_line_number == line_number:
                        return line.strip(), file.read()
        except Exception as e:
            print(f"Could not read file {file_path}: {e}")
    return None, None  # Handle the case where the pattern does not match

def is_server_open(url):
    """Check if the server is running by attempting to connect to the URL. timeout after 5 seconds."""
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)  # Timeout after 5 seconds
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error:
        return False
    finally:
        s.close()

def check_server():
    """Check if the server is running before proceeding with the conversation."""
    url = 'http://nash.cse.unsw.edu.au:24080/process'
    url1 = 'http://nash.cse.unsw.edu.au:24080/init'

    # check if url server is running
    if is_server_open(url):
        pass
    elif is_server_open(url1):
        pass
    else:
        # using raise
        raise Exception("Server is not running")


def main():
    """main function to run the program, create the GUI and start the conversation with the server."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window initially

    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    vhdl_files, verilog_files = find_hdl_files(directory_path)
    all_files = vhdl_files + verilog_files  # Combine both lists if you want all files in one string

    # Get combined content of all VHDL and Verilog files
    combined_content = concatenate_files(all_files)
    # Start a thread to process fetching response to avoid freezing the GUI
    error_message = find_errors_in_files(directory_path)
    if error_message:
        error_line, error_code = find_errors_code(error_message)
        if error_line and error_code:

            dialog = create_dialog(root, error_line, combined_content, error_message)
            # print(dialog)
            response = send_response(error_message, error_line, combined_content, "Can you help with my compilation error?")
            print(response)
            print(response[0])
            # Start the streaming response handling in a separate thread
            thread = threading.Thread(target=fetch_response, args=(dialog, response[0]), daemon=True)
            # thread = threading.Thread(target=fetch_response, args=(response_dialog, error_message, error_line, error_code))
            thread.start()
        else:
            # waiting_popup.destroy()
            messagebox.showerror("Error", "Failed to process error message or code.")
            root.destroy()
    else:
        # waiting_popup.destroy()
        messagebox.showerror("Error", "No errors found in the files.")
        root.destroy()
    
    ## check if connect to server - timeout in 5s
    try:
        check_server()
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Failed to connect to the server.")
        root.destroy()
    root.mainloop()

def find_hdl_files(directory_path):
    vhdl_files = []
    verilog_files = []
    for root, dirs, files in os.walk(directory_path):
        for filename in fnmatch.filter(files, '*.vhd'):
            vhdl_files.append(os.path.join(root, filename))
        for filename in fnmatch.filter(files, '*.v'):
            verilog_files.append(os.path.join(root, filename))
    return vhdl_files, verilog_files

def read_file(file_path):
    """Reads all content from a file and returns it."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"

def concatenate_files(file_paths):
    """Reads all files from the list, adding the filename before its content, and concatenates their content."""
    combined_content = ""
    for path in file_paths:
        file_content = read_file(path)
        header = f"--- File: {os.path.basename(path)} ---\n"  # Header to indicate the start of a new file
        combined_content += header + file_content + "\n\n"  # Append two newlines for clear separation
    return combined_content

def send_response(error_message, error_line, error_code, question):
    """
    Function to send the user's question to the server and receive a response (response, account, uuid).
    """
    url = 'http://nash.cse.unsw.edu.au:24080/init'
    global uuid_check
    if (uuid_check == ""):
        uuidNew = str(uuid.uuid4())
        uuid_check = uuidNew
    else:
        uuidNew = uuid_check
    infro = {
        'account': account_record,
        'uuid': uuidNew,
        'error_message': error_message,
        'error_line': error_line,
        'error_code': error_code,
        'question': question
    }

    response = requests.post(url, json=infro)


    if response.status_code == 200:
        response_data = response.json()
        response_detail = response_data.get('response', 'No response found')
        uuid_new = response_data.get('uuid', 'No UUID provided')
        return response_detail, uuid_new
    else:
        # Handle cases where the server might return an error
        return {"error": f"Failed to get response from server, status code {response.status_code}"}


def send_finish(helpful):
    """Send the helpfulness of the response to the server for logging"""
    url = 'http://nash.cse.unsw.edu.au:24080/process'

    infro = {
        'uuid': uuid_check,
        'helpful': helpful
    }

    helpful_sol = requests.post(url, json=infro)
    return helpful_sol


if __name__ == "__main__":
    main()
