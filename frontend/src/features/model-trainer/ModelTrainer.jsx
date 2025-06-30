import { cn } from "@/lib/utils";
import ModelChart from "./components/ModelChart";
import VerboseAccordion from "./components/VerboseAccordion";
import useGetEpoch from "./hooks/useGetEpoch";

const ModelTrainer = ({ className, item, method }) => {
  const {
    state: { epochs, status },
  } = useGetEpoch({ item, method });

  return (
    <div className={cn("flex h-full w-full flex-col px-4", className)}>
      <div className="h-2/3 py-2">
        <ModelChart epoch_data={epochs} />
      </div>
      <div className="h-1/3">
        <VerboseAccordion epoch_data={epochs} status={status} />
      </div>
    </div>
  );
};

export default ModelTrainer;
