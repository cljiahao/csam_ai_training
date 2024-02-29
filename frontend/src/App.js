import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import Main from "./pages/Main/Main";
import CDA from "./pages/CDA/CDA";
import CMT from "./pages/CMT/CMT";
import Settings from "./pages/Settings/Settings";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/CDA" element={<CDA />} />
        <Route path="/CMT" element={<CMT />} />
        <Route path="/Settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;
