# MediCopilot Frontend

A modern, responsive Next.js frontend for the MediCopilot medical AI assistant.

## Features

- **Query Interface**: Ask medical questions with real-time validation and character counting
- **Response Display**: Beautiful answer formatting with source citations and relevance scores
- **Document Upload**: Drag-and-drop file upload with progress tracking
- **Health Monitoring**: Real-time API and database status indicators
- **Query History**: Local storage of recent queries for easy access
- **Responsive Design**: Mobile-first design that works on all devices
- **Accessibility**: WCAG AA compliant with keyboard navigation support

## Tech Stack

- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Shadcn/ui** for UI components
- **React Hook Form** with Zod validation
- **Axios** for API communication
- **Lucide React** for icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- MediCopilot API running on `http://localhost:8000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.local.example .env.local
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
NEXT_PUBLIC_APP_NAME=MediCopilot
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## Usage

### Query Interface

1. Type your medical question in the textarea
2. Adjust the maximum number of results (3-10)
3. Click "Ask Question" or press Enter
4. View the AI-generated answer with source citations

### Document Upload

1. Switch to the "Upload Documents" tab
2. Drag and drop files or click "Choose Files"
3. Supported formats: PDF, TXT, DOCX (max 10MB each)
4. Monitor upload progress and status

### Query History

- View recent queries in the history panel
- Click on any history item to reload it
- Clear history with the trash icon

## API Integration

The frontend communicates with the MediCopilot API:

- `POST /query/` - Submit medical questions
- `POST /documents/upload` - Upload documents
- `GET /health` - Check API health
- `GET /documents/stats` - Get document statistics

## Development

### Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Main page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── ui/               # Shadcn/ui components
│   ├── QueryInterface.tsx
│   ├── ResponseDisplay.tsx
│   ├── DocumentUpload.tsx
│   └── HealthStatus.tsx
├── lib/                  # Utilities
│   ├── api.ts            # API client
│   └── utils.ts          # Helper functions
├── types/                # TypeScript types
│   └── api.ts            # API type definitions
└── public/               # Static assets
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript checks

### Code Style

- Use TypeScript for all components
- Follow React best practices
- Use Tailwind CSS for styling
- Implement proper error handling
- Add loading states for better UX

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables
4. Deploy automatically

### Docker

```bash
# Build image
docker build -t medicopilot-frontend .

# Run container
docker run -p 3000:3000 medicopilot-frontend
```

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_APP_NAME=MediCopilot
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.