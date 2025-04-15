import { cn } from "@/lib/utils";
import ModelChart from "./components/ModelChart";
import VerboseAccordion from "./components/VerboseAccordion";
import useGetEpoch from "./hooks/useGetEpoch";
import useBaseStore from "@/store/base";

const ModelTrainer = ({ className, item }) => {
  const updateError = useBaseStore((state) => state.updateError);

  const {
    state: { epochs, status },
  } = useGetEpoch({ updateError, item });

  return (
    <div className={cn("flex h-full w-full flex-col", className)}>
      <div className="h-2/3 p-2 px-4">
        <ModelChart epoch_data={epochs} />
      </div>
      <div className="h-1/3 px-4">
        <VerboseAccordion epoch_data={epochs} status={status} />
      </div>
    </div>
  );
};

ModelTrainer.displayName = "ModelTrainer";

export default ModelTrainer;
