# Robot Waiter Speech Test Using Deepseek AI

This is the test for a voice-enabled chatbot that processes food orders using AI (Deepseek via Ollama) and speech recognition. 
Through testing I have deemed this 'not ready yet' for use in our robot waiter, this is due to a number of reasons, including: 
- The AI often trailing off
- The AI derailing when misunderstanding a prompt
- Not having powerful enough hardware to run a more advanced model fast enough
The AI model has shown promise in regards to the way it can handle prompts however, allowing users to specify roughly what they want or using other names for dishes and pinpointing which dish they would really like, as well as deciphering some inconsistencies that the speech interpreter may relay.
## How to Run

### Prerequisites
- Python 3.x
- Microphone access

### Installation
1. **Install dependencies**:
   ```bash
   pip install flask speechrecognition pyaudio
   ```

2. **Install Ollama**:
   - Download from [ollama.ai](https://ollama.ai/download)
   - Pull the AI model:
     ```bash
     ollama pull deepseek-r1:1.5b
     ```

### File Structure
```
project/
├── ai_interpreter.py
├── speech_interpreter.py
├── prompt.txt
└── static/
    └── index.html
```

### Running the Program
1. Start the Flask server:
   ```bash
   python ai_interpreter.py
   ```

2. Open your browser to:
   ```
   http://localhost:5000
   ```

3. Use the interface:
   - **Type** messages in the text box and click "Send"
   - **Speak** by clicking "Listen" (allow microphone access)

### Troubleshooting
- **Microphone issues**: Test `speech_interpreter.py` standalone
- **Model errors**: Ensure Ollama is running (`ollama serve`)
- **Permission errors**: Grant microphone access in your browser