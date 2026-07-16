import {
    ShieldCheck,
    Cpu,
    Search
} from "lucide-react";

import "../../styles/topbar.css";

function Topbar() {

    return (

        <header className="topbar">

            <div>

                <h1>

                    LegalGPT

                </h1>

                <p>

                    AI-powered Legal Research Assistant

                </p>

            </div>

            <div className="topbar-right">

                <div className="status-card">

                    <Search size={18}/>

                    Hybrid Search

                </div>

                <div className="status-card">

                    <Cpu size={18}/>

                    Llama 3

                </div>

                <div className="status-card online">

                    <ShieldCheck size={18}/>

                    Online

                </div>

            </div>

        </header>

    );

}

export default Topbar;