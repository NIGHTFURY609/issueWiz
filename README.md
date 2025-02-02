# IssueWiz 🎯

## Basic Details
### Team Name: Bonito Flakes

### Team Members
- **Mehrin** - Backend Development (FastAPI)
- **Diya** - Frontend Development (Next.js, TypeScript, GitHub API, AI Integration)
- **Aswathy** - NLP Model Training 

### Hosted Project Link
[Insert hosted project link here]

### Project Description
IssueWiz is an AI-powered assistant designed to simplify open-source contributions. It offers tailored documentation, issue-specific guidance, and interactive assistance, making it easier for contributors to navigate and contribute to open-source projects.

### The Problem Statement
Open-source contributions often require a lot of time to understand project documentation, find relevant issues, and figure out how to contribute effectively. This can overwhelm beginners and slow down contributions.

### The Solution
IssueWiz simplifies this process by providing:
- Interactive, AI-driven documentation
- Tailored issue-specific guidance
- Step-by-step assistance, making open-source contribution more accessible for everyone

## Technical Details
### Technologies/Components Used
For Software:
- **Languages used**: Python, TypeScript
- **Frameworks used**: FastAPI, Next.js
- **Libraries used**: GitHub API, OpenAI API, SentenceTransformer,ThreadPoolExecuter, aiohttp, numpy
- **Tools used**: Render, Vercel

For Hardware:
- No hardware used in this project.

### Implementation
For Software:
#### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/issuewiz.git
cd issuewiz

# Install dependencies
pip install -r requirements.txt
npm install

# Set up environment variables (GitHub API, OpenAI API, etc.)
# Create a `.env` file and add necessary keys

# Start the backend server
uvicorn backend.main:app --reload

# Start the frontend server
npm run dev
```

#### Run
```bash
# Backend
uvicorn backend.main:app --reload

# Frontend
npm run dev
```

### Project Documentation
For Software:

#### Screenshots

![Screenshot1](screenshot1.png)
*This screenshot shows the interactive documentation interface where the assistant guides users step by step.*

![Screenshot2](screenshot2.png)
*This screenshot showcases the issue-specific guidance, where contributors can see tailored suggestions for open-source issues.*

![Screenshot3](screenshot3.png)
*This screenshot displays the AI-generated response for a user query about contributing to a particular repository.*

#### Diagrams

![Workflow](workflow-diagram.png)
*This is the system architecture of IssueWiz, showing the flow between the frontend, backend, and AI models.*

### Project Demo
#### Video
[Add your demo video link here]
*This video demonstrates how IssueWiz guides a user through finding an issue to contribute to and provides tailored instructions.*

#### Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- **Mehrin**: Developed the backend with FastAPI and integrated Supabase for user data and authentication.
- **Diya**: Worked on the frontend development using Next.js, integrating the GitHub API for issue tracking, and AI-powered documentation.
- **Aswathy**: Implemented SentenceTransformer , a deep learning model for issue mapping and code analysis .
