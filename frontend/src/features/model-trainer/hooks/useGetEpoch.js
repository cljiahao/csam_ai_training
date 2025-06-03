import { useEffect } from "react";
import { useShallow } from "zustand/react/shallow";

import { STATUS } from "@/constants/common";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { useQueryEpochs, useTrainDataMutation } from "../api/model-trainer";

const useGetEpoch = ({ item }) => {
  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: trainData } = useTrainDataMutation({ updateError });

  const epochs = useQueryEpochs(item, status === STATUS.TRAINING);

  useEffect(() => {
    if (status === STATUS.AUGMENTED) {
      trainData({ item }).then((data) => {
        updateStatus(data?.status);
      });
    }
  }, [item, trainData, status, updateStatus]);

  useEffect(() => {
    if (epochs?.length > 0) {
      updateStatus(epochs.at(-1)?.status);
    }
  }, [epochs, updateStatus]);

  return { state: { epochs, status }, action: {} };
};

export default useGetEpoch;
