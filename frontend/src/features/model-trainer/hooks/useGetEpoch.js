import { useEffect } from "react";
import { useShallow } from "zustand/react/shallow";
import { useQuery } from "@tanstack/react-query";

import useTrainStore from "@/store/train";
import { getEpoch } from "@/services/api-ai-model";
import { useTrainDataMutation } from "../api/model-trainer";
import { QUERY_KEYS } from "@/constants/api-keys";
import { STATUS } from "@/constants/common";

const useGetEpoch = ({ updateError, item }) => {
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: trainData } = useTrainDataMutation({ updateError });

  const { data: epochs } = useQuery({
    queryKey: [QUERY_KEYS.API_EPOCH],
    queryFn: async () => await getEpoch(item),
    enabled: status === STATUS.TRAINING,
    staleTime: 0,
    refetchInterval: status === STATUS.TRAINING ? 5000 : false,
  });

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
