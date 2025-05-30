import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { getSummaryData } from "@/services/api-data-summary";

const useSummaryTable = (mode) => {
  const { data: dataTable } = useQuery({
    queryKey: ["dataTable", mode],
    queryFn: async () => await getSummaryData(mode),
    enabled: true,
    staleTime: 0,
    refetchInterval: 10000,
  });

  const navigate = useNavigate();
  return { state: { dataTable }, action: { navigate } };
};

export default useSummaryTable;
