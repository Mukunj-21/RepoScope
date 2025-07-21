# REPOSCOPE

<div align="center">

![GitHub Repository Analyzer Pro](https://via.placeholder.com/800x200/4299e1/ffffff?text=GitHub+Repository+Analyzer+Pro)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/github-repo-analyzer)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**🔍 Analyze any GitHub repository with the power of Local LLM**

[Live Demo](https://your-vercel-url.vercel.app) • [Documentation](#documentation) • [Features](#features) • [Installation](#installation)

</div>

## 🚀 Overview

GitHub Repository Analyzer Pro is a cutting-edge web application that provides **comprehensive AI-powered analysis** of any GitHub repository. Built with Django and integrated with local LLM models via Ollama, it offers deep insights into code structure, quality, security, and best practices.

### ✨ What makes it special?

- 🤖 **Local LLM Integration** - Uses Ollama for offline AI analysis
- 📊 **Comprehensive Analysis** - 10-point detailed code examination
- 🌓 **Dark/Light Theme** - Beautiful, responsive UI with theme switching
- 🔍 **Smart Search** - AI-powered code search across repositories
- 💾 **Memory System** - Context-aware analysis with persistent storage
- ⚡ **Real-time Preview** - GitHub-like file preview with syntax highlighting

## 🎯 Key Features

<table>
  <tr>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/64/2919/2919906.png" width="48px" alt="Analysis"/>
      <br><b>AI Analysis</b>
      <br>Comprehensive code analysis using local LLM models
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/64/1055/1055646.png" width="48px" alt="Preview"/>
      <br><b>File Preview</b>
      <br>GitHub-like interface with syntax highlighting
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/64/622/622669.png" width="48px" alt="Search"/>
      <br><b>Smart Search</b>
      <br>Context-aware search across entire codebase
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/64/2920/2920277.png" width="48px" alt="Theme"/>
      <br><b>Theme Toggle</b>
      <br>Beautiful dark/light mode with smooth transitions
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/64/3064/3064197.png" width="48px" alt="Memory"/>
      <br><b>Memory System</b>
      <br>Persistent analysis storage and context management
    </td>
    <td align="center">
      <img src="https://cdn-icons-png.flaticon.com/64/1828/1828833.png" width="48px" alt="Offline"/>
      <br><b>Offline Ready</b>
      <br>No API dependencies, runs completely offline
    </td>
  </tr>
</table>

## 🛠 Tech Stack

<div align="center">

| Backend | Frontend | AI/ML | Deployment |
|---------|----------|-------|------------|
| ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white) | ![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white) |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | ![LLaMA](https://img.shields.io/badge/LLaMA-FF6B6B?style=for-the-badge&logo=meta&logoColor=white) | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | ![CodeLlama](https://img.shields.io/badge/CodeLlama-4B8BBE?style=for-the-badge&logo=python&logoColor=white) | - |

</div>

## 📸 Screenshots

<details>
<summary>🌅 Light Theme</summary>

![Light Theme](https://via.placeholder.com/800x500/ffffff/333333?text=Light+Theme+Screenshot)

*Clean, professional light mode interface*

</details>

<details>
<summary>🌙 Dark Theme</summary>

![Dark Theme](https://via.placeholder.com/800x500/1a202c/ffffff?text=Dark+Theme+Screenshot)

*Elegant dark mode for comfortable coding sessions*

</details>

<details>
<summary>🔍 Analysis View</summary>

![Analysis View](https://via.placeholder.com/800x500/4299e1/ffffff?text=Analysis+Results+View)

*Comprehensive AI-powered code analysis results*

</details>

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- GitHub Personal Access Token (optional, for higher rate limits)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/github-repo-analyzer.git
cd github-repo-analyzer
```



### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:

source venv/bin/activate

# On Windows:

venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt
```


### 3. Configure Environment Variables

```bash
# Create .env file

cp .env.example .env

# Edit .env with your settings

GITHUB_TOKEN=your_github_personal_access_token # Optional
SECRET_KEY=your_django_secret_key
DEBUG=True
```


### 4. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```


### 5. Install Ollama (for AI Analysis)

```bash
# macOS

curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service

ollama serve

# Pull required models (in another terminal)

ollama pull codellama:7b
ollama pull llama3:8b
```


### 6. Run Application

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` and start analyzing repositories! 🎉

## 📖 Usage Guide

### Basic Usage

1. **Enter Repository URL**: Paste any public GitHub repository URL
2. **Load Repository**: Click "Load Repository" to fetch files
3. **Select File**: Click on any file to preview its contents
4. **Analyze**: Click "Analyze File" for comprehensive AI analysis
5. **Search**: Use the search box to find specific code patterns

### Advanced Features

#### 🤖 AI Analysis Output

The AI provides detailed analysis covering:

- **Primary Purpose & Functionality**
- **Code Structure & Architecture**
- **Dependencies & Imports**
- **Key Algorithms & Logic**
- **Data Structures & Models**
- **API & Interfaces**
- **Security & Best Practices**
- **Testing & Debugging**
- **Performance Considerations**
- **Integration Points**

#### 🔍 Smart Search

- Natural language queries
- Context-aware results
- Cross-file relationship mapping
- Code usage patterns

## 🏗 Architecture

```bash
github-repo-analyzer/
├── repo_analyzer/ # Django project settings
├── analyzer/ # Main application
│ ├── models.py # Database models
│ ├── views.py # API endpoints
│ ├── services/ # Business logic
│ │ ├── github_service.py
│ │ ├── llm_service.py
│ │ └── memory_service.py
│ └── templates/ # Frontend templates
├── static/ # Static files
├── requirements.txt # Dependencies
└── .env # Environment variables
```


### Service Architecture

```bash
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ GitHub API  │───▶│ GitHub Service  │───▶│Repository Files │
└─────────────┘    └─────────────────┘    └─────────────────┘
                                                  │
                                                  ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│Frontend UI  │◀───│ Memory Service  │◀───│   LLM Service   │
└─────────────┘    └─────────────────┘    └─────────────────┘
      ▲                    │                       │
      │                    ▼                       ▼
┌─────────────┐   ┌─────────────────┐     ┌─────────────────┐
│ Database    │   │   AI Analysis   │     │      Ollama     │
└─────────────┘   └─────────────────┘     └─────────────────┘
```


## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | No | None |
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Enable debug mode | No | False |

### Ollama Models

| Model | Purpose | Size | Download Command |
|-------|---------|------|------------------|
| `codellama:7b` | Code analysis | 3.8GB | `ollama pull codellama:7b` |
| `llama3:8b` | General analysis | 4.7GB | `ollama pull llama3:8b` |
| `deepseek-coder:6.7b` | Fallback option | 3.8GB | `ollama pull deepseek-coder:6.7b` |

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI**:

```bash
npm i -g vercel
```


2. **Deploy**:
```bash 
vercel
```

3. **Set Environment Variables** in Vercel dashboard:
- `GITHUB_TOKEN`
- `SECRET_KEY`
- `DEBUG=False`

### Docker Deployment
```bash
Dockerfile included in repository
docker build -t github-analyzer .
docker run -p 8000:8000 github-analyzer
```


## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python manage.py test`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

## 📈 Roadmap

### 🎯 Version 2.0 (Planned)

- [ ] **Batch Repository Analysis** - Analyze multiple repositories
- [ ] **API Rate Limiting** - Smart GitHub API usage optimization
- [ ] **Export Features** - PDF/JSON reports generation
- [ ] **Team Collaboration** - Multi-user workspace support
- [ ] **CI/CD Integration** - GitHub Actions workflow
- [ ] **Advanced Visualizations** - Dependency graphs and metrics

### 🔮 Future Features

- [ ] **Enterprise SSO** - SAML/OAuth integration
- [ ] **Custom Models** - Train on organization-specific patterns
- [ ] **IDE Extensions** - VS Code/IntelliJ plugins
- [ ] **Mobile App** - React Native companion app

## 🐛 Troubleshooting

### Common Issues

**Issue**: Repository won't load
```bash
Solution: Check if repository is public and URL is correct
Enable debug logging to see detailed error messages
```


**Issue**: Ollama not connecting

```bash
Solution: Ensure Ollama service is running
ollama serve

Check if models are installed
ollama list
```


**Issue**: Analysis takes too long
```bash
Solution: Large files may take time. Check Ollama logs:
ollama logs
```


### Getting Help

- 📖 Check our [Documentation](https://github.com/yourusername/github-repo-analyzer/wiki)
- 🐛 Report bugs via [GitHub Issues](https://github.com/yourusername/github-repo-analyzer/issues)
- 💬 Join our [Discord Community](https://discord.gg/your-invite)
- 📧 Email: support@yourproject.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team** - For making local LLM deployment simple
- **Django Community** - For the amazing web framework
- **Highlight.js** - For beautiful syntax highlighting
- **Lucide Icons** - For clean, modern icons
- **GitHub API** - For comprehensive repository data

## 📊 Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/yourusername/github-repo-analyzer?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/github-repo-analyzer?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/github-repo-analyzer)
![GitHub license](https://img.shields.io/github/license/yourusername/github-repo-analyzer)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/github-repo-analyzer)

**⭐ Star this repository if you found it helpful!**

</div>

<div align="center">

**Built with ❤️ by [Your Name](https://github.com/yourusername)**

[🌟 Star](https://github.com/yourusername/github-repo-analyzer) • [🍴 Fork](https://github.com/yourusername/github-repo-analyzer/fork) • [📖 Docs](https://github.com/yourusername/github-repo-analyzer/wiki) • [🐛 Issues](https://github.com/yourusername/github-repo-analyzer/issues)

</div>
