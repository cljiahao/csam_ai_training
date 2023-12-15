import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import Main from "./pages/Main/Main";
import CDA from "./pages/CDA/CDA";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/CDA" element={<CDA />} />
      </Routes>
    </Router>
  );
}

export default App;
