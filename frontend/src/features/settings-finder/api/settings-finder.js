import { useMutation, useQueryClient } from "@tanstack/react-query";

import { uploadImage } from "@/services/api-image-settings";
import { SETTINGS_API } from "../constants/query-keys";

export const useSettingsMutation = ({ mode, setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [SETTINGS_API.mutations, mode],
    mutationFn: async ({ item, targetCount, formData }) =>
      await uploadImage(mode, item, targetCount, formData),
    onSuccess: (data) => {
      queryClient.setQueryData([SETTINGS_API.queries, mode], data);
    },
    onError: (error) => {
      setError(error.message);
      queryClient.removeQueries([SETTINGS_API.queries, mode]); // Clear cache on error
    },
  });
};
