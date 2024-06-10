css = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f0f8ff;
        color: #333;
    }

    .chat-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #e0ffff;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
    }

    .chat-header {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .chat-header h2 {
        color: #333;
        font-weight: 600;
        margin: 0;
    }

    .chat-header img {
        width: 48px;
        height: 48px;
        margin-right: 1rem;
    }

    .chat-messages {
        flex-grow: 1;
        display: flex;
        flex-direction: column-reverse;
    }

    .chat-message {
        display: flex;
        margin-bottom: 1.5rem;
    }

    .chat-message .avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        overflow: hidden;
        margin-right: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    .chat-message .avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .chat-message .message {
        padding: 1rem;
        border-radius: 18px;
        max-width: 75%;
        position: relative;
    }

    .chat-message.user .message {
        background-color: #90ee90;
        color: #333;
        margin-right: auto;
    }

    .chat-message.bot .message {
        background-color: #add8e6;
        color: #333;
        margin-left: auto;
    }

    .chat-message.bot .message:before {
        content: '';
        position: absolute;
        right: -8px;
        top: 12px;
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-left: 8px solid #add8e6;
    }

    .chat-message.user .message:before {
        content: '';
        position: absolute;
        left: -8px;
        top: 12px;
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-right: 8px solid #90ee90;
    }

    .file-upload-container {
        margin-top: 2rem;
        text-align: center;
    }

    .file-upload-instructions {
        margin-top: 1rem;
        font-style: italic;
        color: #666;
    }

    .process-button {
        background-color: #007bff;
        color: #fff;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .process-button:hover {
        background-color: #0056b3;
    }
</style>
"""


bot_template = """
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://cdn.pixabay.com/photo/2012/04/05/02/04/speech-25916_1280.png" alt="Bot Avatar">
    </div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn.pixabay.com/photo/2016/06/24/06/56/text-mining-1476780_1280.png" alt="User Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

header_template = """
<div class="chat-header">
    <img src="https://cdn.pixabay.com/photo/2013/07/13/13/20/bubble-160851_1280.png" alt="PDF Icon">
    <h2>Start your conversations here</h2>
</div>
"""

file_upload_template = """
<div class="file-upload-container">
    <img src="https://cdn.pixabay.com/photo/2016/06/24/06/56/text-mining-1476780_1280.png" alt="PDF Icon" width="80" height="80">
    <span>Chat with PDFs</span>
    <p class="file-upload-instructions">Upload multiple PDF documents and click process to make your documents conversational</p>
</div>
"""