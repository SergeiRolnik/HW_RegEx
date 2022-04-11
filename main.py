import re
import csv

# open csv file and read contact list
with open('phonebook_raw.csv', encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=',')
  contact_list = list(rows)

new_contact_list = []
for line in contact_list:

  # names processing
  if re.search(r'\w+\s\w+\s\w+', line[0]) != None: # check for pattern (last_name + first_name + surname)
    full_name = re.split(r'\s', line[0])
    line[2] = full_name[2]
    line[1] = full_name[1]
    line[0] = full_name[0]
  elif re.search(r'\w+\s\w+', line[1]) != None: #  check for pattern (last_name, first_name + surname)
    first_name_and_surname = re.split(r'\s', line[1])
    line[2] = first_name_and_surname[1]
    line[1] = first_name_and_surname[0]
  elif re.search(r'\w+\s\w+', line[0]) != None: #  check for pattern (last_name + first_name, surname)
    last_name_first_name = re.split(r'\s', line[0])
    line[1] = last_name_first_name[1]
    line[0] = last_name_first_name[0]

  # phone numbers processing
  old_pattern = r'\+?([7|8])\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*)\(?(\s*доб.)?\s*(\d+)?\)?'
  new_pattern = r'+7(\2)\3-\4-\5\6\7\8'
  line[5] = re.sub(old_pattern, new_pattern, line[5])
  new_contact_list.append(line)

# check for duplicate records
lines_to_delete = []
i = 1
for line1 in new_contact_list[1:len(new_contact_list) - 1]:
  for line2 in new_contact_list[i + 1:len(new_contact_list)]:
    if line1[0] == line2[0] and line1[1] == line2[1]: #check if first_name and last_name are the same
      for k in range(len(line1)):
        if line1[k] == '':
          line1[k] = line2[k]
      lines_to_delete.append(new_contact_list.index(line2))
  i += 1

# delete duplicate records
lines_to_delete.sort(reverse=True)
for line_number in lines_to_delete:
  new_contact_list.pop(line_number)

# print updated contact list
print('-------- UPDATED CONTACT LIST ---------')
for line in new_contact_list:
  print(line)

# writing updated list to file
with open('phonebook.csv', 'w', encoding='utf-8', newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_contact_list)