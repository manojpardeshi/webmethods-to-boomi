import React from 'react';
import './ProcessingStatus.css';

interface ProcessingStatusProps {
  isProcessing: boolean;
  error?: string | null;
  success?: boolean;
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ 
  isProcessing, 
  error, 
  success 
}) => {
  if (!isProcessing && !error && !success) {
    return null;
  }

  return (
    <div className="processing-status">
      {isProcessing && (
        <div className="status-container processing">
          <div className="spinner"></div>
          <p className="status-text">Processing files...</p>
          <p className="status-subtext">
            Analyzing webMethods code and generating migration plan
          </p>
        </div>
      )}

      {error && (
        <div className="status-container error">
          <svg className="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="status-text">Error occurred</p>
          <p className="error-message">{error}</p>
        </div>
      )}

      {success && (
        <div className="status-container success">
          <svg className="status-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="status-text">Migration plan generated!</p>
          <p className="status-subtext">
            Plan.md has been downloaded to your computer
          </p>
        </div>
      )}
    </div>
  );
};

export default ProcessingStatus;
