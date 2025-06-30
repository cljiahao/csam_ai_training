import { useQueryClient } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { STATUS } from "@/constants/common";
import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { useRetrainDataMutation } from "../api/model-bar";

const useRetrain = ({ item }) => {
  const queryClient = useQueryClient();

  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: retrainModel } = useRetrainDataMutation({ updateError });

  const handleStartRetrain = (modelName) => {
    queryClient.removeQueries();
    retrainModel({ item, ai_model_name: modelName }).then((data) =>
      updateStatus(data?.status),
    );
  };

  return { state: { status }, action: { handleStartRetrain } };
};

export default useRetrain;
