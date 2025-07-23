# WebMethods to Boomi Migration Tool - Frontend

React TypeScript frontend for the WebMethods to Boomi migration tool. Provides a user-friendly interface for uploading webMethods files and downloading generated migration plans.

## Features

- Drag-and-drop file upload interface
- Multiple file selection support
- File type validation (.html and .txt only)
- Real-time processing status
- Automatic Plan.md download
- Backend health monitoring
- Responsive design
- Full CORS support for cross-machine deployment

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set the backend URL:
   ```
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```
   For remote backend, use:
   ```
   REACT_APP_BACKEND_URL=http://backend-machine-ip:8000
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   The app will open at http://localhost:3000

## Building for Production

```bash
npm run build
```

The build folder will contain optimized static files ready for deployment.

## Deployment Options

### Local Network Access
- The development server is accessible from other machines on the same network
- Use your machine's IP address instead of localhost

### Production Deployment
- Build the app and serve the static files using any web server
- Configure the backend URL in the environment variables
- Ensure CORS is properly configured on the backend

## Usage

1. Open the application in your browser
2. Drag and drop webMethods files (.html or .txt) onto the upload area
3. Or click to browse and select files
4. Review selected files
5. Click "Generate Migration Plan"
6. Wait for processing to complete
7. Plan.md will automatically download to your computer

## Troubleshooting

- **Backend not available:** Ensure the FastAPI backend is running and accessible
- **CORS errors:** Verify the backend has proper CORS configuration
- **File upload fails:** Check that files are .html or .txt format
- **Download doesn't start:** Check browser download settings

## Technology Stack

- React 18 with TypeScript
- Axios for API communication
- CSS3 for styling
- Create React App for build tooling
