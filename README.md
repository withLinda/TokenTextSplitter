
# Token Text Splitter

The application allows you to open a text file, split the text into chunks based on a specified maximum number of tokens, and copy the text to the clipboard. This is a simple GUI application built with Python's `tkinter` library. 

## Features

- Open a text file and display its content in the GUI.
- Split the text into chunks based on a specified maximum number of tokens.
- Copy the selected text to the clipboard.

## Classes

- `TextProcessor`: This class contains a static method `split_text_into_chunks` that splits a given text into chunks based on a specified maximum number of tokens.
- `TextFileReader`: This class inherits from `tk.Tk` and represents the main application window. It contains methods for opening a file, splitting the text, and copying the text to the clipboard.

## Usage

To run the application, simply execute the script `Split-text-app.py`. The GUI will appear and you can interact with it.

- Click the "Open File" button to open a text file.
- Enter a number in the "Max Tokens" field and click "Save Max Tokens" to set the maximum number of tokens for each chunk.
- The text from the file will be displayed in the GUI, split into chunks based on the maximum number of tokens.
- Click the "Select and Copy Text" button to copy the text to the clipboard.

## Dependencies

- Python 3
- tkinter
- customtkinter
- pyperclip
- re
- os

## Note

This application uses the `customtkinter` library for custom tkinter widgets. Make sure to install this library before running the application. 


<img src="https://github.com/withLinda/TokenTextSplitter/assets/82918531/15c19828-1595-459f-8b1e-e9551db2f040" width="400" height="1000"> 


