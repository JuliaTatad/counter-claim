import os
import json
from flask import Flask, render_template, request, jsonify, session
from google import genai
from google.genai import types
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

class ArbitrationCoCounsel:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        self.model = "gemini-2.5-flash"
        
        # Enhanced system prompt for arbitration expertise
        self.system_prompt = """You are an expert strategic co-counsel specializing in international and domestic arbitration. You provide sophisticated legal analysis, strategic guidance, and practical insights to arbitration lawyers.

Your expertise includes:
- International Commercial Arbitration (ICC, LCIA, SIAC, etc.)
- Investment Treaty Arbitration (ICSID, UNCITRAL)
- Construction Arbitration (ICC, LCIA Construction)
- Sports Arbitration (CAS)
- Procedural strategy and case management
- Evidence assessment and presentation
- Settlement negotiations and mediation
- Award enforcement and challenge proceedings
- Arbitrator selection and challenges
- Cross-border dispute resolution

Provide detailed, practical advice while maintaining the highest professional standards. Consider jurisdictional nuances, procedural rules, and strategic implications in your responses. Always maintain attorney-client privilege awareness and suggest when external counsel consultation may be warranted."""

    def generate_response(self, user_input, conversation_history=None):
        """Generate response using Gemini API with arbitration context"""
        
        # Build conversation contents
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=self.system_prompt)],
            ),
            types.Content(
                role="model",
                parts=[types.Part.from_text(text="I understand. I'm ready to serve as your strategic co-counsel for arbitration matters. I'll provide expert analysis and guidance while maintaining the highest professional standards. How may I assist you with your arbitration case or strategy today?")],
            )
        ]
        
        # Add conversation history if available
        if conversation_history:
            for entry in conversation_history:
                contents.append(
                    types.Content(
                        role="user" if entry['role'] == 'user' else "model",
                        parts=[types.Part.from_text(text=entry['content'])],
                    )
                )
        
        # Add current user input
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            )
        )
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
            ),
            response_mime_type="text/plain",
        )
        
        try:
            response = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response += chunk.text
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error processing your request. Please try again. Error: {str(e)}"

# Initialize the co-counsel
co_counsel = ArbitrationCoCounsel()

