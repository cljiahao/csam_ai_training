import { cn } from "@/lib/utils";
import ItemForm from "./components/ItemForm";
import UtilityPanel from "./subfeatures/utility-panel/UtilityPanel";

const SettingsBar = ({ className }) => {
  return (
    <div className={cn("flex h-full w-full items-center", className)}>
      <UtilityPanel />
      <ItemForm />
    </div>
  );
};

export default SettingsBar;
