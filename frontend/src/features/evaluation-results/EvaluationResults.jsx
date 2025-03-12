import { useState } from "react";

import { cn } from "@/lib/utils";
import ConfusionMatrix from "./components/ConfusionMatrix";
import useEvaluate from "./hooks/useEvaluate";

const EvaluationResults = ({ className, item }) => {
  const [error, setError] = useState("");

  const {
    state: { evalResults },
  } = useEvaluate({ setError, item });

  // TODO
  console.log(error);

  return (
    <div className={cn("grid h-full w-full grid-rows-3 gap-2", className)}>
      {evalResults?.results.map((evalResult) => (
        <ConfusionMatrix key={evalResult.mode} evalResult={evalResult} />
      ))}
    </div>
  );
};

export default EvaluationResults;
