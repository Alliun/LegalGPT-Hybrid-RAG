import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App.jsx";

import "./styles/globals.css";
import "./styles/layout.css";
import "./styles/sidebar.css";
import "./styles/topbar.css";
import "./styles/chat.css";
import "./styles/input.css";
import "./styles/judgment.css";
import "./styles/markdown.css";

ReactDOM.createRoot(document.getElementById("root")).render(

    <React.StrictMode>

        <App />

    </React.StrictMode>

);