# Python Password Manager Library

This is a Python library that generates random passwords with a specified length, complexity, and character set. Also gives a score of given password.

## Usage

```bash
from password_manager import generate_password , password_strength # Import the library

password = generate_password(length=12, use_letters=True, use_digits=False, use_symbols=False, exclude_chars="a") # Generate a password
print(password) # Print the password

print(password_strength("Emr")) # Check the password strength. Result is like: 3 / 10
```