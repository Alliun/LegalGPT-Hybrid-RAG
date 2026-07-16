import ReactMarkdown from "react-markdown";

import JudgmentCard from "../judgment/JudgmentCard";

function MessageBubble({

    message,

    onExplain

}) {

    // ==========================================
    // Loading
    // ==========================================

    if (message.type === "loading") {

        return (

            <div className="assistant-message">

                <div className="message-content loading">

                    LegalGPT is thinking...

                </div>

            </div>

        );

    }

    // ==========================================
    // Judgment List
    // ==========================================

    if (message.type === "judgment-list") {

        return (

            <div className="assistant-message">

                <div className="message-content">

                    <h3>⚖ Relevant Judgments</h3>

                    {

                        message.data.map(judgment => (

                            <JudgmentCard

                                key={judgment.rank}

                                judgment={judgment}

                                onExplain={onExplain}

                            />

                        ))

                    }

                </div>

            </div>

        );

    }

    // ==========================================
    // Explanation Card
    // ==========================================

    if (message.type === "explanation") {

        return (

            <div className="assistant-message">

                <div className="message-content markdown-body">

                    <h2>⚖ Judgment Explanation</h2>

                    <table className="metadata-table">

                        <tbody>

                            <tr>

                                <td><strong>Citation</strong></td>

                                <td>{message.citation}</td>

                            </tr>

                            <tr>

                                <td><strong>Court</strong></td>

                                <td>{message.court}</td>

                            </tr>

                            <tr>

                                <td><strong>Case No.</strong></td>

                                <td>{message.case_number}</td>

                            </tr>

                            <tr>

                                <td><strong>Judge</strong></td>

                                <td>{message.judges}</td>

                            </tr>

                            <tr>

                                <td><strong>Date</strong></td>

                                <td>{message.decided_date}</td>

                            </tr>

                            <tr>

                                <td><strong>Source</strong></td>

                                <td>{message.source_file}</td>

                            </tr>

                        </tbody>

                    </table>

                    <hr />

                    <ReactMarkdown>

                        {message.content}

                    </ReactMarkdown>

                </div>

            </div>

        );

    }

    // ==========================================
    // User Message
    // ==========================================

    if (message.role === "user") {

        return (

            <div className="user-message">

                <div className="message-content">

                    {message.content}

                </div>

            </div>

        );

    }

    // ==========================================
    // Assistant Text
    // ==========================================

    return (

        <div className="assistant-message">

            <div className="message-content markdown-body">

                <ReactMarkdown>

                    {message.content}

                </ReactMarkdown>

            </div>

        </div>

    );

}

export default MessageBubble;