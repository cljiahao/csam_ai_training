import { useMutation, useQueryClient } from "@tanstack/react-query";

import { uploadImage } from "@/services/api-image-settings";
import { QUERY_KEYS, MUTATION_KEYS } from "@/constants/api-keys";

export const useSettingsMutation = ({ mode, setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.API_SETTINGS, mode],
    mutationFn: async ({ mode, item, targetCount, formData }) =>
      await uploadImage(mode, item, targetCount, formData),
    onSuccess: (data, variables) => {
      queryClient.setQueryData([QUERY_KEYS.API_SETTINGS, variables.mode], data);
    },
    onError: (error, variables) => {
      setError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_SETTINGS, variables.mode]); // Clear cache on error
    },
  });
};
