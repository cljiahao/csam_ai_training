import NavSheet from "@/components/widgets/nav-sheet/NavSheet";

import { navigation_info } from "@/core/navigation";

const UtilityPanel = ({ children }) => {
  return (
    <div className="flex-center h-full px-2">
      <NavSheet nav_info={navigation_info}>{children}</NavSheet>
    </div>
  );
};

export default UtilityPanel;
