import React, { useState, useEffect } from 'react';
import './App.css';
import FileUploader from './components/FileUploader';
import ProcessingStatus from './components/ProcessingStatus';
import { apiService } from './services/api';

function App() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    // Check backend health on mount
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    const healthy = await apiService.checkHealth();
    setBackendHealthy(healthy);
  };

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);
    setError(null);
    setSuccess(false);
  };

  const handleMigrate = async () => {
    if (selectedFiles.length === 0) {
      setError('Please select at least one file');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setSuccess(false);

    try {
      await apiService.migrateFiles(selectedFiles);
      setSuccess(true);
      // Clear files after successful migration
      setSelectedFiles([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>WebMethods to Boomi Migration Tool</h1>
        <p className="subtitle">
          Upload your webMethods files to generate a Boomi migration plan
        </p>
      </header>

      <main className="App-main">
        {backendHealthy === false && (
          <div className="health-warning">
            <p>⚠️ Backend service is not available. Please ensure the API server is running.</p>
            <button onClick={checkBackendHealth} className="retry-button">
              Retry Connection
            </button>
          </div>
        )}

        <FileUploader
          onFilesSelected={handleFilesSelected}
          acceptedFileTypes=".html,.txt"
          disabled={isProcessing}
        />

        {selectedFiles.length > 0 && !isProcessing && (
          <div className="action-container">
            <button
              className="migrate-button"
              onClick={handleMigrate}
              disabled={backendHealthy === false}
            >
              Generate Migration Plan
            </button>
          </div>
        )}

        <ProcessingStatus
          isProcessing={isProcessing}
          error={error}
          success={success}
        />
      </main>

      <footer className="App-footer">
        <p>
          Powered by LangChain and Claude Opus 4 via OpenRouter
        </p>
      </footer>
    </div>
  );
}

export default App;
