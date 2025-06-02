import { Card, CardContent } from "@/components/ui/card";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { cn } from "@/lib/utils";

const ConfusionMatrix = ({ evalResult = {} }) => {
  const capitalize = (str) => str?.charAt(0).toUpperCase() + str?.slice(1);
  const percentage = (value, total) =>
    total === 0
      ? "0.00%"
      : total
        ? `${((value / total) * 100).toFixed(2)}%`
        : "N/A";

  const { mode, total_count, cm_results } = evalResult;

  console.log(total_count);

  return (
    <Card className="flex-center h-full w-full">
      <CardContent className="grid h-full w-full grid-cols-12 grid-rows-6 gap-2 p-2">
        {/* Evaluation Mode Title */}
        <div className="flex-center col-span-4 row-span-2 text-xl font-bold underline">
          {capitalize(mode)}
        </div>

        {/* Predicted Headers */}
        <div className="col-span-8 row-span-2 grid grid-cols-2">
          <div className="flex-center col-span-2 text-sm underline">
            Predicted
          </div>
          <div className="flex-center text-sm">NG</div>
          <div className="flex-center text-sm">Good</div>
        </div>

        {/* Actual Headers */}
        <div className="col-span-5 row-span-4 grid grid-cols-3">
          <div className="flex-center row-span-2 -rotate-90 text-sm underline">
            Actual
          </div>
          <div className="flex-center col-span-2 text-sm">NG</div>
          <div className="flex-center col-span-2 text-sm">Good</div>
        </div>

        {/* Confusion Matrix Results */}
        <div className="group col-span-7 row-span-4 grid grid-cols-2">
          {Object.entries(cm_results).map(([key, value]) => (
            <HoverButton
              key={key}
              className={cn(
                "flex-center hw-full rounded-xl border-2 border-gray-200 text-lg",
                key.includes("false_neg")
                  ? value
                    ? "bg-red-500 hover:bg-red-400"
                    : "bg-green-500 backdrop:hover:bg-green-400"
                  : "",
              )}
              text={percentage(value, total_count)}
              hoverText={value}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default ConfusionMatrix;
