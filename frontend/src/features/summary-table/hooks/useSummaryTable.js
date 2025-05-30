import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { getSummaryData } from "@/services/api-data-summary";
import { QUERY_KEYS } from "@/constants/api-keys";

const useSummaryTable = (mode) => {
  const { data: dataTable } = useQuery({
    queryKey: [QUERY_KEYS.API_DATATABLE, mode],
    queryFn: async () => await getSummaryData(mode),
    enabled: true,
    staleTime: 0,
    refetchInterval: 10000,
  });

  const navigate = useNavigate();
  return { state: { dataTable }, action: { navigate } };
};

export default useSummaryTable;
