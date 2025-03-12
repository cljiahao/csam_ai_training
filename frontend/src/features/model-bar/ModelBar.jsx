import { useState } from "react";

import { cn } from "@/lib/utils";
import UtilityPanel from "./components/UtilityPanel";
import ModelButtons from "./components/ModelButtons";
import useAugment from "./hooks/useAugment";

const ModelBar = ({ className, item }) => {
  const [error, setError] = useState("");

  const {
    state: { status },
    action: { handleStartTrain },
  } = useAugment({ setError, item });

  //TODO
  console.log(error);

  return (
    <div className={cn("flex h-full w-full items-center space-x-4", className)}>
      <UtilityPanel />
      <ModelButtons
        onTrain={handleStartTrain}
        disabled={status !== "idle" && status !== "evaluated"}
      />
    </div>
  );
};

export default ModelBar;
