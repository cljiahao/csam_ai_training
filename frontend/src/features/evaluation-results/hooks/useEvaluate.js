import { useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import useTrainStore from "@/store/train";
import { startEvaluation } from "@/services/api_model";

const useEvaluationResults = ({ setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["evaluateModel"],
    mutationFn: async ({ item, modelName }) =>
      await startEvaluation(item, { ai_model_name: modelName }),
    onSuccess: (data) => {
      queryClient.setQueryData(["evaluatedModel"], data);
    },
    onError: (error) => {
      console.log(error.message);
      setError(error.message);
      queryClient.removeQueries(["evaluatedModel"]); // Clear cache on error
    },
  });
};

const useEvaluate = ({ setError, item }) => {
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
    useEvaluationResults({
      setError,
    });

  useEffect(() => {
    if (status === "trained") {
      evaluateModel({ item, modelName: trainModel.ai_model_name }).then(
        (data) => updateStatus(data?.status),
      );
    }
  }, [item, evaluateModel, trainModel, status, updateStatus]);

  return { state: { evalResults }, action: {} };
};

export default useEvaluate;
