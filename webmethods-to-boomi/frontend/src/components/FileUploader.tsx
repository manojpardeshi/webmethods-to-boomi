import React, { useState, useRef } from 'react';
import './FileUploader.css';

interface FileUploaderProps {
  onFilesSelected: (files: File[]) => void;
  acceptedFileTypes: string;
  disabled?: boolean;
}

const FileUploader: React.FC<FileUploaderProps> = ({ 
  onFilesSelected, 
  acceptedFileTypes,
  disabled = false 
}) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (files: FileList | null) => {
    if (!files) return;

    const fileArray = Array.from(files);
    const validFiles = fileArray.filter(file => 
      file.name.endsWith('.html') || file.name.endsWith('.txt')
    );

    if (validFiles.length !== fileArray.length) {
      alert('Only .html and .txt files are allowed');
    }

    setSelectedFiles(validFiles);
    onFilesSelected(validFiles);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
    onFilesSelected(newFiles);
  };

  const clearFiles = () => {
    setSelectedFiles([]);
    onFilesSelected([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="file-uploader">
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''} ${disabled ? 'disabled' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={!disabled ? handleClick : undefined}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedFileTypes}
          onChange={(e) => handleFileSelect(e.target.files)}
          style={{ display: 'none' }}
          disabled={disabled}
        />
        
        <div className="drop-zone-content">
          <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p className="drop-zone-text">
            {isDragging 
              ? 'Drop files here...' 
              : 'Drag & drop webMethods files here or click to browse'
            }
          </p>
          <p className="file-types">Accepted: .html, .txt files</p>
        </div>
      </div>

      {selectedFiles.length > 0 && (
        <div className="selected-files">
          <div className="files-header">
            <h3>Selected Files ({selectedFiles.length})</h3>
            <button 
              className="clear-button" 
              onClick={clearFiles}
              disabled={disabled}
            >
              Clear All
            </button>
          </div>
          <ul className="file-list">
            {selectedFiles.map((file, index) => (
              <li key={index} className="file-item">
                <span className="file-name">{file.name}</span>
                <span className="file-size">
                  ({(file.size / 1024).toFixed(2)} KB)
                </span>
                <button
                  className="remove-button"
                  onClick={() => removeFile(index)}
                  disabled={disabled}
                  aria-label={`Remove ${file.name}`}
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUploader;
