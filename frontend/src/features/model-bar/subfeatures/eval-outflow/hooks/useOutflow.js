import { useState } from "react";

import { useQueryEvalResults } from "@/features/model-bar/api/model-bar";

const useOutflow = () => {
  const [isDialogOpen, setDialogOpen] = useState();

  const evalResults = useQueryEvalResults();

  const handleDialogOpen = () => {
    setDialogOpen((state) => !state);
  };

  return { state: { isDialogOpen, evalResults }, action: { handleDialogOpen } };
};

export default useOutflow;
