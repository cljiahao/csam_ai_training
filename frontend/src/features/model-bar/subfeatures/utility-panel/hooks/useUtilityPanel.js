import { useState } from "react";

import useBaseStore from "@/store/base";
import { useGetModelsMutation } from "@/features/model-bar/api/model-bar";

const useUtilityPanel = () => {
  const [isOpen, setIsOpen] = useState(false);
  const updateError = useBaseStore((state) => state.updateError);

  const { mutateAsync: getModels } = useGetModelsMutation({ updateError });

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
