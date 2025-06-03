import { cn } from "@/lib/utils";
import UtilityPanel from "./subfeatures/utility-panel/UtilityPanel";
import LabelSwitch from "@/components/widgets/label-switch/LabelSwitch";
import useUtilityPanel from "./subfeatures/utility-panel/hooks/useUtilityPanel";

const SummaryBar = ({ className, method }) => {
  const {
    state: { isChecked },
    action: { onCheckChange },
  } = useUtilityPanel({ method });

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
