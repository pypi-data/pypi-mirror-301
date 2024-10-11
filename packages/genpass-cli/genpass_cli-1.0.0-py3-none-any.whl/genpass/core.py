import string
import random
import argparse
import pyperclip

def generate_password(length=12, use_special=True, use_numbers=True, use_uppercase=True):
    """Generate a secure password with specified requirements."""
    
    chars = string.ascii_lowercase
    
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = []
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # randomize rest of the password
    remaining_length = length - len(password)
    password.extend(random.choice(chars) for _ in range(remaining_length))
    
    # shuffle the password
    random.shuffle(password)
    return ''.join(password)

def main():
    parser = argparse.ArgumentParser(
        description='Generate secure passwords with custom requirements'
    )
    parser.add_argument(
        '-l', '--length', 
        type=int, 
        default=12,
        help='Password length (default: 12)'
    )
    parser.add_argument(
        '--no-special',
        action='store_false',
        dest='special',
        help='Exclude special characters'
    )
    parser.add_argument(
        '--no-numbers',
        action='store_false',
        dest='numbers',
        help='Exclude numbers'
    )
    parser.add_argument(
        '--no-uppercase',
        action='store_false',
        dest='uppercase',
        help='Exclude uppercase letters'
    )
    parser.add_argument(
        '-c', '--copy',
        action='store_true',
        help='Copy password to clipboard'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Only output the password (useful for scripts)'
    )
    
    args = parser.parse_args()
    
    password = generate_password(
        args.length,
        args.special,
        args.numbers,
        args.uppercase
    )
    
    if args.copy:
        pyperclip.copy(password)
        
    if args.quiet:
        print(password)
    else:
        print(f"\nGenerated password: {password}")
        if args.copy:
            print("Password copied to clipboard!")
        print(f"\nLength: {len(password)} characters")
        print("Contains:")
        print(f"  - Uppercase letters: {'Yes' if args.uppercase else 'No'}")
        print(f"  - Numbers: {'Yes' if args.numbers else 'No'}")
        print(f"  - Special characters: {'Yes' if args.special else 'No'}")

if __name__ == "__main__":
    main()
