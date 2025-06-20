import random
import pandas as pd
high_conf_sensitive = [
    "The password is: {}",
    "OTP is {}",
    "My phone number is {}",
    "My Aadhaar number is {}",
    "Bank account number is {}",
    "Here is my PIN: {}",
    "My email is {}",
    "Credit card number: {}",
    "My full name is {}",
    "My username is {}, and password is {}"
]
medium_conf_sensitive = [
    "I am revealing my password",
    "Should I tell you my pin?",
    "Do you need my personal details?",
    "Should I give my contact info?",
    "Want my phone number?",
    "I might share my secret code",
    "Thinking of entering password",
    "Maybe I’ll give the OTP",
    "Need to enter my PIN",
    "Should I write down the code?"
]

low_conf_ambiguous = [
    "I need a token of love",
    "He lost the key",
    "She shared the code",
    "That number is lucky",
    "I am sending a signal",
    "It’s a key moment",
    "Token system is useful",
    "He mentioned something secret",
    "Code is a puzzle",
    "The number is big"
]

low_conf_general = [
    "Hi",
    "Hello",
    "Good morning",
    "How are you?",
    "Nice to meet you",
    "Hope you're fine",
    "Is it raining?",
    "Let's talk",
    "What’s up?",
    "Good evening"
]


def get_random_digit_string(length=6):
    return ''.join(random.choices('0123456789', k=length))

def get_random_email():
    return f"user{random.randint(100,999)}@example.com"

def get_random_name():
    names = ["John Doe", "Priya Singh", "Amit Kumar", "Sarah Ali", "Dev Patel"]
    return random.choice(names)


def generate_query_list():
    queries = []


    for _ in range(70):
        for template in high_conf_sensitive:
            if '{}' in template and template.count('{}') == 2:
                q = template.format(get_random_digit_string(), get_random_digit_string())
            elif "email" in template:
                q = template.format(get_random_email())
            elif "full name" in template:
                q = template.format(get_random_name())
            else:
                q = template.format(get_random_digit_string())
            queries.append(q)


    for _ in range(50):
        queries.extend(medium_conf_sensitive)


    for _ in range(40):
        queries.extend(low_conf_ambiguous)

    for _ in range(40):
        queries.extend(low_conf_general)

    random.shuffle(queries)
    return queries[:2000]


query_samples = generate_query_list()

df = pd.DataFrame({"query": query_samples})
file_path = "generated_sensitive_query_dataset.csv"
df.to_csv(file_path, index=False)

print(f"Dataset saved to: {file_path}")

