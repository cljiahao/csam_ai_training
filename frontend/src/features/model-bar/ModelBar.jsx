import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { MdCompare } from "react-icons/md";

import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { STATUS } from "@/constants/common";
import { METHOD_PARAMS } from "@/constants/url-params";
import { cn } from "@/lib/utils";
import useAugment from "./hooks/useAugment";
import EvalOutflow from "./subfeatures/eval-outflow/EvalOutflow";
import UtilityPanel from "./subfeatures/utility-panel/UtilityPanel";
import ModelSelectionDialog from "./subfeatures/model-selection/ModelSelectionDialog";

const ModelBar = ({ className, item, method }) => {
  const {
    state: { status },
    action: { handleStartTrain },
  } = useAugment({ item });

  const disableButton = status !== STATUS.IDLE && status !== STATUS.EVALUATED;

  return (
    <div className={cn("flex h-full w-full items-center space-x-4", className)}>
      <UtilityPanel />
      <div className="flex h-full w-full items-center justify-between pl-6 pr-12">
        {method === METHOD_PARAMS.TRAIN ? (
          <HoverButton
            className="w-24 text-lg"
            icon={LiaChalkboardTeacherSolid}
            hoverText="Train"
            onClick={handleStartTrain}
            disabled={disableButton}
          />
        ) : (
          <ModelSelectionDialog
            triggerChildren={
              <HoverButton
                className="w-24 text-lg"
                icon={LiaChalkboardTeacherSolid}
                hoverText="Retrain"
                disabled={disableButton}
              />
            }
            item={item}
          />
        )}
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
