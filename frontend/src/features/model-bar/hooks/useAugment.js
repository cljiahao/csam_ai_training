import { useQueryClient } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { STATUS } from "@/constants/common";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { useAugmentMutation } from "../api/model-bar";

const useAugment = ({ item }) => {
  const queryClient = useQueryClient();

  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: augmentData } = useAugmentMutation({ updateError });

  const handleStartTrain = () => {
    queryClient.removeQueries();
    updateStatus(STATUS.AUGMENTING);
    augmentData({ item }).then((data) => updateStatus(data?.status));
  };

  return { state: { status }, action: { handleStartTrain } };
};

export default useAugment;
