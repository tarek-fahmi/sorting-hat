import csv
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np


class Student:
    '''
    This class is to represent a student. A student must have a name, SID and preferred study times and modes.
    '''
    def __init__(self, name, sid, preferred_time, preferred_mode):
        self.name = name
        self.sid = sid
        self.preferred_time = preferred_time
        self.preferred_mode = preferred_mode

def collect_preferences(file_path):
    '''
    This function collects the relevant data from the .csv file provided by the user. This function anticipates
    that the file is of the type of a canvas quiz download, containing the student's name, SID and quiz answers 
    in certain columns. 
    MODIFY THIS FUNCTION IF THE CANVAS QUIZ QUESTIONS CHANGE. 
    Input: file path to the .csv file. 
    Output: list of students with their name, SID, preferred times and preferred modes. 
    '''
    students = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            # Check if the row has at least 15 columns - this is the format for Canvas quiz downloads. 
            if len(row) < 15: 
                    return None
            # Unpack data from row 
            name, _, sid, _, _, _, _, _, preferred_times_answer, _, preferred_mode, _, _, _, _ = row  
            # Unpack preferred times to a list
            preferred_time = preferred_times_answer.split(",")
            students.append(Student(name, sid, preferred_time, preferred_mode))

    return students


def form_groups(students, group_size):
    ''' 
    This function is where the sorting happens. It firstly determines how many groups can be in the desired 
    size (i.e. if the total number of students divided by the desired group size contains remainders) - note 
    that the program opts down, so if the user enters 5 for group size then the range of group size is 4-5. 
    GThe function then sorts students according to their preferred time of the day and then sorts students based on their 
    preffered mode of meeting. Finally it groups the students according to this sorting. 
    Input: list of students, integer of desired group size.
    Output: list of groups, list of dominating preferences for each group.
    '''
    groups = []
    group_preferences = []  # This will store the dominant preference for each group
    
     # Determine the actual size of each group and the optimal number of groups
    total_students = len(students)
    num_full_groups = total_students // group_size
    remainder = total_students % group_size
    
    # if there exists a remainder smaller than 1-less of the desired group size, check how many groups need to
    # contain a smaller size to meet the amount of total students.
    if 0 < remainder < group_size-1:
        adj_group_size = group_size-1
        num_smaller_groups = total_students // adj_group_size
        remainder = total_students % adj_group_size
        if 0 < remainder < adj_group_size-1:
            num_full_groups = remainder
            num_smaller_groups = num_smaller_groups - remainder
    else:
        if remainder == 0:
            adj_group_size = group_size     

    # Sort students by preferred time and then by preferred mode
    sorted_students = sorted(students, key=lambda s: (s.preferred_time, s.preferred_mode))

    # Group students according to desired group size
    current_group = []
    current_group_preferences = {'times': {}, 'modes': {}}
    
    group_size_counter = 0
    
    for student in sorted_students:
        current_group.append(student)
        
        
        # Count preferences for the current group
        for time in student.preferred_time:
            current_group_preferences['times'][time] = current_group_preferences['times'].get(time, 0) + 1
        current_group_preferences['modes'][student.preferred_mode] = current_group_preferences['modes'].get(student.preferred_mode, 0) + 1

        # switch group size to the smaller alternative if required.
        if group_size_counter == num_full_groups:
            if len(current_group) == adj_group_size:
                groups.append(current_group)
                
                # Identify dominant preferences for the group
                dominant_time = max(current_group_preferences['times'], key=current_group_preferences['times'].get)
                dominant_mode = max(current_group_preferences['modes'], key=current_group_preferences['modes'].get)
                group_preferences.append((dominant_time, dominant_mode))
                # Reset for the next group
                current_group = []
                current_group_preferences = {'times': {}, 'modes': {}}
        
        # if the current group has reached the desired size, add it to the list of groups. 
        if len(current_group) == group_size:
            groups.append(current_group)
            group_size_counter += 1
            
            # Identify dominant preferences for the group
            dominant_time = max(current_group_preferences['times'], key=current_group_preferences['times'].get)
            dominant_mode = max(current_group_preferences['modes'], key=current_group_preferences['modes'].get)
            group_preferences.append((dominant_time, dominant_mode))
            # Reset for the next group
            current_group = []
            current_group_preferences = {'times': {}, 'modes': {}}
        
    return groups, group_preferences

def write_groups_to_csv(groups, output_file_path):
    '''
    This function writes the groups to a .csv file. It uses the students' names but can be easily modified to
    use their SIDs.
    Input: list of groups, file path for output. 
    Output: None
    '''
    with open(output_file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for i, group in enumerate(groups):
            group_data = [f"Group {i+1}"] + [student.name for student in group]
            csv_writer.writerow(group_data)
    
def main(root):
    '''
    There is no GUI window, but there are dialog boxes that pop up on the user's screen to instruct them and 
    communicate what is happening. 
    '''
    
    file_path = filedialog.askopenfilename(title="Select CSV file with student preferences")
    if not file_path:
        return

    group_size = simpledialog.askinteger("Input", "Please enter the desired size of each group:",
                                         parent=root, minvalue=2, maxvalue=15)
    if not group_size:
        return

    students = collect_preferences(file_path)
    if students is None:
        messagebox.showerror("File Error", "Failed to parse the file. Please check the file format and retry.")
        return
    groups, _ = form_groups(students, group_size)

    output_file_path = filedialog.asksaveasfilename(title="Save the output CSV file", defaultextension=".csv")
    if not output_file_path:
        return

    write_groups_to_csv(groups, output_file_path)
    messagebox.showinfo("Success", f"Groups have been written to {output_file_path}\nThank you for using the Sorting Hat!")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    messagebox.showinfo("Welcome", "Welcome to the Sorting Hat Program. \nPlease select the CSV file with student preferences.")
    main(root)
