import { createElement, Suspense, lazy } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

import { navigation_info } from "@/core/navigation";
import Loading from "./components/static/loading";
import SeoHead from "./components/layouts/SeoHead";
import { resetStore } from "./store/resetStore";
import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";

const element_info = {
  Home: lazy(() => import("@/pages/home")),
  CDS: lazy(() => import("@/pages/csamds")),
  CMT: lazy(() => import("@/pages/csammt")),
  Settings: lazy(() => import("@/pages/settings")),
};

function App() {
  return (
    <Router>
      <SubApp />
    </Router>
  );
}

function SubApp() {
  const location = useLocation();
  const queryClient = useQueryClient();

  useEffect(() => {
    // Reset all global stores when route changes
    resetStore();
    queryClient.removeQueries();
  }, [location.pathname, queryClient]); // Re-run on pathname change

  return (
    <Routes>
      {navigation_info.map((info) => (
        <Route
          key={info.name}
          path={info.url}
          element={
            <Suspense fallback={<Loading className="h-screen" />}>
              <SeoHead title={info.title} />
              {createElement(element_info[info.name])}
            </Suspense>
          }
        />
      ))}
    </Routes>
  );
}

export default App;
