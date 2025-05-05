import { useMutation, useQueryClient } from "@tanstack/react-query";

import { MARKERS } from "@/core/constants";
import { uploadImage } from "@/services/api_settings";

const useSettingsMutation = ({ mode, setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["imageProcess", mode],
    mutationFn: async ({ mode, item, targetCount, formData }) =>
      await uploadImage(mode, item, targetCount, formData),
    onSuccess: (data) => {
      queryClient.setQueryData(["processedSettings", mode], data);
    },
    onError: (error) => {
      console.log(error.message);
      setError(error.message);
      queryClient.removeQueries(["processedSettings", mode]); // Clear cache on error
    },
  });
};

const useSettingsFinder = ({ mode, setError }) => {
  const { mutate: processImage } = useSettingsMutation({ mode, setError });

  const handleImageProcess = (mode, item, targetCount, file, addMark) => {
    const formData = new FormData();
    formData.append("file", file);
    processImage(
      { mode, item, targetCount, formData },
      {
        onSuccess: (data) => {
          console.log(data);
          if (data) {
            data?.coordinates.map((_, index) => {
              addMark(index, MARKERS.static);
            });
          }
        },
      },
    );
  };

  return {
    state: {},
    action: { handleImageProcess },
  };
};

export default useSettingsFinder;
