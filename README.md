# 📈 AI Stock Advisor - Minervini Trend Template Analysis
🤖 AI-Powered Stock Analysis | 📊 Technical Charts | 🎯 Minervini Methodology
Professional-grade stock analysis application with advanced AI insights


## 📋 **Table of Contents**
- [✨ Features](#-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [🏗️ Architecture](#️-architecture)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📁 Project Structure](#-project-structure)
- [🎯 Technical Highlights](#-technical-highlights)
- [🔬 Methodology](#-methodology)
- [🚀 Future Enhancements](#-future-enhancements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

## ✨ **Features**

### 🎯 **Core Functionality**
- **Multi-Market Support**: NSE, BSE, and US stock exchanges
- **Real-time Data**: Live stock data via Yahoo Finance API
- **Interactive Charts**: Professional Plotly visualizations with technical indicators
- **AI-Powered Analysis**: GPT-4 powered stock insights using advanced RAG

### 📊 **Technical Analysis**
- **Moving Averages**: 50, 150, and 200-day DMA calculations
- **Minervini Trend Template**: Complete stage detection (1-4)
- **Volume Analysis**: Color-coded volume bars
- **Stage Highlighting**: Visual Stage 2 period identification

### 🤖 **AI Features**
- **Conversational AI**: Natural language stock analysis
- **RAG Implementation**: Retrieval-augmented generation from methodology books
- **Context-Aware Responses**: Stock-specific analysis with historical context
- **Memory Management**: Persistent conversation threads per stock

### 🎨 **User Experience**
- **Responsive Design**: Mobile-friendly Streamlit interface
- **Real-time Feedback**: Loading spinners and progress indicators
- **Error Handling**: Comprehensive error management with user guidance
- **Chat Controls**: Clear conversation history functionality

---

## 🛠️ **Technology Stack**

### **Frontend & UI**
- **Streamlit** - Modern web application framework
- **Plotly** - Interactive data visualizations
- **Pandas** - Data manipulation and analysis

### **AI & NLP**
- **LangChain** - LLM application framework
- **OpenAI GPT-4** - Advanced language model via Groq API
- **LangGraph** - Agent orchestration and memory management

### **Data & Storage**
- **ChromaDB** - Vector database for RAG implementation
- **HuggingFace Embeddings** - BGE-base-v1.5 for semantic search
- **Yahoo Finance** - Real-time stock data API

### **Processing & Analysis**
- **PyMuPDF** - PDF document parsing for knowledge base
- **Markdown Splitters** - Intelligent document chunking
- **Technical Analysis** - Custom moving average calculations

---

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Stock Logic    │────│  Yahoo Finance  │
│                 │    │  (Analysis)     │    │     API         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chat Agent    │────│   LangChain     │────│   GPT-4 via     │
│   (LangGraph)   │    │   Tools         │    │     Groq        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RAG Engine    │────│   ChromaDB      │────│   Minervini     │
│   (Retrieval)   │    │   Vectors       │    │   Knowledge     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Data Flow**
1. **User Input** → Symbol selection and market choice
2. **Data Fetching** → Yahoo Finance API for historical data
3. **Technical Analysis** → Moving average calculations and stage detection
4. **AI Processing** → RAG retrieval + GPT-4 analysis
5. **Visualization** → Interactive charts and AI insights

---

## 📦 **Installation**

### **Prerequisites**
- Python 3.8+
- pip/uv package manager
- Git

### **Setup Instructions**

1. **Clone the repository**
   ```bash
   git clone https://github.com/gordhan04/AI_Stock_Advisor.git
   cd ai_stock_advisor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt / uv add-r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Add knowledge base**
   ```bash
   # Place Minervini methodology PDFs in data/raw/
   mkdir -p data/raw
   # Add your PDF files here
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## 🚀 **Usage**

### **Basic Analysis**
1. Select market (NSE/BSE/US) from sidebar
2. Enter stock symbol (e.g., TCS, AAPL, RELIANCE)
3. View interactive price chart with technical indicators
4. Review Minervini stage analysis

### **AI Consultation**
1. Ask specific questions about the stock
2. Get AI-powered insights based on Minervini methodology
3. Receive context-aware analysis with relevant references

### **Example Queries**
```
"Is this stock in a proper buyable stage?"
"What are the key resistance levels?"
"Should I consider this for my portfolio?"
"How does this compare to Minervini's criteria?"
```

---

## 📁 **Project Structure**

```
ai-stock-advisor/
├── 📄 app.py                 # Main Streamlit application
├── 📄 chat_agent.py          # LangChain agent configuration
├── 📄 stock_logic.py         # Technical analysis functions
├── 📄 plot_chart.py          # Chart visualization module
├── 📄 rag_engine.py          # RAG implementation
├── 📄 main.py               # CLI entry point
├── 📄 requirements.txt      # Python dependencies
├── 📄 pyproject.toml        # Project configuration
├── 📁 data/
│   ├── 📁 raw/             # Source documents (PDFs)
│   └── 📁 processed/       # Vector database
├── 📄 README.md            # Project documentation
└── 📄 .env                 # Environment variables
```

---

## 🎯 **Technical Highlights**

### **Advanced AI Implementation**
- **RAG Architecture**: Implemented retrieval-augmented generation for accurate, methodology-based responses
- **Agent Orchestration**: Used LangGraph for complex agent workflows with memory management
- **Context Preservation**: Maintained conversation continuity with thread-based memory

### **Data Engineering**
- **Vector Database**: ChromaDB implementation with semantic search capabilities
- **Document Processing**: Intelligent PDF parsing and markdown-based chunking
- **Real-time Data Pipeline**: Efficient data fetching and processing pipeline

### **Financial Analysis**
- **Minervini Methodology**: Complete implementation of the 4-stage trend template
- **Technical Indicators**: Custom moving average calculations with proper handling
- **Multi-Market Support**: Unified interface for different stock exchanges

### **Production-Ready Features**
- **Error Handling**: Comprehensive exception management with user-friendly messages
- **Performance Optimization**: Efficient data structures and caching mechanisms
- **Scalable Architecture**: Modular design for easy extension and maintenance

---

## 🔬 **Methodology**

### **Minervini Trend Template**
This application implements Mark Minervini's proven trend template methodology:

1. **Stage 1**: Basing - Stock building a foundation above major moving averages
2. **Stage 2**: Advancing - Strong uptrend with price > 150 DMA > 200 DMA
3. **Stage 3**: Topping - Exhaustion phase with weakening momentum
4. **Stage 4**: Declining - Downtrend with price below key moving averages

### **Technical Requirements**
- Consistent earnings growth
- Strong relative strength
- Institutional sponsorship
- Market direction alignment
- Proper basing structure

---

## 🚀 **Future Enhancements**

### **Phase 1: Enhanced Analytics**
- [ ] **Options Analysis**: Put/call ratio and implied volatility
- [ ] **Fundamental Integration**: Earnings, revenue, and ratio analysis
- [ ] **Sentiment Analysis**: News and social media sentiment tracking

### **Phase 2: Advanced AI**
- [ ] **Multi-Agent System**: Specialized agents for different analysis types
- [ ] **Portfolio Optimization**: AI-driven portfolio construction
- [ ] **Risk Assessment**: Dynamic position sizing recommendations

### **Phase 3: Platform Features**
- [ ] **User Authentication**: Secure user accounts and preferences
- [ ] **Real-time Alerts**: Price and technical indicator notifications
- [ ] **Backtesting Engine**: Historical strategy performance analysis

---

## 🤝 **Contributing**

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/chart`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/chart`)
5. Open a Pull Request

### **Development Guidelines**
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Govardhan Purohit**
- 📧 Email: govardhan.purohit@gmail.com
- 🔗 LinkedIn: [Govardhan Purohit](www.linkedin.com/in/govardhan-purohit-88b223318)
- 🐙 GitHub: [govardhan-purohit](https://github.com/gordhan04)

### **Technical Skills Demonstrated**
- **Full-Stack Development**: Python, Streamlit, API integration
- **AI/ML Engineering**: LangChain, RAG, GPT integration
- **Data Engineering**: Vector databases, ETL pipelines
- **Financial Analysis**: Technical analysis, algorithmic trading concepts
- **Cloud & DevOps**: Environment management, deployment strategies
- **Software Architecture**: Modular design, scalable systems

---

<div align="center">
  <p><strong>⭐ Star this repo if you found it helpful!</strong></p>
  <p>Built with ❤️ using cutting-edge AI and financial analysis techniques</p>
</div>