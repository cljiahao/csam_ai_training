import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { MdCompare } from "react-icons/md";

import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { STATUS } from "@/constants/common";
import { cn } from "@/lib/utils";
import useAugment from "./hooks/useAugment";
import EvalOutflow from "./subfeatures/eval-outflow/EvalOutflow";
import UtilityPanel from "./subfeatures/utility-panel/UtilityPanel";

const ModelBar = ({ className, item }) => {
  const {
    state: { status },
    action: { handleStartTrain },
  } = useAugment({ item });

  const disableButton = status != STATUS.IDLE && status != STATUS.EVALUATED;

  return (
    <div className={cn("flex h-full w-full items-center space-x-4", className)}>
      <UtilityPanel />
      <div className="hw-full flex-between pl-6 pr-12">
        <HoverButton
          className="w-24 text-lg"
          icon={LiaChalkboardTeacherSolid}
          hoverText="Train"
          onClick={handleStartTrain}
          disabled={disableButton}
        />
        <EvalOutflow
          triggerChildren={
            <HoverButton
              className="w-24 text-lg"
              icon={MdCompare}
              hoverText="Outflows"
              disabled={disableButton}
            />
          }
        />
      </div>
    </div>
  );
};

export default ModelBar;
