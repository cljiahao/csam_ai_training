import { HelmetProvider } from "react-helmet-async";
import { DisplayContext, ImageDetailsContext } from "@/contexts/context";
import { useDisplay } from "@/hooks/useDisplay";
import { useImageDetails } from "@/hooks/useImageDetails";

export const AppProvider = ({ children }) => {
  const stateDisplay = useDisplay();
  const stateImageDetails = useImageDetails();

  return (
    <HelmetProvider>
      <DisplayContext.Provider value={stateDisplay}>
        <ImageDetailsContext.Provider value={stateImageDetails}>
          {children}
        </ImageDetailsContext.Provider>
      </DisplayContext.Provider>
    </HelmetProvider>
  );
};
