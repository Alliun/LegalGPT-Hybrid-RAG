import {
    BookOpen,
    Scale,
    ExternalLink,
    Bookmark
} from "lucide-react";

import "../../styles/judgment.css";

function JudgmentCard({

    judgment,

    onExplain

}) {

    return (

        <div className="judgment-card">

            {/* ==========================
                Header
            ========================== */}

            <div className="judgment-top">

                <div>

                    <div className="judgment-rank">

                        ⚖ Judgment {judgment.rank}

                    </div>

                    <h2 className="citation">

                        {judgment.citation}

                    </h2>

                    <div className="tags">

                        <span>Legal Judgment</span>

                        <span>AI Ranked</span>

                        <span>Hybrid RAG</span>

                    </div>

                </div>

                <div className="match-score">

                    Top Match

                </div>

            </div>

            {/* ==========================
                AI Summary
            ========================== */}

            <div className="summary-box">

                <div className="summary-title">

                    🤖 AI Summary

                </div>

                <p>

                    {judgment.reason}

                </p>

            </div>

            {/* ==========================
                Action Buttons
            ========================== */}

            <div className="judgment-actions">

                <button

                    className="primary"

                    onClick={() => onExplain(judgment.citation)}

                >

                    <BookOpen size={18} />

                    Explain

                </button>

                <button

                    onClick={() => {

                        alert("Compare feature coming soon.");

                    }}

                >

                    <Scale size={18} />

                    Compare

                </button>

                <button

                    onClick={() => {

                        alert("Open full judgment coming soon.");

                    }}

                >

                    <ExternalLink size={18} />

                    Open

                </button>

                <button

                    onClick={() => {

                        alert("Bookmark feature coming soon.");

                    }}

                >

                    <Bookmark size={18} />

                    Save

                </button>

            </div>

        </div>

    );

}

export default JudgmentCard;