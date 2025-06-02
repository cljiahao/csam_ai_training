import { cn } from "@/lib/utils";
import Loading from "@/components/static/loading";
import { STATUS } from "@/constants/common";
import ConfusionMatrix from "./components/ConfusionMatrix";
import useEvaluate from "./hooks/useEvaluate";

const EvaluationResults = ({ className, item }) => {
  const {
    state: { status, evalResults },
  } = useEvaluate({ item });

  if (status != STATUS.IDLE && status != STATUS.EVALUATED)
    return <Loading className={className} />;

  return (
    <div className={cn("grid h-full w-full grid-rows-3 gap-2", className)}>
      {evalResults?.results.map((evalResult) => (
        <ConfusionMatrix key={evalResult.mode} evalResult={evalResult} />
      ))}
    </div>
  );
};

export default EvaluationResults;
