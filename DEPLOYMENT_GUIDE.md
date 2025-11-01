# 🚀 Streamlit Deployment Guide for Vallabh409's Projects

This guide provides step-by-step instructions for deploying your Python projects on Streamlit Cloud.

## 📋 Projects Ready for Streamlit Deployment

### ✅ Already Deployed/Ready:
1. **Food_wastage_management** - Food wastage management system with Streamlit UI
2. **metro-churn-app** - Customer churn prediction app
3. **image-calssification** - Image classification with Streamlit (Already Live!)
4. **shopper-spectrum-app** - Customer segmentation and clustering

### 🆕 Newly Added Streamlit Apps:
1. **zomato-Unsupervised-clustering** - Restaurant clustering analysis
2. **A-B-Test-Analysis-for-E-commerce-Website** - A/B test statistical analysis
3. **Movie-Dataset-Analysis** - TMDB movie dataset analysis

---

## 🛠️ Prerequisites

Before deploying, ensure each repository has:
- ✅ `app.py` - The main Streamlit application file
- ✅ `requirements.txt` - Python dependencies
- ✅ Data files (CSV, models, etc.) if required by the app
- ✅ GitHub repository is public (or you have Streamlit Cloud access to private repos)

---

## 📝 Step-by-Step Deployment Instructions

### Step 1: Sign Up / Log In to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in" and authenticate with your GitHub account
3. Grant Streamlit Cloud access to your repositories

### Step 2: Deploy a New App
1. Click "New app" button
2. Select your repository from the dropdown
3. Choose the branch (usually `main`)
4. Specify the file path to your app:
   - For most projects: `app.py`
   - For image-classification: `app (1).py`
5. (Optional) Set a custom URL/subdomain
6. Click "Deploy!"

### Step 3: Monitor Deployment
- Streamlit Cloud will:
  1. Clone your repository
  2. Install dependencies from `requirements.txt`
  3. Start your Streamlit app
  4. Provide a public URL

- Deployment typically takes 2-5 minutes
- Watch the logs for any errors

### Step 4: Share Your App
- Once deployed, you'll receive a URL like: `https://your-app-name.streamlit.app`
- Share this URL with anyone!
- The app will auto-update when you push changes to GitHub

---

## 🔧 Repository-Specific Notes

### zomato-Unsupervised-clustering
- **App File:** `app.py`
- **Data Required:** `zomato.csv`
- **Features:** Interactive K-Means clustering, 2D/3D visualizations, cluster statistics
- **URL Path:** `/`

### A-B-Test-Analysis-for-E-commerce-Website
- **App File:** `app.py`
- **Data Required:** `ab_data.csv`, `countries.csv`
- **Features:** Conversion rate analysis, statistical significance testing, visualizations
- **URL Path:** `/`

### Movie-Dataset-Analysis
- **App File:** `app.py`
- **Data Required:** `tmdb-movies.csv`
- **Features:** Budget/revenue analysis, genre analysis, rating distribution, movie search
- **URL Path:** `/`

### Food_wastage_management
- **App File:** `app.py`
- **Data Required:** Database files in `database/` folder
- **Special Note:** Uses SQLite database

### shopper-spectrum-app
- **App File:** `app.py`
- **Data Required:** `kmeans_model.pkl`, `scaler.pkl`
- **Special Note:** Uses pre-trained ML models

### metro-churn-app
- **App File:** Check repository for main file
- **Special Note:** Customer churn prediction model

### image-calssification
- **App File:** `app (1).py`
- **Special Note:** Already deployed! ✅

---

## 🐛 Common Issues & Solutions

### Issue 1: Module Not Found Error
**Solution:** Ensure all required packages are listed in `requirements.txt`
```txt
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
scikit-learn==1.3.0
scipy==1.11.3
```

### Issue 2: File Not Found Error
**Solution:** 
- Verify data files are committed to the repository
- Check file paths are relative (not absolute)
- Ensure file names match exactly (case-sensitive)

### Issue 3: Memory Limit Exceeded
**Solution:**
- Use `@st.cache_data` decorator for data loading
- Consider sampling large datasets
- Optimize data processing

### Issue 4: App Sleeping/Timeout
**Solution:**
- Free tier apps sleep after inactivity
- App will wake up when accessed (takes ~30 seconds)
- Consider Streamlit Cloud paid plan for always-on apps

---

## 💡 Best Practices

### 1. Use Caching
```python
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    return df
```

### 2. Add Loading Indicators
```python
with st.spinner('Loading data...'):
    data = load_data()
```

### 3. Handle Errors Gracefully
```python
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    st.error("Data file not found!")
```

### 4. Add Configuration
```python
st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide"
)
```

### 5. Keep requirements.txt Updated
- Pin versions for reproducibility
- Remove unused packages
- Test locally before deploying

---

## 📊 Monitoring & Updates

### View Logs
1. Go to your app on Streamlit Cloud
2. Click "Manage app" → "Logs"
3. View real-time logs and errors

### Update Your App
1. Make changes to your code locally
2. Commit and push to GitHub
3. Streamlit Cloud auto-deploys the changes
4. Changes appear within 1-2 minutes

### Restart Your App
- From Streamlit Cloud dashboard
- Click "Manage app" → "Reboot app"
- Useful for clearing cache or fixing stuck states

---

## 🔐 Security Considerations

### Environment Variables
For sensitive data (API keys, passwords):
1. Go to "Manage app" → "Settings" → "Secrets"
2. Add secrets in TOML format:
```toml
[database]
username = "myuser"
password = "mypassword"

[api]
key = "your-api-key"
```
3. Access in code:
```python
import streamlit as st
api_key = st.secrets["api"]["key"]
```

### Never Commit:
- Database passwords
- API keys
- Private credentials
- Sensitive user data

---

## 🎯 Quick Deployment Checklist

Before deploying each app:
- [ ] `app.py` exists and runs locally
- [ ] `requirements.txt` includes all dependencies
- [ ] Data files are committed (if needed)
- [ ] No hardcoded credentials
- [ ] Code is pushed to GitHub
- [ ] Repository is public (or Streamlit has access)
- [ ] Tested locally with `streamlit run app.py`

---

## 📱 Access Your Apps

Once deployed, you can access your apps at:
- `https://[app-name]-[username].streamlit.app`

Example:
- `https://zomato-clustering-vallabh409.streamlit.app`
- `https://ab-test-analysis-vallabh409.streamlit.app`
- `https://movie-analysis-vallabh409.streamlit.app`

---

## 🆘 Support Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery) - For inspiration

---

## 🎉 You're Ready to Deploy!

All your Python projects now have Streamlit apps ready for deployment. Follow the steps above to make them live!

**Happy Deploying! 🚀**

---

*Last Updated: November 1, 2025*
*Author: Comet Assistant for Vallabh409*
