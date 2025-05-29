import { useState } from "react";

import { navigation_info } from "@/constants/navigation";
import NavSheet from "@/components/widgets/nav-sheet/NavSheet";
import ModelInstaller from "./ModelInstaller";
import useModelServices from "../hooks/useModelServices";
import useBaseStore from "@/store/base";

const UtilityPanel = () => {
  const [isOpen, setIsOpen] = useState(false);

  const setError = useBaseStore((state) => state.setError);

  const {
    action: { getModels },
  } = useModelServices({ setError });

  return (
    <div className="flex-center h-full px-2">
      <NavSheet
        nav_info={navigation_info.filter(
          (nav) => nav.name.toLowerCase() != "cmt",
        )}
        open={isOpen}
        onOpenChange={() => {
          getModels();
          setIsOpen(!isOpen);
        }}
      >
        <ModelInstaller />
      </NavSheet>
    </div>
  );
};

export default UtilityPanel;
