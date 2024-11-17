import React, { useState } from 'react';
import axios from 'axios';
import '../stylesheets/Upload.css';
import EditableGroups from './EditableGroups';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [groupSize, setGroupSize] = useState<number | "">("");
  const [groups, setGroups] = useState<{ name: string; members: string[] }[] | null>(null);

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  // Handle group size input
  const handleGroupSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = Number(event.target.value);
    if (value >= 2 && value <= 15) {
      setGroupSize(value);
    } else {
      alert("Group size must be between 2 and 15.");
    }
  };

  // Handle file upload to backend
  const handleFileUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    if (!groupSize) {
      alert('Please enter a group size.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('group_size', groupSize.toString());

    try {
      const response = await axios.post('http://127.0.0.1:5001/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });

      console.log('Upload success:', response);
      const csvText = await response.data.text();
      const parsedCsvData = parseCsv(csvText);
      setGroups(formatGroups(parsedCsvData));
      alert('File uploaded successfully');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file. Please try again.');
    }
  };

  // Handle download CSV file
  const handleDownloadCsv = () => {
    if (!groups) return;

    let csvContent = 'Group Name,Student Names\n';
    groups.forEach(group => {
      csvContent += `${group.name},${group.members.join(',')}\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'updated_grouped_students.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Parse CSV text to array
  const parseCsv = (csvText: string): string[][] => {
    const rows = csvText.split('\n');
    return rows.map(row => row.split(',').map(cell => cell.replace(/"/g, '').trim()));
  };

  // Format parsed CSV data into groups
  const formatGroups = (parsedData: string[][]): { name: string; members: string[] }[] => {
    return parsedData.slice(1, parsedData.length - 1).map((row) => ({
      name: row[0],
      members: row.slice(1),
    }));
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">Upload CSV File</h1>
      <div className="upload-form">
        <div className="file-input-container">
          <label className="file-label" htmlFor="file-upload">Choose File</label>
          <input id="file-upload" type="file" accept=".csv" onChange={handleFileChange} className="file-input" />
        </div>
        <div className="group-size-container">
          <label className="group-size-label" htmlFor="group-size">Group Size</label>
          <input id="group-size" type="number" value={groupSize} onChange={handleGroupSizeChange} min="2" max="15" className="group-size-input" />
        </div>
        <button className="upload-button" onClick={handleFileUpload}>Upload File</button>
      </div>
      {groups && (
        <EditableGroups initialGroups={groups} onSave={setGroups} />
      )}
      {groups && (
        <button className="download-button" onClick={handleDownloadCsv}>Download CSV</button>
      )}
    </div>
  );
};

export default Upload;
