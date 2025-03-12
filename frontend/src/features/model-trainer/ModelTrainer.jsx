import { useState } from "react";

import { cn } from "@/lib/utils";
import ModelChart from "./components/ModelChart";
import VerboseAccordion from "./components/VerboseAccordion";
import useGetEpoch from "./hooks/useGetEpoch";

const ModelTrainer = ({ className, item }) => {
  const [error, setError] = useState("");

  const {
    state: { epochs, status },
  } = useGetEpoch({ setError, item });

  //TODO
  console.log(error);

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
