import { useState } from "react";
import { SendHorizontal } from "lucide-react";

function ChatInput({ onSend }) {

    const [text, setText] = useState("");

    const handleSend = () => {

        if (!text.trim()) return;

        onSend(text.trim());

        setText("");

    };

    const handleKeyDown = (e) => {

        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            handleSend();

        }

    };

    return (

        <div className="chat-input-wrapper">

            <div className="chat-input">

                <input

                    type="text"

                    value={text}

                    placeholder="Ask LegalGPT anything..."

                    onChange={(e) => setText(e.target.value)}

                    onKeyDown={handleKeyDown}

                />

                <button

                    onClick={handleSend}

                    disabled={!text.trim()}

                >

                    <SendHorizontal size={20} />

                </button>

            </div>

        </div>

    );

}

export default ChatInput;