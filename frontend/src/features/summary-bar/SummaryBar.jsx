import { cn } from "@/lib/utils";
import UtilityPanel from "./components/UtilityPanel";
import LabelSwitch from "@/components/widgets/label-switch/LabelSwitch";
import useLabelSwitch from "./hooks/useLabelSwitch";

const SummaryBar = ({ className, method }) => {
  const {
    state: { isChecked },
    action: { onCheckChange },
  } = useLabelSwitch({ method });

  return (
    <div className={cn("flex h-full w-full items-center", className)}>
      <UtilityPanel />
      <LabelSwitch
        labelClassName="text-2xl"
        label={method}
        checked={isChecked}
        onCheckedChange={onCheckChange}
      />
    </div>
  );
};

export default SummaryBar;
