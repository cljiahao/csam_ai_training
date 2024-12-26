import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import SeoHead from "@/components/SeoHead";
import { Home } from "@/pages";
import { navigation_info } from "@/core/navigation";

const element_info = {
  Home: <Home />,
};

function App() {
  return (
    <Router>
      <Routes>
        {navigation_info.map((info) => (
          <Route
            key={info.name}
            path={info.url}
            element={
              <>
                <SeoHead title={info.title} />
                {element_info[info.name]}
              </>
            }
          />
        ))}
      </Routes>
    </Router>
  );
}

export default App;
