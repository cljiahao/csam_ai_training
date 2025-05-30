import NavSheet from "@/components/widgets/nav-sheet/NavSheet";
import { navigation_info } from "@/constants/navigation";
import ItemSettings from "./components/ItemSettings";

const UtilityPanel = () => {
  return (
    <NavSheet
      nav_info={navigation_info.filter(
        (nav) => nav.name.toLowerCase() != "cmt",
      )}
    >
      <div className="hw-full flex-center">
        <ItemSettings />
      </div>
    </NavSheet>
  );
};

export default UtilityPanel;
