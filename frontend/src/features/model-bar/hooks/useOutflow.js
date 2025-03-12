import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

const useOutflow = () => {
  const [isDialogOpen, setDialogOpen] = useState();

  const { data: evalResults } = useQuery({
    queryKey: ["evaluatedModel"],
  });

  const handleDialogOpen = () => {
    setDialogOpen((prevState) => !prevState);
  };

  return { state: { isDialogOpen, evalResults }, action: { handleDialogOpen } };
};

export default useOutflow;
