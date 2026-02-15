# AI Project Prioritization App - Complete Deployment Guide
## Step-by-Step Tutorial for Leadership Demo (macOS Version)

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Setup & Testing](#local-setup--testing)
4. [Cloud Deployment](#cloud-deployment)
5. [Leadership Demo Script](#leadership-demo-script)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This AI Project Prioritization App helps your team:
- **Intelligently score** AI projects on two dimensions: Business Value (x-axis) and Technical Feasibility (y-axis)
- **Leverage AI benchmarking** using Claude to compare your use cases against proven patterns
- **Visualize** your portfolio with color-coded categories:
  - 🟢 **Low Hanging Fruit** (Quick Wins): High value + High feasibility
  - 🟠 **Disruptive** (Strategic Bets): High value + Lower feasibility
  - 🔵 **Incremental**: Other projects

---

## ✅ Prerequisites for Mac

### Required:
1. **Python 3.8+** installed on your Mac
   - Check: Open Terminal (⌘ + Space, type "Terminal") and run:
     ```bash
     python3 --version
     ```
   - If not installed or version is too old:
     ```bash
     # Install using Homebrew (recommended)
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     brew install python@3.11
     ```
   - Or download from [python.org](https://www.python.org/downloads/macos/)

2. **Anthropic API Key** (for intelligent scoring)
   - Sign up at [console.anthropic.com](https://console.anthropic.com/)
   - Generate an API key from your account settings
   - Keep this key secure - you'll need it later

### Optional (for cloud deployment):
3. **Streamlit Cloud Account** (free)
   - Sign up at [streamlit.io/cloud](https://streamlit.io/cloud)
4. **GitHub Account** (free)
   - Sign up at [github.com](https://github.com/)

---

## 🖥️ Local Setup & Testing on Mac

### Step 1: Create Project Folder
Open Terminal (⌘ + Space, type "Terminal") and run:

```bash
# Create project directory in your home folder
mkdir ~/ai-prioritization
cd ~/ai-prioritization
```

### Step 2: Save the Files
You have two options:

**Option A: Using Finder**
1. Open Finder and navigate to your home folder
2. Find the `ai-prioritization` folder you just created
3. Drag and drop the downloaded files:
   - `ai_prioritization_app.py`
   - `requirements.txt`

**Option B: Using Terminal**
If files are in your Downloads folder:
```bash
cd ~/ai-prioritization
cp ~/Downloads/ai_prioritization_app.py .
cp ~/Downloads/requirements.txt .
```

Your folder structure should look like:
```
ai-prioritization/
├── ai_prioritization_app.py
└── requirements.txt
```

Verify with:
```bash
ls -la
```

### Step 3: Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# You should see (venv) at the start of your terminal prompt

# Upgrade pip (package manager)
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

**Note:** If you see any permission errors, use:
```bash
pip install --user -r requirements.txt
```

### Step 4: Set Your API Key

**Method 1: Environment Variable (Temporary - for this session only)**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Method 2: Create Secrets File (Recommended - Persistent)**
```bash
# Create .streamlit directory
mkdir -p .streamlit

# Create secrets file with your API key
cat > .streamlit/secrets.toml << 'EOF'
ANTHROPIC_API_KEY = "your-api-key-here"
EOF
```

Replace `your-api-key-here` with your actual Anthropic API key.

**Method 3: Add to Shell Profile (Permanent)**
```bash
# For zsh (default on modern Macs)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# For older Macs using bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bash_profile
source ~/.bash_profile
```

### Step 5: Run the App Locally
```bash
# Make sure you're in the project directory
cd ~/ai-prioritization

# Activate virtual environment if not already active
source venv/bin/activate

# Run the app
streamlit run ai_prioritization_app.py
```

Your default browser should automatically open to `http://localhost:8501`

**If it doesn't open automatically:**
- Open Safari, Chrome, or Firefox
- Navigate to: `http://localhost:8501`

**🎉 Success!** The app should now be running locally.

**To stop the app:**
Press `Control + C` in the Terminal

---

## ☁️ Cloud Deployment (Streamlit Cloud) on Mac

### Option A: Deploy via GitHub (Recommended)

#### Step 1: Create GitHub Repository
1. Go to [github.com](https://github.com/) and sign in
2. Click the "+" icon → "New repository"
3. Name it: `ai-project-prioritization`
4. Choose "Public" or "Private"
5. Click "Create repository"

#### Step 2: Upload Files to GitHub

**Using GitHub Web Interface (Easiest):**
1. On your new repository page, click "uploading an existing file"
2. Open Finder and navigate to `~/ai-prioritization`
3. Drag and drop both files:
   - `ai_prioritization_app.py`
   - `requirements.txt`
4. Click "Commit changes"

**Or using Git Command Line (Terminal):**

First, install Git if you don't have it:
```bash
# Check if Git is installed
git --version

# If not installed, install via Homebrew
brew install git
```

Then push your files:
```bash
# Navigate to your project folder
cd ~/ai-prioritization

# Initialize Git repository
git init

# Add your files
git add ai_prioritization_app.py requirements.txt

# Commit your files
git commit -m "Initial commit"

# Rename branch to main
git branch -M main

# Add your GitHub repository as remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/ai-project-prioritization.git

# Push to GitHub
git push -u origin main
```

**If prompted for credentials:**
- Use your GitHub username
- For password, use a Personal Access Token (not your GitHub password)
- Create token at: Settings → Developer settings → Personal access tokens → Tokens (classic)

#### Step 3: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository:** your-username/ai-project-prioritization
   - **Branch:** main
   - **Main file path:** ai_prioritization_app.py
5. Click "Advanced settings"
6. Add your API key in "Secrets":
   ```toml
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```
7. Click "Deploy!"

**⏱️ Deployment takes 2-5 minutes**

Your app will be live at: `https://your-app-name.streamlit.app`

---

### Option B: Quick Deploy (Without GitHub) - Mac

If you need to demo immediately without GitHub:

**Method 1: Using LocalTunnel (Recommended for Mac)**
```bash
# Install Node.js if you don't have it
brew install node

# Install localtunnel
npm install -g localtunnel

# In one Terminal window, run your Streamlit app
streamlit run ai_prioritization_app.py

# In another Terminal window (⌘ + T for new tab), create tunnel
lt --port 8501
```

You'll get a URL like `https://random-name-123.loca.lt` - share this for demo.

**Method 2: Using ngrok**
```bash
# Install ngrok via Homebrew
brew install ngrok/ngrok/ngrok

# Run your Streamlit app in one Terminal window
streamlit run ai_prioritization_app.py

# In another Terminal window, create tunnel
ngrok http 8501
```

Share the generated HTTPS URL (e.g., `https://abc123.ngrok.io`)

**⚠️ Note:** These URLs are temporary and only work while your Mac is running the app.

---

## 🎤 Leadership Demo Script

### Demo Flow (10-15 minutes)

#### **Introduction (2 min)**
"Today I'm presenting our new AI Project Prioritization Tool. This helps us make data-driven decisions about which AI projects to pursue by scoring them on business value and technical feasibility."

#### **Show the Dashboard (2 min)**
1. Navigate to "📊 Dashboard"
2. Show the empty state or pre-populated examples
3. Explain the quadrants:
   - **Top Right (Quick Wins)**: High value, easy to implement
   - **Bottom Right (Strategic Bets)**: High value, requires investment
   - **Top Left**: Easy but low value
   - **Bottom Left**: Avoid unless strategic

#### **Add a Project - Live Demo (5 min)**
1. Click "➕ Add Project"
2. Use this example:
   - **Project Name:** "Customer Support Chatbot"
   - **Description:** "AI-powered chatbot to handle tier-1 customer support inquiries, reducing support costs and improving response times"
   
3. Fill questionnaire:
   - **Revenue Impact:** Medium ($100K-$1M)
   - **Cost Savings:** High ($500K-$2M)
   - **Users Impacted:** 10,000-100,000
   - **Strategic Alignment:** Highly aligned
   - **Time to Value:** 3-6 months
   - **Data Availability:** Good quality data available
   - **Technical Complexity:** Straightforward
   - **Team Skills:** Good skills available
   - **Infrastructure:** Mostly ready
   - **Integration:** Straightforward

4. Click "🚀 Analyze & Add Project"
5. **Show the AI analysis** - explain how Claude compares it to benchmarks
6. Point out the scores and category

#### **Show the Updated Chart (2 min)**
1. Go back to "📊 Dashboard"
2. Show where the new project appears
3. Highlight the color coding
4. Show top recommendations

#### **Add Another Project - Quick Example (2 min)**
Add a contrasting project:
- **Project Name:** "Autonomous Manufacturing Systems"
- **Description:** "Fully autonomous factory floor management with predictive maintenance and real-time optimization"
- Fill with more ambitious/complex answers
- Show how it plots differently (likely disruptive/orange)

#### **Export & Next Steps (2 min)**
1. Go to "💾 Export Data"
2. Download CSV for further analysis
3. Discuss how the team can use this collaboratively

---

## 🎯 Demo Tips

### Before the Demo:
- ✅ Test the app completely
- ✅ Have 2-3 example projects ready to add
- ✅ Clear browser cache
- ✅ Have backup screenshots in case of technical issues
- ✅ Check your internet connection

### During the Demo:
- 💡 **Emphasize the AI intelligence**: "The system uses Claude to benchmark against proven use cases"
- 💡 **Show the simplicity**: "Non-technical teams can use this"
- 💡 **Highlight collaboration**: "Multiple stakeholders can contribute"
- 💡 **Focus on decisions**: "This helps us prioritize our AI roadmap"

### Talking Points:
1. **Objectivity**: "Reduces bias in project selection"
2. **Speed**: "Get scoring in seconds, not hours of meetings"
3. **Benchmark-driven**: "Learns from industry best practices"
4. **Scalable**: "Can handle dozens of projects"
5. **Exportable**: "Integrates with existing tools"

---

## 🔧 Troubleshooting (Mac-Specific)

### Issue: "command not found: python"
**Solution:**
```bash
# Use python3 instead
python3 -m venv venv

# Or create an alias in ~/.zshrc
echo 'alias python=python3' >> ~/.zshrc
echo 'alias pip=pip3' >> ~/.zshrc
source ~/.zshrc
```

### Issue: "module not found" error
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# You should see (venv) at the start of your prompt

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Permission denied when installing packages
**Solution:**
```bash
# Option 1: Install with --user flag
pip install --user -r requirements.txt

# Option 2: Fix venv permissions
chmod -R u+w venv/
pip install -r requirements.txt
```

### Issue: API key not working
**Solution:**
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# If empty, set it again
export ANTHROPIC_API_KEY="your-api-key-here"

# Or verify secrets file exists and is correct
cat .streamlit/secrets.toml

# Make sure there are no extra quotes or spaces
```

### Issue: Port 8501 already in use
**Solution:**
```bash
# Find what's using the port
lsof -i :8501

# Kill the process (replace PID with actual number from above)
kill -9 PID

# Or run Streamlit on a different port
streamlit run ai_prioritization_app.py --server.port 8502
```

### Issue: App is slow
**Solution:**
- First request to Claude takes 2-3 seconds (normal)
- Close other applications to free up memory
- Check Activity Monitor (⌘ + Space, type "Activity Monitor") for CPU usage
- Ensure you have stable internet connection

### Issue: Browser doesn't open automatically
**Solution:**
```bash
# Manually open browser to:
open http://localhost:8501

# Or specify browser when running Streamlit
streamlit run ai_prioritization_app.py --browser.serverAddress localhost
```

### Issue: "xcrun: error" or missing command line tools
**Solution:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Click Install when prompted
```

### Issue: SSL Certificate errors
**Solution:**
```bash
# Update certificates
pip install --upgrade certifi

# Or use Homebrew Python
brew reinstall python@3.11
```

### Issue: Charts not displaying
**Solution:**
1. Add at least one project first
2. Hard refresh browser (⌘ + Shift + R)
3. Try a different browser (Chrome, Safari, Firefox)
4. Check browser console (Option + ⌘ + J in Chrome) for errors

### Issue: Deployment fails on Streamlit Cloud
**Solution:**
1. Verify `requirements.txt` is in the repository root
2. Check that filenames match exactly (case-sensitive)
3. Ensure API key is in Streamlit Cloud Secrets (not in code)
4. View deployment logs for specific errors:
   - Click on your app in Streamlit Cloud
   - Click "Manage app" → "Logs"

### Issue: Virtual environment activation not working
**Solution:**
```bash
# For zsh (default on modern Macs)
source venv/bin/activate

# If using bash
source venv/bin/activate

# If still not working, deactivate and recreate
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Operation not permitted" errors
**Solution:**
```bash
# macOS Catalina+ has strict security
# Grant Terminal full disk access:
# System Preferences → Security & Privacy → Privacy → Full Disk Access
# Click the lock to make changes
# Add Terminal to the list
```

---

## 📞 Support Resources

- **Streamlit Documentation:** [docs.streamlit.io](https://docs.streamlit.io/)
- **Anthropic API Docs:** [docs.anthropic.com](https://docs.anthropic.com/)
- **Streamlit Community:** [discuss.streamlit.io](https://discuss.streamlit.io/)

---

## 🎓 Advanced Customization

### Modify Benchmark Use Cases
Edit the `BENCHMARK_USE_CASES` dictionary in `ai_prioritization_app.py` to add your organization's specific use cases:

```python
BENCHMARK_USE_CASES = {
    "your_use_case": {
        "tech_feasibility": 8, 
        "business_value": 7, 
        "category": "low_hanging"
    },
    # Add more...
}
```

### Customize Scoring Questions
Modify the `INTAKE_QUESTIONS` dictionary to add your own questions or adjust scoring weights.

### Change Color Scheme
Update the `color_map` in the `create_prioritization_chart()` function:
```python
color_map = {
    "low_hanging": "#10b981",  # Your color
    "disruptive": "#f59e0b",   # Your color
    "incremental": "#6366f1"   # Your color
}
```

---

## 📊 Expected Outcomes

After implementing this tool, your organization should see:
- ✅ Faster decision-making on AI investments
- ✅ More objective, data-driven prioritization
- ✅ Better alignment between business and technical teams
- ✅ Clear communication of project portfolio
- ✅ Reduced risk of pursuing unfeasible projects

---

## 🚀 Next Steps After Demo

1. **Gather feedback** from leadership
2. **Schedule working sessions** with teams to input real projects
3. **Customize** benchmark use cases for your industry
4. **Integrate** with existing project management tools
5. **Establish governance** around scoring criteria

---

**Good luck with your demo! 🎉**
