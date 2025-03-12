import { LiaChalkboardTeacherSolid } from "react-icons/lia";

import HoverButton from "@/components/widgets/hover-button/HoverButton";
import EvalOutflow from "./EvalOutflow";

const ModelButtons = ({ onTrain, disabled }) => {
  return (
    <div className="hw-full flex-between pl-6 pr-12">
      <HoverButton
        className="w-24 text-lg"
        icon={LiaChalkboardTeacherSolid}
        hoverText="Train"
        onClick={onTrain}
        disabled={disabled}
      />
      <EvalOutflow disabled={disabled} />
    </div>
  );
};

export default ModelButtons;
