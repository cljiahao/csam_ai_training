import { useMutation, useQueryClient } from "@tanstack/react-query";

import { MUTATION_KEYS, QUERY_KEYS } from "@/constants/api-keys";
import { startTrain } from "@/services/api-ai-model";

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
