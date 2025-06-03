import { useQuery } from "@tanstack/react-query";

import { QUERY_KEYS } from "@/constants/api-keys";
import { getSummaryData } from "@/services/api-data-summary";

export const useQueryDataTable = (mode) => {
  const { data: dataTable } = useQuery({
    queryKey: [QUERY_KEYS.API_DATATABLE, mode],
    queryFn: async () => await getSummaryData(mode),
    enabled: true,
    staleTime: 0,
    refetchInterval: 10000,
  });
  return dataTable;
};
