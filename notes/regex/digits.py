import re

'''Numbers'''
# first as int
my_phone_number = "555-867-5309"

numbers = []
for char in my_phone_number:
    number_val = None
    try:
        number_val = int(char)
    except:
        pass
    if number_val != None:
        numbers.append(number_val)

numbers_as_str = "".join([f"{x}" for x in numbers])
# second as string
numbers_as_str2 = my_phone_number.replace("-", "")
# third
numbers_as_str3 = "".join([f"{x}" for x in my_phone_number if x.isdigit()])
# print(numbers_as_str3)

'''Regular Expressions'''
# Ex1
pattern = "\d"
# return list of digits. If add +, its group by digits
pattern = "\d+"
digits = re.findall(pattern, my_phone_number)
# Ex2
my_other_phone_numbers = "Hi there, my home number is 3123123asdfasdf3123 555-867-5309 and my cell number is +1-555-555-0007."

pattern = "\d+"
digits = re.findall(pattern, my_other_phone_numbers)
# Ex3
meeting_str = "Hey, give me a call at 8:30 on my cell at +1-555-555-0007."

pattern = "\d+"
digits = re.findall(pattern, meeting_str)
# Ex4
meeting_str = "Hey, give me a call at 8:30 on my cell at +1-555-555-0007 1-555-555-0007."

pattern = r"\+\d{1}-\d{3}-\d{3}-\d{4}" # "\n" \+ escaping +

digits = re.findall(pattern, meeting_str)

# ['+1-555-555-0007']
# \+ -> escape the + and use it in our pattern.

# \d -> matches all digits

# {1} -> {n} -> for n number, let's slice there.

# - -> is there a dash?

# Chunk 1 -> \+\d{1}-

# Chunk 2 -> \d{3}-

# Chunk 3 -> \d{3}-

# Chunk 4 => \d{4}

# Ex4
meeting_str = "Hey, give me a call at 8:30 on my cell at +1-555-555-0007 1-555-555-0007."

chunk_1 = r"\+\d{1}-" # "\n"

digits = re.findall(chunk_1, meeting_str)

# Ex5
chunk_1 = "\+?" + "\d{1}" + "-?"
chunk_2 = "\d{3}" + "-?"
chunk_3 = "\d{3}-?"
chunk_4 = "\d{4}"

pattern = f"{chunk_1}{chunk_2}{chunk_3}{chunk_4}"

meeting_str = "Hey, give me a call at 8:30 on my cell at +1-555-555-0007 1-555-555-0007 +15555553121."

regex = re.compile(pattern)
digits = re.findall(regex, meeting_str)
print(digits)