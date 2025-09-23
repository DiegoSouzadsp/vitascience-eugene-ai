# Eugene Schwartz VSL Analyzer - Frontend

Professional web interface for analyzing Video Sales Letters using Eugene Schwartz's 5 Levels of Market Consciousness methodology.

## 🌟 Features

### Core Functionality
- **VSL Text Analysis**: Submit VSL text for comprehensive analysis
- **N8N Integration**: Real-time integration with N8N workflow at `localhost:5678/webhook/analyze-vsl-squad`
- **Results Display**: Structured presentation of analysis results
- **Demo Mode**: Sample VSL for demonstration purposes
- **Health Monitoring**: System status checking and monitoring

### Analysis Results Display
- **Consciousness Level Analysis**: Identification of market consciousness level (1-5)
- **Framework Analysis**: Structural evaluation of the VSL
- **Problem Identification**: Detection of 5+ specific issues
- **Eugene's Solutions**: Actionable improvements based on methodology
- **Creative Angles**: 3+ new creative approaches suggested

### User Experience
- **Professional UI**: Bootstrap-based responsive design
- **Real-time Validation**: Character count, word count, reading time
- **Loading States**: Enhanced loading animations and progress indicators
- **Error Handling**: Comprehensive error messages and user feedback
- **Mobile Responsive**: Optimized for all device sizes
- **Accessibility**: WCAG compliant design patterns

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- N8N instance running on `localhost:5678`
- Eugene Schwartz VSL analysis workflow active in N8N

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

5. **Access the interface**:
   Open http://localhost:8080 in your browser

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
HOST=0.0.0.0
PORT=8080

# N8N Integration
N8N_WEBHOOK_URL=http://localhost:5678/webhook/analyze-vsl-squad
N8N_BASE_URL=http://localhost:5678
```

### N8N Webhook Configuration

The frontend expects the N8N workflow to:
- Accept POST requests at `/webhook/analyze-vsl-squad`
- Process JSON payload with `vsl_text` field
- Return structured analysis results

Example request format:
```json
{
  "vsl_text": "Your VSL content here...",
  "analysis_type": "complete",
  "timestamp": "2024-01-20T10:30:00Z",
  "client": "squad-vitascience-frontend"
}
```

## 📁 Project Structure

```
frontend/
├── app.py                 # Main Flask application
├── run.py                 # Production runner script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Main analysis form
│   ├── results.html      # Analysis results display
│   ├── demo.html         # Demo page with sample VSL
│   └── error.html        # Error page template
│
└── static/              # Static assets
    ├── css/
    │   └── custom.css    # Enhanced styling
    └── js/
        └── enhanced.js   # Advanced JavaScript functionality
```

## 🎯 Usage

### Basic Analysis

1. **Navigate to the home page**: http://localhost:8080
2. **Enter VSL text**: Paste your Video Sales Letter content (minimum 100 characters)
3. **Select analysis type**:
   - Complete Analysis (recommended)
   - Consciousness Only
   - Structure Only
   - Improvements Only
4. **Submit for analysis**: Click "Analisar VSL"
5. **View results**: Review detailed analysis with actionable insights

### Demo Analysis

1. **Navigate to demo page**: http://localhost:8080/demo
2. **Review sample VSL**: Pre-loaded example from health/weight loss market
3. **Run analysis**: Click "Analisar Demo"
4. **Examine results**: See how the analyzer identifies consciousness levels and suggests improvements

### API Usage

The frontend also provides a REST API endpoint:

```bash
# POST /api/analyze
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "vsl_text": "Your VSL content here...",
    "analysis_type": "complete"
  }'
```

## 📊 Analysis Output

The system provides comprehensive analysis including:

### Consciousness Analysis
- **Dominant Level**: Primary consciousness level (1-5)
- **Level Description**: Detailed explanation of the identified level
- **Strategies**: Specific approaches for the identified level

### Structural Analysis
- **Copy Structure**: Evaluation of VSL organization
- **Flow Assessment**: Analysis of logical progression
- **Conversion Elements**: Identification of persuasion components

### Problem Identification
- **Consciousness Mismatches**: Gaps between content and audience level
- **Structural Issues**: Problems with VSL organization
- **Copy Weaknesses**: Specific copywriting improvements needed

### Improvement Suggestions
- **Consciousness Alignment**: How to better match audience level
- **Structural Enhancements**: Organization improvements
- **Copy Optimizations**: Specific text improvements

### Creative Angles
- **New Approaches**: Fresh angles based on Eugene's methodology
- **Level-Specific**: Tailored to identified consciousness level
- **Market-Tested**: Based on proven frameworks

## 🔍 Health Monitoring

### System Status
- **Health Endpoint**: `/health` - Returns system and N8N status
- **Status Indicator**: Navigation shows real-time system health
- **Connectivity Check**: Automatic N8N connectivity verification

### Error Handling
- **Timeout Protection**: 2-minute timeout for analysis requests
- **Connection Error Handling**: Graceful failure when N8N unavailable
- **User Feedback**: Clear error messages with troubleshooting tips

## 🎨 Customization

### Styling
- **Custom CSS**: `static/css/custom.css` for enhanced styling
- **Bootstrap Integration**: Uses Bootstrap 5.1.3 for responsive design
- **Color Scheme**: Professional blue/gray theme with accent colors

### JavaScript Enhancement
- **Enhanced UX**: `static/js/enhanced.js` for advanced interactions
- **Real-time Validation**: Character counting, form validation
- **Loading States**: Smooth animations and progress indicators
- **Keyboard Shortcuts**: Ctrl+Enter to submit forms

## 🚀 Production Deployment

### Basic Production Setup

1. **Set environment to production**:
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-secure-production-key
   ```

2. **Use production WSGI server**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

## 🔧 Troubleshooting

### Common Issues

1. **N8N Connection Error**:
   - Verify N8N is running on localhost:5678
   - Check webhook URL configuration
   - Ensure workflow is active

2. **Analysis Timeout**:
   - Check N8N workflow performance
   - Verify OpenAI API connectivity in N8N
   - Reduce VSL text length if very large

3. **Static Files Not Loading**:
   - Verify static directory structure
   - Check Flask static file configuration
   - Clear browser cache

### Debug Mode

Enable debug mode for detailed error information:
```bash
export DEBUG=True
python run.py
```

## 📋 Requirements

### Python Dependencies
- Flask==2.3.2
- requests==2.31.0
- python-dotenv==1.0.0
- gunicorn==21.2.0 (for production)

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Integration with Squad Vitascience

This frontend is specifically designed for the Squad Vitascience demonstration:

- **Webhook Integration**: Uses `/webhook/analyze-vsl-squad` endpoint
- **Brazilian Portuguese**: User interface in Portuguese
- **Health Market Focus**: Optimized for supplement/health VSL analysis
- **Professional Presentation**: Suitable for client demonstrations

## 📞 Support

For issues related to:
- **Frontend functionality**: Check this README and error logs
- **N8N integration**: Verify N8N workflow configuration
- **Analysis quality**: Review Eugene Schwartz methodology implementation

The frontend is designed to be self-contained and work independently, requiring only a properly configured N8N instance for full functionality.