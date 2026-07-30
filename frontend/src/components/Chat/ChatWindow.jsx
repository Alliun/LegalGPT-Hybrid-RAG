import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";
import EmptyState from "./EmptyState";
import ChatInput from "../Input/ChatInput";

function ChatWindow({

    messages,

    onSend,

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

    // ==========================================
    // Check whether conversation has started
    // ==========================================

    const hasConversation = messages.some(

        message => message.role === "user"

    );

    return (

        <div className="chat-window">

            {

                !hasConversation ? (

                    <div className="empty-chat">

                        <EmptyState />

                        <ChatInput

                            onSend={onSend}

                        />

                    </div>

                ) : (

                    <>

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

                        <ChatInput

                            onSend={onSend}

                        />

                    </>

                )

            }

        </div>

    );

}

export default ChatWindow;