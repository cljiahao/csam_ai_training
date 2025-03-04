import { cn } from "@/lib/utils";
import { HelmetProvider } from "react-helmet-async";
import { Toaster } from "../ui/toaster";

const BaseLayout = ({ className, children }) => {
  return (
    <HelmetProvider>
      <main
        className={cn(
          "flex h-screen max-h-screen w-screen overflow-hidden",
          className,
        )}
      >
        {children}
      </main>
      <Toaster />
    </HelmetProvider>
  );
};

export default BaseLayout;
