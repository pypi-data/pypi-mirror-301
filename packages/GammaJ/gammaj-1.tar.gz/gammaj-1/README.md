
A small lightweight language that combines Python and HTML.
Recommended file extension: .γ/.gmaj

Example syntax:
```GammaJ
# comment
x: int = 123 # variable
def xyz() -> None:
    ... # ellipsis (ignores the line)
    
def main() -> None:
    # to insert html, use the 'html' opening and closing tags as shown below
    <html>
        <!-- html code here -->
        <h1>
            Hello, world!
        </h1> <!-- this will open your browser to a random unused port with a 'Hello, world' heading -->
    </html>
    
    # after the closing 'html' tag, you can continue with python code
    
if __name__ == '__main__': # runs only when the file is executed directly
    main() # executes the main function
```

DISCLAIMER: You cannot import GammaJ files in Python files or from other GammaJ files.
            You _can_ import Python from GammaJ files though.

## Running a GammaJ file:
### Method 1: Use -g parameter
```commandline
python -m -g <filename>
```
### Method 2: Use cmdlet
```commandline
gammaj <filename>
```