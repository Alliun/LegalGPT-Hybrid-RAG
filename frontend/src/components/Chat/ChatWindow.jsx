import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";

function ChatWindow({

    messages,

    onExplain,

    onOpen,

    onRelevant

}) {

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({

            behavior: "smooth"

        });

    }, [messages]);

    return (

        <div className="chat-window">

            <div className="messages">

                {

                    messages.map(message => (

                        <MessageBubble

                            key={message.id}

                            message={message}

                            onExplain={onExplain}

                            onOpen={onOpen}

                            onRelevant={onRelevant}

                        />

                    ))

                }

                <div ref={bottomRef} />

            </div>

        </div>

    );

}

export default ChatWindow;