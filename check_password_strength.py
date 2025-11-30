import string

def check_password_strength(password: str) -> bool:
    # Criteria flags
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    
    # Check minimum length
    if len(password) < 8:
        return False

    # Iterate through each character
    for char in password:
        if char.isupper():
            has_upper = True
        if char.islower():
            has_lower = True
        if char.isdigit():
            has_digit = True
        if char in string.punctuation:  # checks special characters
            has_special = True

    # Return True only if ALL criteria are satisfied
    return has_upper and has_lower and has_digit and has_special


# ---- Main script ----

password = input("Enter your password: ")

if check_password_strength(password):
    print("✅ Password is strong!")
else:
    print("❌ Weak password! It must contain:")
    print("- At least 8 characters")
    print("- Uppercase and lowercase letters")
    print("- At least one digit (0-9)")
    print("- At least one special character (!@#$ etc.)")