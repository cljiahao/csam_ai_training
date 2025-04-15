import { cn } from "@/lib/utils";
import UtilityPanel from "./components/UtilityPanel";
import ModelButtons from "./components/ModelButtons";
import useAugment from "./hooks/useAugment";
import useBaseStore from "@/store/base";

const ModelBar = ({ className, item }) => {
  const updateError = useBaseStore((state) => state.updateError);

  const {
    state: { status },
    action: { handleStartTrain },
  } = useAugment({ updateError, item });

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
