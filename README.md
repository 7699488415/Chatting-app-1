# Real-Time Chat Application

A modern, real-time chat application built with Flask, Socket.IO, HTML, CSS, and JavaScript. Features include user authentication, real-time messaging, typing indicators, emoji support, and responsive design.

## Features

- **Real-time messaging** with WebSocket support
- **User authentication** with login page
- **Guest login** option for quick access
- **Typing indicators** to show when users are typing
- **Emoji picker** for expressive messaging
- **Responsive design** that works on desktop and mobile
- **User list** showing online users
- **Message history** with timestamps
- **Connection status** indicators
- **Desktop notifications** for new messages
- **Modern UI** with smooth animations

## Screenshots

### Login Page
- Clean, modern login interface
- Guest login option
- Form validation
- Responsive design

### Chat Interface
- Real-time message display
- User sidebar with online users
- Typing indicators
- Emoji picker
- Message input with character counter

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd chat-app
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Go to `http://localhost:5000`
   - You'll see the login page

## Usage

### Login Options

1. **Regular Login**
   - Username: `demo`
   - Password: `password`
   - Or create your own credentials

2. **Guest Login**
   - Click "Join as Guest" button
   - Automatically generates a guest username

### Chat Features

- **Send Messages**: Type in the input field and press Enter or click Send
- **Emoji**: Click the emoji button to open the emoji picker
- **Typing Indicators**: See when other users are typing
- **User List**: View all online users in the sidebar
- **Responsive**: Works on both desktop and mobile devices

### Keyboard Shortcuts

- `Enter`: Send message
- `Shift + Enter`: New line in message
- `Escape`: Close emoji picker

## File Structure

```
chat-app/
├── app.py                 # Flask backend with Socket.IO
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   ├── login.html        # Login page template
│   └── chat.html         # Chat page template
└── static/
    ├── css/
    │   ├── login.css     # Login page styles
    │   └── chat.css      # Chat page styles
    └── js/
        ├── login.js      # Login page functionality
        ├── chat.js       # Chat page (simulation mode)
        └── chat-websocket.js  # Chat page (WebSocket mode)
```

## Technical Details

### Backend (Flask + Socket.IO)
- **Flask**: Web framework for serving pages and API endpoints
- **Flask-SocketIO**: Real-time WebSocket communication
- **User Management**: In-memory user storage with session handling
- **Message Storage**: In-memory message history (last 100 messages)
- **Room Support**: General chat room with join/leave functionality

### Frontend (HTML + CSS + JavaScript)
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox
- **Socket.IO Client**: Real-time communication with the server
- **Local Storage**: User session persistence
- **Modern JavaScript**: ES6+ features with class-based architecture
- **CSS Animations**: Smooth transitions and loading states

### WebSocket Events

#### Client to Server
- `join_chat`: Join the chat room
- `send_message`: Send a message
- `typing`: Indicate user is typing
- `stop_typing`: Stop typing indicator
- `ping`: Connection health check

#### Server to Client
- `welcome`: Welcome message for new users
- `user_joined`: Notification when user joins
- `user_left`: Notification when user leaves
- `new_message`: New message received
- `user_typing`: Someone is typing
- `user_stop_typing`: Someone stopped typing
- `users_list`: Current users list
- `message_history`: Recent message history

## API Endpoints

- `GET /`: Login page
- `GET /chat`: Chat page
- `GET /api/users`: Get connected users
- `GET /api/messages`: Get recent messages
- `GET /health`: Health check endpoint

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (default: 'your-secret-key-here')
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: '0.0.0.0')

### Customization Options
- **Message Limit**: Change max messages stored (default: 100)
- **Character Limit**: Modify message character limit (default: 500)
- **Reconnection**: Adjust reconnection attempts (default: 5)
- **User Limit**: Add user limit if needed

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Use a production WSGI server like Gunicorn
2. Set up a reverse proxy with Nginx
3. Use a proper database for message storage
4. Implement user authentication with a database
5. Add SSL/TLS encryption

### Example Production Setup
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Security Considerations

- Input sanitization for messages
- XSS protection with HTML escaping
- CORS configuration for cross-origin requests
- Session management with secure tokens
- Rate limiting for message sending (recommended)

## Future Enhancements

- **Database Integration**: PostgreSQL or MongoDB for persistent storage
- **User Registration**: Full user account system
- **Private Messages**: Direct messaging between users
- **File Sharing**: Image and file upload support
- **Message Reactions**: Like/react to messages
- **Chat Rooms**: Multiple chat rooms/channels
- **Admin Panel**: User management and moderation
- **Push Notifications**: Browser push notifications
- **Message Search**: Search through message history
- **User Profiles**: Avatar and profile customization

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Dependencies Not Installing**
   ```bash
   # Upgrade pip
   pip install --upgrade pip
   
   # Install with verbose output
   pip install -r requirements.txt -v
   ```

3. **WebSocket Connection Issues**
   - Check firewall settings
   - Ensure port 5000 is accessible
   - Try different browsers
   - Check browser console for errors

4. **Mobile Display Issues**
   - Clear browser cache
   - Check viewport meta tag
   - Test in different mobile browsers

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Check server logs for backend issues
4. Create an issue with detailed information

---

**Enjoy chatting with your real-time chat application!** 🎉💬

