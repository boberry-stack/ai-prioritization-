# 🎯 AI Project Prioritization Tool

An intelligent Streamlit app that helps organizations prioritize AI projects using a 2D matrix (Business Value × Technical Feasibility) with AI-powered benchmarking.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-AI-orange?style=for-the-badge)

## 🌟 Features

- **📊 Interactive 2D Prioritization Matrix**: Visualize projects by Business Value (x-axis) and Technical Feasibility (y-axis)
- **🤖 AI-Powered Scoring**: Uses Claude to intelligently score projects based on benchmarks and questionnaire responses
- **🎨 Smart Color Coding**:
  - 🟢 **Low Hanging Fruit** (Quick Wins): High feasibility + High value
  - 🟠 **Disruptive** (Strategic Bets): High value + Lower feasibility  
  - 🔵 **Incremental**: Other projects
- **📝 Comprehensive Intake Questionnaire**: Captures business value and technical feasibility factors
- **💾 Export Capabilities**: Download data as JSON or CSV
- **🎯 Benchmark-Driven**: Compares against proven AI use case patterns

## 🚀 Quick Start (macOS)

### Prerequisites
- macOS 10.14 or later
- Python 3.8+ (check with `python3 --version`)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Open Terminal** (⌘ + Space, type "Terminal")

2. **Create project directory**
   ```bash
   mkdir -p ~/ai-prioritization
   cd ~/ai-prioritization
   ```

3. **Add your files**
   - Download all project files
   - Move them to `~/ai-prioritization`
   - Or use Finder to drag files into this folder

4. **Install dependencies**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate it
   source venv/bin/activate
   
   # Install packages
   pip install -r requirements.txt
   ```

5. **Set up your API key**
   ```bash
   # Create secrets directory
   mkdir -p .streamlit
   
   # Create secrets file
   cat > .streamlit/secrets.toml << 'EOF'
   ANTHROPIC_API_KEY = "your-api-key-here"
   EOF
   ```
   
   Replace `your-api-key-here` with your actual Anthropic API key.

6. **Run the app**
   ```bash
   streamlit run ai_prioritization_app.py
   ```

7. **Open your browser** to `http://localhost:8501`

**🎉 That's it!** See `MAC_QUICK_START.md` for detailed Mac-specific guide.

## 📖 How It Works

### 1. Add Your AI Projects
Fill out a comprehensive questionnaire covering:

**Business Value Factors:**
- Revenue impact
- Cost savings potential
- Number of users impacted
- Strategic alignment
- Time to value

**Technical Feasibility Factors:**
- Data availability and quality
- Technical complexity
- Team skills and readiness
- Infrastructure requirements
- Integration difficulty

### 2. AI-Powered Analysis
The system uses Claude to:
- Compare your project against benchmark use cases (chatbots, document search, fraud detection, etc.)
- Analyze questionnaire responses
- Generate intelligent scores on both dimensions
- Provide justification for the scoring

### 3. Visualize & Prioritize
View all projects on an interactive matrix that clearly shows:
- Which projects are "quick wins" (top-right quadrant)
- Which require strategic investment (bottom-right quadrant)
- Which should be reconsidered (other quadrants)

## 🎯 Use Cases

- **Portfolio Planning**: Visualize and prioritize your entire AI project pipeline
- **Resource Allocation**: Make data-driven decisions about where to invest
- **Stakeholder Communication**: Clear visual communication of project priorities
- **Risk Assessment**: Identify high-risk, high-reward opportunities
- **Team Alignment**: Objective framework for cross-functional discussions

## 📊 Example Projects

The app comes with benchmark scoring for common AI use cases:
- Customer support chatbots
- Document search and retrieval
- Fraud detection systems
- Predictive maintenance
- Recommendation engines
- Code generation
- And more...

## 🛠️ Customization

### Add Your Own Benchmarks
Edit `BENCHMARK_USE_CASES` in `ai_prioritization_app.py`:

```python
BENCHMARK_USE_CASES = {
    "your_use_case": {
        "tech_feasibility": 8,
        "business_value": 9,
        "category": "low_hanging"
    }
}
```

### Modify Questions
Customize `INTAKE_QUESTIONS` to fit your organization's needs.

### Change Color Scheme
Update the color map in `create_prioritization_chart()`.

## 🌐 Cloud Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repository
4. Add your API key in Secrets
5. Deploy!

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📁 Project Structure

```
ai-project-prioritization/
├── ai_prioritization_app.py    # Main application
├── requirements.txt             # Python dependencies
├── DEPLOYMENT_GUIDE.md         # Complete deployment tutorial
├── README.md                   # This file
└── .streamlit/
    ├── config.toml             # Streamlit configuration
    └── secrets.toml.template   # API key template
```

## 🔒 Security Notes

- **Never commit your API key** to version control
- Use `.streamlit/secrets.toml` for local development
- Use Streamlit Cloud Secrets for deployment
- Add `.streamlit/secrets.toml` to `.gitignore`

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional benchmark use cases
- More sophisticated scoring algorithms
- Integration with project management tools
- Export to additional formats
- Multi-language support

## 📄 License

This project is provided as-is for organizational use.

## 🆘 Support

For detailed setup and troubleshooting:
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Check [Streamlit documentation](https://docs.streamlit.io/)
- Review [Anthropic API docs](https://docs.anthropic.com/)

## 🎓 Demo Script

Presenting to leadership? Check out the **Leadership Demo Script** section in `DEPLOYMENT_GUIDE.md` for a step-by-step presentation guide.

## ✨ Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Interactive charts
- [Claude](https://www.anthropic.com/) - AI analysis
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

**Ready to prioritize smarter? Get started now! 🚀**
