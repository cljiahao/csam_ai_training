import { Card, CardContent } from "@/components/ui/card";
import HoverButton from "@/components/widgets/hover-button/HoverButton";

const ConfusionMatrix = ({ evalResult = {} }) => {
  const capitalize = (str) => str?.charAt(0).toUpperCase() + str?.slice(1);
  const percentage = (value, total) =>
    total === 0
      ? "0.00%"
      : total
        ? `${((value / total) * 100).toFixed(2)}%`
        : "N/A";

  const { mode, total_count, cm_results } = evalResult;

  return (
    <Card className="flex-center h-full w-full">
      <CardContent className="grid h-full w-full grid-cols-12 grid-rows-6 gap-2 p-2">
        {/* Evaluation Mode Title */}
        <div className="flex-center col-span-4 row-span-2 text-xl font-bold underline">
          {capitalize(mode)}
        </div>

        {/* Actual Headers */}
        <div className="col-span-8 row-span-2 grid grid-cols-2">
          <div className="flex-center col-span-2 text-sm underline">Actual</div>
          <div className="flex-center text-sm">NG</div>
          <div className="flex-center text-sm">Good</div>
        </div>

        {/* Predicted Headers */}
        <div className="col-span-5 row-span-4 grid grid-cols-3">
          <div className="flex-center row-span-2 -rotate-90 text-sm underline">
            Predicted
          </div>
          <div className="flex-center col-span-2 text-sm">NG</div>
          <div className="flex-center col-span-2 text-sm">Good</div>
        </div>

        {/* Confusion Matrix Results */}
        <div className="group col-span-7 row-span-4 grid grid-cols-2">
          {Object.entries(cm_results).map(([key, value]) => (
            <HoverButton
              key={key}
              className="flex-center hw-full rounded-xl border-2 border-gray-200 text-lg"
              text={
                key.includes("pos")
                  ? percentage(value, total_count)
                  : percentage(value, total_count)
              }
              hoverText={value}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default ConfusionMatrix;

{
  /* <div className="grid h-full w-full grid-cols-12 grid-rows-6 gap-2">
<div className="flex-center col-span-4 row-span-2 text-xl font-bold underline">
  {capitalize(mode)}
</div>
<div className="flex-center col-span-8 text-sm underline">
  Predicted
</div>
<div className="flex-center col-span-4 text-sm">NG</div>
<div className="flex-center col-span-4 text-sm">Good</div>
<div className="flex-center row-span-4 -rotate-90 text-sm underline">
  Actual
</div>
<div className="flex-center col-span-3 row-span-2 text-sm">NG</div>
<HoverButton
  className="flex-center hw-full col-span-4 row-span-2 rounded-xl border-2 border-gray-200 text-lg"
  text={(real_ng / (real_ng + real_g)) * 100}
  hoverText={real_ng}
/>
<HoverButton
  className="flex-center hw-full col-span-4 row-span-2 rounded-xl border-2 border-gray-200 text-lg"
  text={(real_g / (real_ng + real_g)) * 100}
  hoverText={real_g}
/>
<div className="flex-center col-span-3 row-span-2 text-sm">Good</div>
<HoverButton
  className="flex-center hw-full col-span-4 row-span-2 rounded-xl border-2 border-gray-200 text-lg"
  text={(pred_ng / (real_ng + real_g)) * 100}
  hoverText={pred_ng}
/>
<HoverButton
  className="flex-center hw-full col-span-4 row-span-2 rounded-xl border-2 border-gray-200 text-lg"
  text={(pred_g / (real_ng + real_g)) * 100}
  hoverText={pred_g}
/>
</div> */
}
