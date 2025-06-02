import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { MUTATION_KEYS, QUERY_KEYS } from "@/constants/api-keys";
import { getEpoch, startTrain } from "@/services/api-ai-model";

export const useTrainDataMutation = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.API_TRAIN],
    mutationFn: async ({ item }) => await startTrain(item),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.API_TRAIN], data);
    },
    onError: (error) => {
      updateError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_TRAIN]); // Clear cache on error
    },
  });
};

export const useQueryEpochs = (item, enabler) => {
  const { data: epochs } = useQuery({
    queryKey: [QUERY_KEYS.API_EPOCH],
    queryFn: async () => await getEpoch(item),
    enabled: enabler,
    staleTime: 0,
    refetchInterval: enabler ? 5000 : false,
  });
  return epochs;
};
