import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { STATUS } from "@/constants/common";
import { QUERY_KEYS } from "@/constants/api-keys";
import {
  createAugment,
  getAllModels,
  installModel,
} from "@/services/api-ai-model";

export const useAugmentMutation = ({ updateError }) => {
  return useMutation({
    mutationKey: [STATUS.AUGMENTING],
    mutationFn: async ({ item }) => await createAugment(item),
    onError: (error) => {
      updateError(error.message);
    },
  });
};

export const useGetModelsMutation = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => await getAllModels(),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.API_MODELS], data);
    },
    onError: (error) => {
      updateError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_MODELS]); // Clear cache on error
    },
  });
};

export const useInstallModelMutation = ({ updateError }) => {
  return useMutation({
    mutationFn: async ({ item, file_name }) =>
      await installModel(item, file_name),
    onError: (error) => {
      updateError(error.message);
    },
  });
};

export const useQueryEvalResults = () => {
  const { data: evalResults } = useQuery({
    queryKey: [QUERY_KEYS.API_EVALUATE],
  });
  return evalResults;
};

export const useQueryAllModels = () => {
  const { data: allModels = [] } = useQuery({
    queryKey: [QUERY_KEYS.API_MODELS],
  });
  return allModels;
};
