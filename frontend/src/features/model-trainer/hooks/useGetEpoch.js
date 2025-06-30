import { useEffect } from "react";
import { useShallow } from "zustand/react/shallow";

import { STATUS } from "@/constants/common";
import { METHOD_PARAMS } from "@/constants/url-params";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { useQueryEpochs, useTrainDataMutation } from "../api/model-trainer";

const useGetEpoch = ({ item, method }) => {
  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: trainData } = useTrainDataMutation({ updateError });

  // Monitor both TRAINING and RETRAINING states
  const isTraining = status === STATUS.TRAINING || status === STATUS.RETRAINING;
  const epochs = useQueryEpochs(method, isTraining);

  useEffect(() => {
    if (status === STATUS.AUGMENTED && method === METHOD_PARAMS.TRAIN) {
      trainData({ item }).then((data) => {
        updateStatus(data?.status);
      });
    }
  }, [item, trainData, status, updateStatus, method]);

  useEffect(() => {
    if (epochs?.length > 0) {
      updateStatus(epochs.at(-1)?.status);
    }
  }, [epochs, updateStatus]);

  return { state: { epochs, status }, action: {} };
};

export default useGetEpoch;
