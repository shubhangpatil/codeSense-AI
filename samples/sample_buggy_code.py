def get_user(name, users=[]):
    users.append(name)
    return users


def calculate_average(numbers):
    return sum(numbers) / len(numbers)


def run_query(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query