@app.route('/')
def index():
    """Main chat interface"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['conversation_history'] = []
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        # Get conversation history from session
        conversation_history = session.get('conversation_history', [])
        
        # Generate response
        response = co_counsel.generate_response(user_message, conversation_history)
        
        # Update conversation history
        conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        conversation_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 20 exchanges to manage memory
        if len(conversation_history) > 40:
            conversation_history = conversation_history[-40:]
        
        session['conversation_history'] = conversation_history
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    session['conversation_history'] = []
    return jsonify({'status': 'success'})

@app.route('/api/export', methods=['GET'])
def export_conversation():
    """Export conversation as JSON"""
    conversation_history = session.get('conversation_history', [])
    return jsonify({
        'session_id': session.get('session_id'),
        'conversation': conversation_history,
        'exported_at': datetime.now().isoformat()
    })

# Template for the HTML interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arbitration Strategic Co-Counsel</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .chat-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 1200px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 20px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .chat-title {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .chat-title i {
            font-size: 24px;
        }
        
        .chat-title h1 {
            font-size: 24px;
            font-weight: 600;
        }
        
        .chat-subtitle {
            font-size: 14px;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .header-actions {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            background: #f8f9fa;
        }
        
        .message {
            display: flex;
            gap: 15px;
            max-width: 85%;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .message.user .message-avatar {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        .message.assistant .message-avatar {
            background: linear-gradient(135deg, #2c3e50, #3498db);
        }
        
        .message-content {
            background: white;
            padding: 15px 20px;
            border-radius: 18px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .message-content::before {
            content: '';
            position: absolute;
            top: 15px;
            width: 0;
            height: 0;
            border: 8px solid transparent;
        }
        
        .message.user .message-content::before {
            right: -15px;
            border-left-color: #667eea;
        }
        
        .message.assistant .message-content::before {
            left: -15px;
            border-right-color: white;
        }
        
        .chat-input-container {
            padding: 20px 30px;
            background: white;
            border-top: 1px solid #e9ecef;
        }
        
        .chat-input-form {
            display: flex;
            gap: 15px;
        }
        
        .chat-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .chat-input:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        
        .send-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }
        
        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .typing-indicator {
            display: none;
            align-items: center;
            gap: 10px;
            color: #666;
            font-style: italic;
            padding: 10px 0;
        }
        
        .typing-dots {
            display: flex;
            gap: 3px;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #3498db;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
        .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        
        .welcome-message {
            text-align: center;
            color: #666;
            padding: 40px;
            background: white;
            border-radius: 15px;
            margin: 20px;
        }
        
        .welcome-message h2 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .scrollbar-thin::-webkit-scrollbar {
            width: 6px;
        }
        
        .scrollbar-thin::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 3px;
        }
        
        .scrollbar-thin::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 3px;
        }
        
        .scrollbar-thin::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
        
        @media (max-width: 768px) {
            .chat-container {
                height: 95vh;
                margin: 10px;
            }
            
            .chat-header {
                padding: 15px 20px;
            }
            
            .chat-title h1 {
                font-size: 20px;
            }
            
            .message {
                max-width: 90%;
            }
            
            .chat-input-container {
                padding: 15px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="chat-title">
                <i class="fas fa-balance-scale"></i>
                <div>
                    <h1>Arbitration Strategic Co-Counsel</h1>
                    <div class="chat-subtitle">Expert guidance for arbitration lawyers</div>
                </div>
            </div>
            <div class="header-actions">
                <button class="btn btn-secondary" onclick="exportConversation()">
                    <i class="fas fa-download"></i> Export
                </button>
                <button class="btn btn-secondary" onclick="clearConversation()">
                    <i class="fas fa-trash"></i> Clear
                </button>
            </div>
        </div>
        
        <div class="chat-messages scrollbar-thin" id="chatMessages">
            <div class="welcome-message">
                <h2><i class="fas fa-handshake"></i> Welcome to Your Strategic Co-Counsel</h2>
                <p>I'm here to provide expert guidance on arbitration matters including procedural strategy, case analysis, settlement negotiations, and award enforcement. How may I assist you with your arbitration case today?</p>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span>Co-counsel is analyzing...</span>
        </div>
        
        <div class="chat-input-container">
            <form class="chat-input-form" id="chatForm">
                <input type="text" class="chat-input" id="messageInput" 
                       placeholder="Describe your arbitration case or ask for strategic guidance..." 
                       autocomplete="off">
                <button type="submit" class="send-btn" id="sendBtn">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </form>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const chatForm = document.getElementById('chatForm');
        const typingIndicator = document.getElementById('typingIndicator');

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = messageInput.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            messageInput.value = '';
            
            // Show typing indicator
            showTyping();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    addMessage(data.response, 'assistant');
                } else {
                    addMessage('I apologize, but I encountered an error. Please try again.', 'assistant');
                }
            } catch (error) {
                addMessage('I apologize, but I encountered a connection error. Please try again.', 'assistant');
            }
            
            hideTyping();
        });

        function addMessage(content, role) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.innerHTML = role === 'user' ? 'L' : '<i class="fas fa-balance-scale"></i>';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = formatMessage(content);
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function formatMessage(content) {
            // Basic formatting for better readability
            return content
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n/g, '<br>');
        }

        function showTyping() {
            typingIndicator.style.display = 'flex';
            sendBtn.disabled = true;
        }

        function hideTyping() {
            typingIndicator.style.display = 'none';
            sendBtn.disabled = false;
        }

        async function clearConversation() {
            if (confirm('Are you sure you want to clear the conversation?')) {
                try {
                    await fetch('/api/clear', { method: 'POST' });
                    chatMessages.innerHTML = `
                        <div class="welcome-message">
                            <h2><i class="fas fa-handshake"></i> Welcome to Your Strategic Co-Counsel</h2>
                            <p>I'm here to provide expert guidance on arbitration matters including procedural strategy, case analysis, settlement negotiations, and award enforcement. How may I assist you with your arbitration case today?</p>
                        </div>
                    `;
                } catch (error) {
                    alert('Error clearing conversation');
                }
            }
        }

        async function exportConversation() {
            try {
                const response = await fetch('/api/export');
                const data = await response.json();
                
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `arbitration-counsel-${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch (error) {
                alert('Error exporting conversation');
            }
        }

        // Auto-resize input and focus
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });

        messageInput.focus();
    </script>
</body>
</html>
'''

# Create templates directory and file if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')
with open('templates/index.html', 'w') as f:
    f.write(HTML_TEMPLATE)

if __name__ == '__main__':
    # Ensure GEMINI_API_KEY is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️  WARNING: GEMINI_API_KEY environment variable not set!")
        print("Please set your Gemini API key: export GEMINI_API_KEY='your-api-key-here'")
    
    print("🚀 Starting Arbitration Strategic Co-Counsel...")
    print("📍 Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    print("🚀 Starting Arbitration Strategic Co-Counsel...")
    print("📍 Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)