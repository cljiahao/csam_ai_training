import { navigation_info } from "@/constants/navigation";
import NavSheet from "@/components/widgets/nav-sheet/NavSheet";
import ModelInstaller from "./components/ModelInstaller";
import useUtilityPanel from "./hooks/useUtilityPanel";

const UtilityPanel = () => {
  const {
    state: { isOpen },
    action: { onOpenChange },
  } = useUtilityPanel();

  return (
    <div className="flex-center h-full px-2">
      <NavSheet
        nav_info={navigation_info.filter(
          (nav) => nav.name.toLowerCase() != "cmt",
        )}
        open={isOpen}
        onOpenChange={onOpenChange}
      >
        <ModelInstaller />
      </NavSheet>
    </div>
  );
};

export default UtilityPanel;
