
A small lightweight language that combines Python and HTML.
Recommended file extension: .γ/.gmaj

Example syntax:
```GammaJ
<!DOCTYPE html>

# comment
x: int = 123 # variable
def xyz() -> None:
    ... # ellipsis (ignores the line)
    
def main() -> None:
    # to insert html, use the 'export gamma' statement along with 'html' opening and closing tags as shown below
    export gamma <html>
        <!-- html code here -->
        <h1>
            Hello, world!
        </h1> <!-- this will open your browser to a random unused port with a 'Hello, world' heading -->
    </html>
    
    # after the closing 'html' tag, you can continue with python code
    # to export for ex. a python variable, which is not possible with 'export gamma',
    # you can use plain 'export' instead:
    name: str = "Bob"
    export paragraph("Hello,", name) # creates a paragraph with text: 'Hello, Bob'
    export heading1("Heading 1") # \
    export heading2("Heading 2") # |
    export heading3("Heading 3") #  > headings
    export heading4("Heading 4") # |
    export heading1("Heading 1") # /
    export print("Unformatted", "text") # creates plain text
    export weblink("https://google.com", "Google") # creates a hyperlink. param 1 is href
    export image("cat.png", "A picture of a munchkin cat") # creates an image. param 1 is src, param 2 is alt
    export list("item 1", "item 2", "item3") # creates an unordered list. cannot be created with brackets [] (e.g. export ["1", "2"]) like non-exported lists
    export table("item 1", "item 2", "item") # creates a table
    
if __name__ == '__main__': # runs only when the file is executed directly
    main() # executes the main function
```

DISCLAIMER: The

DISCLAIMER: You cannot import GammaJ files in Python files or from other GammaJ files.
            You _can_ import Python from GammaJ files though.

## Running a GammaJ file
### Method 1: Use cmdlet (recommended)
```commandline
gammaj <filename>
```
### Method 2: Run using python module
```commandline
python -m gammaj <filename>
```

## How to get Syntax Highlighting (new in v4)
- Disclaimer: Right now, syntax highlighting is only available for PyCharm (all editions including the free community edition)
- Download GammaJ.xml [here](https://github.com/elemenom/gammaj/blob/main/GammaJ.xml)
- Click 'Download raw file'
- Move the downloaded file (usually in C:/Users/<USERNAME>/Downloads) to your PyCharm 'filetypes' directory (usually C:/Users/<USERNAME>/AppData/Roaming/JetBrains/PyCharm<VERSION>/filetypes)
- Restart PyCharm (if needed)
- Voilà! You now have colour in your GammaJ file.