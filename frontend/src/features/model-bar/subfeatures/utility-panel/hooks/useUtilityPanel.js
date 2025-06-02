import { useState } from "react";
import useModelInstaller from "./useModelInstaller";

const useUtilityPanel = () => {
  const [isOpen, setIsOpen] = useState(false);

  const {
    action: { getModels },
  } = useModelInstaller();

  const onOpenChange = () => {
    getModels();
    setIsOpen((state) => !state);
  };

  return {
    state: { isOpen },
    action: { onOpenChange },
  };
};

export default useUtilityPanel;
