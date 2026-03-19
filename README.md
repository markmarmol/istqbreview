# ISTQB Review Quiz App

An interactive ISTQB (International Software Testing Qualifications Board) exam preparation tool built with Streamlit and AI-powered explanations.

## Features

- **Interactive Quiz Interface**: Multiple-choice questions from the ISTQB syllabus
- **AI-Generated Explanations**: Gemini 2.5 Flash provides detailed explanations for each answer
- **Progress Tracking**: Track your score and performance throughout the quiz
- **Styled Answer Explanations**: Beautiful, color-coded explanation boxes
- **Real-time Feedback**: Immediate feedback on answer correctness

## Tech Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - Google Gemini 2.5 Flash (for explanations)
  - OpenAI Embeddings (for vector search)
- **Vector Database**: Pinecone
- **Document Processing**: LangChain
- **Language**: Python 3.10+

## Project Structure

```
istqbreview/
├── app.py                              # Main Streamlit application
├── questions.py                        # Quiz questions database
├── test.ipynb                          # Jupyter notebook for testing
├── requirements.txt                    # Python dependencies
├── documents/                          # ISTQB syllabus PDFs
│   └── ISTQB_CTFL_Syllabus_v4.0.1.pdf
└── images/                             # Images for documentation
```

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/istqbreview.git
cd istqbreview
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. Click **"Start Quiz"** to begin
2. Read each question carefully
3. Select your answer from the four options
4. Click **"Submit Answer"** to check your response
5. View explanations in the three-column layout:
   - **Default Explanation**: Pre-written explanation
   - **AI-Generated Explanation**: Gemini-powered insights
   - **ISTQ Syllabus Source**: Relevant syllabus content
6. Click **"Next Question"** to continue or **"End Quiz"** to finish

## Quiz Statistics

- Automatically tracks your score
- Displays final results with percentage
- Shows correct/incorrect answer count

## Dependencies

Key packages used:
- `streamlit` - Web framework
- `google-genai` - Google Gemini API
- `langchain_openai` - OpenAI embeddings
- `python-dotenv` - Environment variable management
- `pinecone-client` - Vector database

See `requirements.txt` for complete list.

## API Keys Required

1. **OpenAI API Key**: For embeddings
   - Get from [openai.com](https://openai.com/api/)

2. **Google Gemini API Key**: For AI explanations
   - Get from [ai.google.dev](https://ai.google.dev/)

3. **Pinecone API Key**: For vector search (optional)
   - Get from [pinecone.io](https://pinecone.io/)

## Current Limitations

- Vectorstore integration requires langchain-pinecone (Python 3.14 compatibility pending)
- ISTQ syllabus source retrieval currently disabled
- Feature will be enabled once dependency compatibility is resolved

## Future Enhancements

- [ ] ISTQ syllabus source integration
- [ ] Topic-based filtering
- [ ] Performance analytics dashboard
- [ ] Question difficulty ratings
- [ ] Custom question sets
- [ ] Mobile responsive design
- [ ] Multi-language support

## Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions, please open an issue on GitHub.

## Disclaimer

This is an educational tool to help prepare for the ISTQB CTFL exam. Please refer to the official ISTQB syllabus for accurate and complete exam preparation material.

---

**Note**: Keep your API keys secure and never commit them to version control. Use `.env` files and add them to `.gitignore`.
