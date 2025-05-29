import { useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import useTrainStore from "@/store/train";
import { startEvaluation } from "@/services/api-ai-model";

const useEvaluationResults = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["evaluateModel"],
    mutationFn: async ({ item, ai_model_name }) =>
      await startEvaluation(item, { ai_model_name }),
    onSuccess: (data) => {
      queryClient.setQueryData(["evaluatedModel"], data);
    },
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["evaluatedModel"]); // Clear cache on error
    },
  });
};

const useEvaluate = ({ updateError, item }) => {
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { data: trainModel } = useQuery({
    queryKey: ["trainedModel"],
  });

  const { mutateAsync: evaluateModel, data: evalResults } =
    useEvaluationResults({ updateError });

  useEffect(() => {
    if (status === "trained") {
      evaluateModel({ item, ai_model_name: trainModel?.ai_model_name }).then(
        (data) => updateStatus(data?.status),
      );
    }
  }, [item, evaluateModel, trainModel, status, updateStatus]);

  return { state: { status, evalResults }, action: {} };
};

export default useEvaluate;
