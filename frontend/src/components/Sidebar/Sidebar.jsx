import {
    Plus,
    MessageSquare,
    Database,
    BrainCircuit,
    Scale
} from "lucide-react";

import "../../styles/sidebar.css";

function Sidebar() {

    const history = [

        "Divorce Law",

        "Property Dispute",

        "Labour Law",

        "Cheque Bounce",

        "Consumer Complaint"

    ];

    return (

        <aside className="sidebar">

            {/* Logo */}

            <div className="sidebar-header">

                <div className="logo-box">

                    <Scale size={28} />

                </div>

                <div>

                    <h2>LegalGPT</h2>

                    <p>Hybrid Legal AI</p>

                </div>

            </div>

            {/* New Chat */}

            <button className="new-chat-btn">

                <Plus size={18} />

                New Chat

            </button>

            {/* History */}

            <div className="sidebar-history">

                <div className="sidebar-title">

                    Recent Conversations

                </div>

                {

                    history.map((item,index)=>(

                        <div

                            key={index}

                            className="history-card"

                        >

                            <MessageSquare size={16}/>

                            <span>{item}</span>

                        </div>

                    ))

                }

            </div>

            {/* Footer */}

            <div className="sidebar-footer">

                <div className="footer-item">

                    <Database size={16}/>

                    Elasticsearch

                </div>

                <div className="footer-item">

                    <BrainCircuit size={16}/>

                    Hybrid RAG

                </div>

            </div>

        </aside>

    );

}

export default Sidebar;