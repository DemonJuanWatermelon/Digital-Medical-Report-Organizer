# Digital Medical Report Organizer - Frontend

A modern Next.js frontend application for the Digital Medical Report Organizer with a sleek black/green UI theme.

## Features

- **Modern UI**: Built with Next.js 14 and Tailwind CSS
- **Dark Theme**: Professional black/green color scheme
- **Responsive Design**: Works on desktop, tablet, and mobile
- **File Upload**: Drag & drop medical report uploads
- **Real-time Updates**: Live status updates for report processing
- **AI Integration**: Display AI analysis results and insights

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **File Handling**: React Dropzone
- **HTTP Client**: Axios
- **State Management**: React Query
- **Forms**: React Hook Form

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Environment Variables

Create a `.env.local` file with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── app/                 # Next.js app directory
│   ├── globals.css     # Global styles
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Home page
├── components/         # React components
│   ├── Header.tsx      # Navigation header
│   ├── UploadModal.tsx # File upload modal
│   ├── ReportCard.tsx  # Report display card
│   └── StatsCard.tsx   # Statistics card
├── lib/               # Utility functions
├── types/             # TypeScript type definitions
└── public/            # Static assets
```

## Features Overview

### Dashboard
- Overview statistics
- Recent reports grid
- Quick upload access

### File Upload
- Drag & drop interface
- File type validation
- Progress indicators
- Error handling

### Report Management
- Report cards with key information
- Status indicators
- Risk level classification
- Quick actions

## Styling

The application uses a custom Tailwind configuration with:

- **Primary Colors**: Green gradient (primary-400 to primary-600)
- **Dark Theme**: Dark-800 to dark-900 backgrounds
- **Accent Colors**: Various status colors for different states

## API Integration

The frontend communicates with the FastAPI backend through:

- RESTful API calls
- File upload endpoints
- Real-time status updates
- Authentication handling

## Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Write responsive components
4. Test on multiple screen sizes
5. Follow accessibility guidelines
