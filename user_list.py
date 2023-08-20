admin_id = 5992320846


def user_scanning(message):
    if message.from_user.id == admin_id:
        file = open('users.txt').readlines()
        users = str(len(set(file)))
        return "Users: " + users
    else:
        return "no access"


def remove_duplicates_inplace(message, filename):
    if message.from_user.id != admin_id:
        return "no access"
    
    unique_lines = set()

    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines:
            cleaned_line = line.strip()
            if cleaned_line and cleaned_line not in unique_lines:
                unique_lines.add(cleaned_line)
                file.write(line)
