ARCHITECTURE & PIPELINE
------------------------
Page: single-page portfolio + embedded chat.
Sections: Hero/Intro, Skills, Chat (heading: "Ask Anything About This Person").
No unnecessary buttons; only message input + send.

PIPELINE
- User loads page → GET serves portfolio HTML.
- User types question → POST /chat (or /) sends JSON {message}.
- Backend (main.py) responds → frontend renders reply in chat box.
- Session/typing states minimal; error fallback shown.

COMPONENTS NEEDED
1. Portfolio layout (header, skills, intro)
2. Chat interface (box, input, button, messages)
3. Fetch/POST connector to backend endpoint
4. Response renderer with basic formatting

PROMPT FOR ANTI-GRAVITY
"Build a single-page portfolio frontend that connects to the backend in main.py. One page: top is a clean portfolio showing skills/introduction; below it a chat section with the heading 'Ask Anything About This Person'. The chat must have an input field and send button, post the message via fetch/POST to the backend route, receive the response, and display it in the chat box. Do not add unnecessary buttons or pages. Ensure the POST works with the existing backend and the GET page displays the portfolio. Do not modify main.py. Keep design minimal, typography-focused like Claude's clean layout."
