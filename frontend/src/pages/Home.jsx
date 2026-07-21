import { useEffect, useRef, useState } from "react";

import Sidebar from "../components/Sidebar/Sidebar";
import Topbar from "../components/Topbar/Topbar";
import ChatWindow from "../components/Chat/ChatWindow";
import ChatInput from "../components/Input/ChatInput";

function Home() {

    const [messages, setMessages] = useState([
        {
            id: 1,
            role: "assistant",
            type: "text",
            content:
                "# 👋 Welcome to LegalGPT\n\nAsk me any legal question and I'll retrieve the most relevant judgments."
        }
    ]);

    

    const bottomRef = useRef(null);

    // ============================================
    // Auto Scroll
    // ============================================

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages]);

    // ============================================
    // Send Message
    // ============================================

    const sendMessage = async (text) => {

        if (!text.trim()) return;

        const userMessage = {

            id: Date.now(),

            role: "user",

            type: "text",

            content: text

        };

        const loadingId = Date.now() + 1;

        const loadingMessage = {

            id: loadingId,

            role: "assistant",

            type: "loading"

        };

        setMessages(prev => [

            ...prev,

            userMessage,

            loadingMessage

        ]);

        try {

            const response = await fetch(

                "http://127.0.0.1:5000/api/chat",

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify({

                        query: text

                    })

                }

            );

            const data = await response.json();

            let assistantMessage;

            if (data.type === "explanation") {

                assistantMessage = {

                    id: loadingId,

                    role: "assistant",

                    type: "text",

                    content: data.content

                };

            }

            else {

                assistantMessage = {

                    id: loadingId,

                    role: "assistant",

                    type: "judgment-list",

                    data: data.results

                };

            }

            setMessages(prev =>

                prev.map(msg =>

                    msg.id === loadingId

                        ? assistantMessage

                        : msg

                )

            );

        }

        catch {

            setMessages(prev =>

                prev.map(msg =>

                    msg.id === loadingId

                        ? {

                            id: loadingId,

                            role: "assistant",

                            type: "text",

                            content:
                                "❌ Unable to reach the backend."

                        }

                        : msg

                )

            );

        }

    };

    // ============================================
// Explain Judgment
// ============================================

const explainJudgment = async (citation) => {

    const loadingId = Date.now();

    setMessages(prev => [

        ...prev,

        {

            id: loadingId,

            role: "assistant",

            type: "loading"

        }

    ]);

    try {

        const response = await fetch(

            "http://127.0.0.1:5000/api/explain",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    citation

                })

            }

        );

        const data = await response.json();

      setMessages(prev =>

    prev.map(msg =>

        msg.id === loadingId

            ? {

                id: loadingId,

                role: "assistant",

                type: "explanation",

                citation: data.citation,

                case_number: data.case_number,

                court: data.court,

                judges: data.judges,

                decided_date: data.decided_date,

                source_file: data.source_file,

                content: data.content

            }

            : msg

    )

);

    }

    catch {

        setMessages(prev =>

            prev.map(msg =>

                msg.id === loadingId

                    ? {

                        id: loadingId,

                        role: "assistant",

                        type: "text",

                        content:

                            "❌ Unable to explain this judgment."

                    }

                    : msg

            )

        );

    }

};

// ============================================
// Open Full Judgment
// ============================================

const openJudgment = async (citation) => {

    const loadingId = Date.now();

    setMessages(prev => [

        ...prev,

        {

            id: loadingId,

            role: "assistant",

            type: "loading"

        }

    ]);

    try {

        const response = await fetch(

            "http://127.0.0.1:5000/api/open",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    citation

                })

            }

        );

        const data = await response.json();

        setMessages(prev =>

            prev.map(msg =>

                msg.id === loadingId

                    ? {

                        id: loadingId,

                        role: "assistant",

                        type: "judgment",

                        citation: data.citation,

                        case_number: data.case_number,

                        court: data.court,

                        judges: data.judges,

                        decided_date: data.decided_date,

                        source_file: data.source_file,

                        judgment_text: data.judgment_text

                    }

                    : msg

            )

        );

    }

    catch {

        setMessages(prev =>

            prev.map(msg =>

                msg.id === loadingId

                    ? {

                        id: loadingId,

                        role: "assistant",

                        type: "text",

                        content:

                            "❌ Unable to open this judgment."

                    }

                    : msg

            )

        );

    }

};



// ============================================
// Compare Judgments
// ============================================
const relevanceAnalysis = async (citation) => {

    const loadingId = Date.now();

    setMessages(prev => [

        ...prev,

        {

            id: loadingId,

            role: "assistant",

            type: "loading"

        }

    ]);

    try {

        const response = await fetch(

            "http://127.0.0.1:5000/api/relevance",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    citation

                })

            }

        );

        const data = await response.json();

        setMessages(prev =>

            prev.map(msg =>

                msg.id === loadingId

                    ? {

                        id: loadingId,

                        role: "assistant",

                        type: "relevance",

                        query: data.query,

                        citation: data.citation,

                        case_number: data.case_number,

                        court: data.court,

                        judges: data.judges,

                        decided_date: data.decided_date,

                        source_file: data.source_file,

                        content: data.content

                    }

                    : msg

            )

        );

    }

    catch {

        setMessages(prev =>

            prev.map(msg =>

                msg.id === loadingId

                    ? {

                        id: loadingId,

                        role: "assistant",

                        type: "text",

                        content:

                            "❌ Unable to generate relevance analysis."

                    }

                    : msg

            )

        );

    }

};
    

    return (

        <div className="app">

            <Sidebar />

            <div className="main">

                <Topbar />

               <ChatWindow

                     messages={messages}

                     onExplain={explainJudgment}

                     onOpen={openJudgment}

                     onRelevant={relevanceAnalysis}

                />

                <div ref={bottomRef} />

                <ChatInput

                    onSend={sendMessage}

                />

            </div>

        </div>

    );

}

export default Home;