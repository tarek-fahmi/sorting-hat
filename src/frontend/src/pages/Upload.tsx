import React, { useState } from 'react';
// import axios from 'axios'; // Commented out axios import for now

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [groupSize, setGroupSize] = useState<number>(5);
  const [minGroupSize, setMinGroupSize] = useState<number>(2);
  const [maxGroupSize, setMaxGroupSize] = useState<number>(15);
  const [csvContent, setCsvContent] = useState<string>(''); // State to hold dummy CSV content
  const [attributes, setAttributes] = useState<string[]>([]); // Attributes parsed from CSV
  const [selectedAttributes, setSelectedAttributes] = useState<string[]>([]); // User selected attributes
  const [groups, setGroups] = useState<string[][]>([]); // State to hold groups
  const [enableFlexibility, setEnableFlexibility] = useState<boolean>(false); // Toggle for student flexibility
  const [enableCustomWeights, setEnableCustomWeights] = useState<boolean>(false); // Toggle for custom weights

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      // Reading the CSV file content as text
      const reader = new FileReader();
      reader.onload = () => {
        const content = reader.result as string;
        setCsvContent(content);
        
        // Parse CSV to extract attributes from the header row
        const rows = content.split('\n').map((row) => row.split(','));
        if (rows.length > 0) {
          setAttributes(rows[0]); // Set the first row as attribute headers
        }
      };
      reader.readAsText(selectedFile);
    }
  };

  // Handle group size input changes
  const handleGroupSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setGroupSize(Number(event.target.value));
  };

  const handleMinGroupSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMinGroupSize(Number(event.target.value));
  };

  const handleMaxGroupSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMaxGroupSize(Number(event.target.value));
  };

  // Handle attribute selection
  const handleAttributeSelection = (attribute: string) => {
    setSelectedAttributes((prevSelected) => 
      prevSelected.includes(attribute)
        ? prevSelected.filter((attr) => attr !== attribute)
        : [...prevSelected, attribute]
    );
  };

  // Handle file processing and group formation using dummy data
  const handleFileUpload = () => {
    if (!csvContent) {
      alert('Please select a file first.');
      return;
    }

    // Parsing the CSV file content into an array of students
    const rows = csvContent.split('\n').map((row) => row.split(','));
    const data = rows.slice(1); // Exclude header row

    if (data.length === 0) {
      alert('The selected CSV file is empty.');
      return;
    }

    // Forming groups based on the group size
    let groupNumber = 0;
    const formedGroups: string[][] = [];

    for (let i = 0; i < data.length; i += groupSize) {
      groupNumber++;
      const group = data.slice(i, i + groupSize).map(row => row[0]); // Using student name from first column
      formedGroups.push([`Group ${groupNumber}`, ...group]);
    }

    setGroups(formedGroups);
    alert('File processed and groups formed successfully!');
  };

  // Handle student flexibility toggle
  const handleFlexibilityToggle = () => {
    setEnableFlexibility(!enableFlexibility);
  };

  // Handle custom weights toggle
  const handleCustomWeightsToggle = () => {
    setEnableCustomWeights(!enableCustomWeights);
  };

  return (
    <div>
      <h1>Upload Questionnaire Results</h1>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      
      <h2>Group Settings</h2>
      <input
        type="number"
        value={groupSize}
        min="2"
        max="15"
        onChange={handleGroupSizeChange}
        placeholder="Group Size"
      />
      <input
        type="number"
        value={minGroupSize}
        min="2"
        max="15"
        onChange={handleMinGroupSizeChange}
        placeholder="Min Group Size"
      />
      <input
        type="number"
        value={maxGroupSize}
        min="2"
        max="15"
        onChange={handleMaxGroupSizeChange}
        placeholder="Max Group Size"
      />

      <h2>Attributes Selection</h2>
      {attributes.length > 0 ? (
        <div>
          {attributes.map((attribute, index) => (
            <div key={index}>
              <input
                type="checkbox"
                checked={selectedAttributes.includes(attribute)}
                onChange={() => handleAttributeSelection(attribute)}
              />
              <label>{attribute}</label>
            </div>
          ))}
        </div>
      ) : (
        <p>No attributes available for selection yet. Please upload a CSV file.</p>
      )}

      <h2>Customisation Options</h2>
      <div>
        <input
          type="checkbox"
          checked={enableFlexibility}
          onChange={handleFlexibilityToggle}
        />
        <label>Enable Student Flexibility</label>
      </div>
      <div>
        <input
          type="checkbox"
          checked={enableCustomWeights}
          onChange={handleCustomWeightsToggle}
        />
        <label>Enable Custom Weights for Attributes</label>
      </div>

      <button onClick={handleFileUpload}>Process File</button>

      {/* Uncomment this code when backend is ready */}
      {/*
      const handleFileUpload = async () => {
        if (!file) {
          alert('Please select a file first.');
          return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('group_size', groupSize.toString());

        try {
          const response = await axios.post('http://127.0.0.1:5000/upload', formData);
          console.log('Upload success:', response.data);
          alert('File uploaded successfully');
        } catch (error) {
          console.error('Error uploading file:', error);
          alert('Error uploading file. Please try again.');
        }
      };
      */}

      {/* Displaying formed groups */}
      {groups.length > 0 && (
        <div>
          <h2>Formed Groups</h2>
          <ul>
            {groups.map((group, index) => (
              <li key={index}>
                {group[0]}: {group.slice(1).join(', ')}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Upload;
