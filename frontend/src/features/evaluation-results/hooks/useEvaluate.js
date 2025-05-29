import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import useTrainStore from "@/store/train";
import { useEvaluationResults } from "../api/evaluation-results";

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
