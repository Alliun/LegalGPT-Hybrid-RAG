import { useEffect, useRef, useState } from "react";
import JudgmentList from "../components/judgment/JudgmentList";
import Sidebar from "../components/Sidebar/Sidebar";
import Topbar from "../components/Topbar/Topbar";
import ChatWindow from "../components/Chat/ChatWindow";


function Home() {
    const [judgments, setJudgments] = useState([]);
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

// ========================================
// Simple Text Response
// ========================================

if (data.type === "text") {

    assistantMessage = {

        id: loadingId,

        role: "assistant",

        type: "text",

        content: data.content

    };

}

// ========================================
// Clarification
// ========================================

else if (data.type === "clarification") {

    assistantMessage = {

        id: loadingId,

        role: "assistant",

        type: "text",

        content: data.content

    };

}

// ========================================
// Explanation
// ========================================

else if (data.type === "explanation") {

    assistantMessage = {

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

    };

}

// ========================================
// Judgment Search Results
// ========================================

else if (data.type === "judgment-list") {

    // Update the right sidebar
    setJudgments(data.results || []);

    // Add a conversational response in chat
    assistantMessage = {

        id: loadingId,

        role: "assistant",

        type: "text",

        content: `I found ${data.results.length} relevant judgments.

They are displayed in the right sidebar.

You can ask me to explain one, open the full judgment, or tell you why it is relevant.`

    };

}

// ========================================
// Fallback
// ========================================

else {

    assistantMessage = {

        id: loadingId,

        role: "assistant",

        type: "text",

        content: "Unexpected response from the backend."

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
        console.log(data);

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

        {/* =========================
            Left Sidebar
        ========================= */}

        <aside className="left-sidebar">

            <Sidebar />

        </aside>

        {/* =========================
            Center
        ========================= */}

        <main className="main">

            <Topbar />

            <ChatWindow

                messages={messages}

                onSend={sendMessage}

                onExplain={explainJudgment}

                onOpen={openJudgment}

                onRelevant={relevanceAnalysis}

            />

            <div ref={bottomRef} />

            

        </main>

        {/* =========================
            Right Sidebar
        ========================= */}

        <aside className="right-sidebar">

            <JudgmentList

                judgments={judgments}

                onExplain={explainJudgment}

                onOpen={openJudgment}

                onRelevant={relevanceAnalysis}

            />

        </aside>

    </div>

);

}

export default Home;