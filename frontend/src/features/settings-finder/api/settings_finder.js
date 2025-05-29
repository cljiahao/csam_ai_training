import { uploadImage } from "@/services/api_settings";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export const useSettingsMutation = ({ setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["imageProcess"],
    mutationFn: async ({ mode, item, targetCount, formData }) =>
      await uploadImage(mode, item, targetCount, formData),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(["processedSettings", variables.mode], data);
    },
    onError: (error, variables) => {
      setError(error.message);
      queryClient.removeQueries(["processedSettings", variables.mode]); // Clear cache on error
    },
  });
};
