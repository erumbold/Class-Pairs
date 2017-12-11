from csv import reader, writer
from random import randint
from shutil import move
'''
This program creates pairs of students for in-class exercises
Author: Erika Rumbold
Last Modified: November 7, 2017
'''

def write_new_class(filename):
    '''
    creates CSV file with student names and their table number
    Args: filename
    Returns: None
    '''
    print("creating class...\n")
    print("Enter student names and table numbers (i.e. Bob 3)")
    print("Press ENTER when done")
    entries = list()
    entry = input()
    while entry != "":
        test = entry.split(" ")
        try:
            test_table = int(test[1])
            entries.append(entry.replace(" ", ","))
        except ValueError:
            print("Re-enter")
        entry = input()

    with open(filename, 'w') as f:
        for line in entries:
            f.write(line+"\n")

def load_class(filename):
    '''
    creates a list of student information from a CSV file
    Args: filename
    Returns: class_list
    '''
    print("loading class file...\n")
    class_list = list()
    file = open(filename, 'r')
    r = reader(file)
    for row in r:
        class_list.append(row)
    file.close()
    return class_list

def absent(class_list):
    '''
    creates a list of student info from class_list without absent student info
    Args: class_list
    Returns: present_list
    '''

    print("Enter absent students' names")
    print("Press ENTER when done")
    present_list = class_list[:]
    entry = input()
    while entry != "":
        for student in present_list:
            if entry in student:
                present_list.remove(student)
                break
        entry = input()
    return present_list

def make_pairs(students):
    '''
    randomly pairs students
    Args: students
    Returns: pairs
    '''
    pairs = dict()
    tries = 0
    while len(students) > 3:
        s1 = randint(1,len(students)-1)
        s2 = randint(1,len(students)-1)
        if not check_pair(students[s1], students[s2]) or tries > len(students):
            pairs[students[s1][0]] = students[s2][0]
            del students[s1]
            if s2 > s1:
                del students[s2-1]
            else:
                del students[s2]
            tries = 0
        else:
            tries += 1
    if len(students) == 3 or len(students) == 2:
        pairs[students[0][0]] = students[1][0]
        del students[0]
        del students[0]
    if len(students) == 1:
        pairs[students[0][0]] = "YOU PICK"
        del students[0]
    return pairs

def check_pair(s1, s2):
    '''
    checks if students have worked together already
    Args: s1, s2
    Returns: True if have worked together or sit at the same table; False otherwise
    '''
    if (s1[0] in s2 and s2[0] in s1) or s1[1] == s2[1]:
        return True
    else:
        return False

def log_pair(filename, s1, s2):
    '''
    updates CSV file with new pair
    Args: filename, s1, s2
    Returns: None
    '''
    f = open(filename)
    r = reader(f)
    for row in r:
        if row[0] == s1:
            row.append(s2)
        elif row[0] == s2:
            row.append(s1)

    with open(filename, 'r') as fin:
        with open("new.csv", 'w') as fout:
            w = writer(fout, lineterminator="\n")
            r = reader(fin)
            all_rows = list()
            for row in r:
                if row[0] == s1:
                    row.append(s2)
                elif row[0] == s2:
                    row.append(s1)
                all_rows.append(row)
            w.writerows(all_rows)
    move("new.csv", filename)

def reset_file(filename):
    '''
    clears file of all partner data
    Args: filename
    Returns: None
    '''
    with open(filename, 'r') as fi:
        r = reader(filename)
        with open("new.csv", 'w') as fo:
            w = writer("new.csv")
            for row in r:
                w.writerow((row[0], row[1]))
    move("new.csv", filename)

def need_reset(class_list):
    '''
    checks list of student info to see if all pairings have been met
    Args: class_list
    Returns: True if file needs to be reset; False otherwise
    '''
    tally = list()
    for row in class_list:
        count = 0
        for col in row:
            if col != "ABSENT" and col != "YOU PICK":
                count += 1
        tally.append(count)
    count = 0
    for i in tally:
        if i > len(class_list) * 0.75:
            count += 1
    if count > 0.75 * len(class_list):
        return True
    else:
        return False

def selection(message):
    '''
    provides options to user and processses user input
    Args: message
    Returns: selection
    '''
    ui = 0
    while ui < 1 or ui > 2:
        ui = input(message)
        try:
            ui = int(ui)
        except ValueError:
            ui = 0
    return ui

def print_pairs(pairs):
    '''
    prints pairs in readable formatting
    Args: pairs
    Returns: None
    '''
    for s1 in pairs:
        if len(s1) < 8:
            spacing = "\t\t"
        else:
            spacing = "\t"
        print(s1+spacing+pairs[s1])

def main():
    ui = selection("1) existing class or 2) new class ")
    filename = input("Enter CSV filename: ")
    while ".csv" not in filename:
        filename = input("Enter CSV filename: ")
    if ui == 2:
        write_new_class(filename)
    class_list = load_class(filename)

    if need_reset(class_list):
        reset_file(filename)
        class_list = load_class(filename)
    present_list = absent(class_list)
    
    rolling = True
    while rolling:
        pairs = make_pairs(present_list[:])
        print_pairs(pairs)

        roll = selection("1) keep or 2) reroll ")
        if roll == 1:
            rolling = False

    here = list()
    for s1 in pairs:
        log_pair(filename, s1, pairs[s1])
        here.append(s1)
        if pairs[s1] != "YOU PICK":
            here.append(pairs[s1])
    for i in class_list:
        if i[0] not in here:
            log_pair(filename, i[0], "ABSENT")
    
    
main()
