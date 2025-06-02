import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { QUERY_KEYS } from "@/constants/api-keys";

const useOutflow = () => {
  const [isDialogOpen, setDialogOpen] = useState();

  const { data: evalResults } = useQuery({
    queryKey: [QUERY_KEYS.API_EVALUATE],
  });

  const handleDialogOpen = () => {
    setDialogOpen((prevState) => !prevState);
  };

  return { state: { isDialogOpen, evalResults }, action: { handleDialogOpen } };
};

export default useOutflow;
