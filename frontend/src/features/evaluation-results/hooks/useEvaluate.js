import { useEffect } from "react";
import { useShallow } from "zustand/react/shallow";

import { STATUS } from "@/constants/common";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import {
  useEvaluationResults,
  useQueryTrainModel,
} from "../api/evaluation-results";

const useEvaluate = ({ item }) => {
  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const trainModel = useQueryTrainModel();

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
