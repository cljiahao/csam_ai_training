import { useMutation } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { createAugment } from "@/services/api_model";
import useTrainStore from "@/store/train";

const useAugmentMutation = ({ setError }) => {
  return useMutation({
    mutationKey: ["augment"],
    mutationFn: async ({ item }) => await createAugment(item),
    onError: (error) => {
      console.log(error.message);
      setError(error.message);
    },
  });
};

const useAugment = ({ setError, item }) => {
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: augmentData } = useAugmentMutation({ setError });

  const handleStartTrain = () => {
    updateStatus("processing");
    augmentData({ item }).then((data) => updateStatus(data?.status));
  };

  return { state: { status }, action: { handleStartTrain } };
};

export default useAugment;
