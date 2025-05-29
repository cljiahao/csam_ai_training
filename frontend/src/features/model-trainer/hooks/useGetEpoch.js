import { useEffect } from "react";
import { useShallow } from "zustand/react/shallow";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import useTrainStore from "@/store/train";
import { getEpoch, startTrain } from "@/services/api-ai-model";

const useTrainDataMutation = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["trainData"],
    mutationFn: async ({ item }) => await startTrain(item),
    onSuccess: (data) => {
      queryClient.setQueryData(["trainedModel"], data);
    },
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["trainedModel"]); // Clear cache on error
    },
  });
};

const useGetEpoch = ({ updateError, item }) => {
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: trainData } = useTrainDataMutation({ updateError });
  const { data: epochs } = useQuery({
    queryKey: ["getEpoch"],
    queryFn: async () => await getEpoch(item),
    enabled: status === "training",
    staleTime: 0,
    refetchInterval: status === "training" ? 5000 : false,
  });

  useEffect(() => {
    if (status === "augmented") {
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
