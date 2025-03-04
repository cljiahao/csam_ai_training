import { cn } from "@/lib/utils";
import ItemForm from "./components/ItemForm";
import UtilityPanel from "./components/UtilityPanel";

const SettingsBar = ({ className }) => {
  return (
    <div className={cn("flex h-full w-full items-center space-x-4", className)}>
      <UtilityPanel />
      <ItemForm />
    </div>
  );
};

export default SettingsBar;
