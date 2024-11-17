import csv
import io
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Student:
    '''
    Represents a student with a name, SID (Student ID), preferred study times, and preferred study modes.
    '''
    def __init__(self, name, sid, preferred_time, preferred_mode):
        self.name = name
        self.sid = sid
        self.preferred_time = preferred_time
        self.preferred_mode = preferred_mode

def collect_preferences(file):
    '''
    Reads the CSV file from a file-like object and extracts student data and preferences.
    Returns a list of Student objects.
    '''
    students = []
    csv_reader = csv.reader(io.StringIO(file.read().decode('utf-8')))
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        # Ensure the row has at least 15 columns (Canvas quiz format)
        if len(row) < 15: 
            continue
        # Extract relevant data from specific columns
        name, _, sid, _, _, _, _, _, preferred_times_answer, _, preferred_mode, _, _, _, _ = row  
        # Convert preferred times into a list
        preferred_time = preferred_times_answer.split(",")
        students.append(Student(name, sid, preferred_time, preferred_mode))
    return students

def form_groups(students, group_size):
    ''' 
    Groups students based on their preferred study times and modes, aiming to match preferences within groups.
    Returns a list of groups and the dominant preferences for each group.
    '''
    groups = []
    group_preferences = []  # This will store the dominant preference for each group
    
    total_students = len(students)
    num_full_groups = total_students // group_size
    remainder = total_students % group_size
    
    if 0 < remainder < group_size - 1:
        adj_group_size = group_size - 1
        num_smaller_groups = total_students // adj_group_size
        remainder = total_students % adj_group_size
        if 0 < remainder < adj_group_size - 1:
            num_full_groups = remainder
            num_smaller_groups = num_smaller_groups - remainder
    else:
        if remainder == 0:
            adj_group_size = group_size     
    
    # Since preferred_time is a list, we need a consistent way to sort it
    # We'll join the list into a string for sorting purposes
    for student in students:
        student.preferred_time_str = ','.join(sorted(student.preferred_time))
    
    # Sort students by preferred time string and then by preferred mode
    sorted_students = sorted(students, key=lambda s: (s.preferred_time_str, s.preferred_mode))
    
    current_group = []
    current_group_preferences = {'times': {}, 'modes': {}}
    group_size_counter = 0
    
    for student in sorted_students:
        current_group.append(student)
        
        # Count preferences for the current group
        for time in student.preferred_time:
            current_group_preferences['times'][time] = current_group_preferences['times'].get(time, 0) + 1
        current_group_preferences['modes'][student.preferred_mode] = current_group_preferences['modes'].get(student.preferred_mode, 0) + 1

        # Switch group size to the smaller alternative if required.
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
        
        # If the current group has reached the desired size, add it to the list of groups. 
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

def write_groups_to_csv(groups):
    '''
    Writes the formed groups to a CSV file-like object.
    Each row represents a group, starting with "Group N" followed by student names.
    Returns the CSV data as a BytesIO object.
    '''
    output = io.BytesIO()
    # Create a StringIO buffer to write strings, which will then be encoded to bytes
    string_buffer = io.StringIO()
    writer = csv.writer(string_buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Writing header
    writer.writerow(["Group Name", "Student Names"])
    
    for i, group in enumerate(groups):
        group_name = f"Group {i+1}"
        student_names = ", ".join([student.name for student in group])
        writer.writerow([group_name, student_names])
    
    # Write the StringIO content to the BytesIO output
    output.write(string_buffer.getvalue().encode('utf-8'))
    
    # Set the file pointer to the start of the stream before sending
    output.seek(0)
    return output

@app.route('/test', methods=['GET'])
def test():
    return 'CORS is working', 200

@app.route('/upload', methods=['POST'])
def process_csv():
    '''
    Accepts a CSV file and group size, processes the data, and returns grouped CSV data.
    '''
    # Check if a file is present in the request
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Get the desired group size from the form data
    group_size = request.form.get('group_size')
    if not group_size:
        return 'No group size provided', 400
    try:
        group_size = int(group_size)
        if group_size < 2 or group_size > 15:
            return 'Group size must be between 2 and 15', 400
    except ValueError:
        return 'Invalid group size', 400

    # Collect student preferences
    students = collect_preferences(file)
    if students is None:
        return 'Failed to parse the file. Please check the file format and retry.', 400

    # Form groups
    groups, _ = form_groups(students, group_size)

    # Write groups to CSV
    output = write_groups_to_csv(groups)

    # Send the CSV file as a response
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='grouped_students.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
