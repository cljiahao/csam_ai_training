import { useMutation, useQueryClient } from "@tanstack/react-query";

import { MUTATION_KEYS, QUERY_KEYS } from "@/constants/api-keys";
import { startEvaluation } from "@/services/api-ai-model";

export const useEvaluationResults = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.API_EVALUATE],
    mutationFn: async ({ item, ai_model_name }) =>
      await startEvaluation(item, { ai_model_name }),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.API_EVALUATE], data);
    },
    onError: (error) => {
      updateError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_EVALUATE]); // Clear cache on error
    },
  });
};
