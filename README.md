# FastAPI Twilio Integration with Whisper Model

This project implements a FastAPI-based server to handle real-time audio processing using Twilio and OpenAI's Whisper model. It includes WebSocket support for real-time audio data streaming, processes the audio using OpenAI's Whisper API, and sends back the transcribed text to Twilio to respond to the user.

## Features

- **Twilio Integration**: Handles incoming audio streams from Twilio.
- **Real-time WebSocket Communication**: Enables WebSocket connection for real-time processing.
- **Audio Processing**: Uses OpenAI's Whisper model to transcribe audio to text.
- **FastAPI Backend**: Handles requests and WebSocket communication efficiently.

## Prerequisites

Before setting up the project, make sure you have the following installed:

- Python 3.7+
- pip (Python package installer)
- Node.js and npm (for WebSocket support)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Dibyendu-13/fastapi-twilio-whisper.git
cd fastapi-twilio-whisper
```

### 2. Set up a virtual environment

Create a virtual environment in the project directory:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:

```bash
venv\Scriptsctivate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root of the project with the following variables:

```plaintext
PORT=5050
OPENAI_API_KEY=<your_openai_api_key>
TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
```

### 5. Running the Server

Run the FastAPI server using the following command:

```bash
uvicorn app:app --reload
```

This will start the server at `http://localhost:5050`.

### 6. Testing

To test the integration, make requests to the `/twilio/events` endpoint using Twilio’s webhook, and connect to the WebSocket endpoint `/ws/audio` for real-time audio processing.

### 7. WebSocket Client

To connect to the WebSocket server, you can use any WebSocket client. Here's an example using JavaScript in the browser:

```javascript
const ws = new WebSocket("ws://localhost:5050/ws/audio");

ws.onopen = () => {
  console.log("Connected to WebSocket server");
  // Send audio data or listen for messages
};

ws.onmessage = (event) => {
  console.log("Received:", event.data);
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};
```

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
