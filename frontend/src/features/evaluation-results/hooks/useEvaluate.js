import { useEffect } from "react";
import { useShallow } from "zustand/react/shallow";

import { STATUS } from "@/constants/common";
import { METHOD_PARAMS } from "@/constants/url-params";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import {
  useEvaluationResults,
  useQueryTrainModel,
  useQueryRetrainModel,
} from "../api/evaluation-results";

const useEvaluate = ({ item, method }) => {
  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const trainModel = useQueryTrainModel();
  const retrainModel = useQueryRetrainModel();
  const modelData =
    method === METHOD_PARAMS.RETRAIN ? retrainModel : trainModel;

  const { mutateAsync: evaluateModel, data: evalResults } =
    useEvaluationResults({ updateError });

  useEffect(() => {
    // Trigger evaluation when the model has been trained or retrained
    if (
      (status === STATUS.TRAINED && method === METHOD_PARAMS.TRAIN) ||
      (status === STATUS.RETRAINED && method === METHOD_PARAMS.RETRAIN)
    ) {
      if (modelData?.ai_model_name) {
        evaluateModel({ item, ai_model_name: modelData.ai_model_name }).then(
          (data) => updateStatus(data?.status),
        );
      } else {
        console.warn("No model name available for evaluation");
        updateStatus(STATUS.IDLE);
      }
    }
  }, [item, evaluateModel, modelData, status, updateStatus, method]);
  return { state: { status, evalResults }, action: {} };
};

export default useEvaluate;
