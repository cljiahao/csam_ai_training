import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { QUERY_KEYS } from "@/constants/api-keys";
import { STATUS } from "@/constants/common";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { useEvaluationResults } from "../api/evaluation-results";

const useEvaluate = ({ item }) => {
  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { data: trainModel } = useQuery({
    queryKey: [QUERY_KEYS.API_TRAIN],
  });

  const { mutateAsync: evaluateModel, data: evalResults } =
    useEvaluationResults({ updateError });

  useEffect(() => {
    if (status === STATUS.TRAINED) {
      evaluateModel({ item, ai_model_name: trainModel?.ai_model_name }).then(
        (data) => updateStatus(data?.status),
      );
    }
  }, [item, evaluateModel, trainModel, status, updateStatus]);

  return { state: { status, evalResults }, action: {} };
};

export default useEvaluate;
