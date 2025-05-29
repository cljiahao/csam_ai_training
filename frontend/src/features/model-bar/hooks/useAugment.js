import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { createAugment } from "@/services/api-ai-model";
import useTrainStore from "@/store/train";

const useAugmentMutation = ({ updateError }) => {
  return useMutation({
    mutationKey: ["augment"],
    mutationFn: async ({ item }) => await createAugment(item),
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
    },
  });
};

const useAugment = ({ updateError, item }) => {
  const queryClient = useQueryClient();
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: augmentData } = useAugmentMutation({ updateError });

  const handleStartTrain = () => {
    updateStatus("processing");
    queryClient.removeQueries();
    augmentData({ item }).then((data) => updateStatus(data?.status));
  };

  return { state: { status }, action: { handleStartTrain } };
};

export default useAugment;
