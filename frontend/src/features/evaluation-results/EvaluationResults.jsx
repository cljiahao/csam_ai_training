import { cn } from "@/lib/utils";
import ConfusionMatrix from "./components/ConfusionMatrix";
import useEvaluate from "./hooks/useEvaluate";
import useBaseStore from "@/store/base";
import Loading from "@/components/static/loading";

const EvaluationResults = ({ className, item }) => {
  const updateError = useBaseStore((state) => state.updateError);

  const {
    state: { status, evalResults },
  } = useEvaluate({ updateError, item });

  if (status != "idle" && status != "evaluated")
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
