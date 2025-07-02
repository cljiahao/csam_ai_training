import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import useBaseStore from "@/store/base";
import useTrainStore from "@/store/train";
import { useRetrainDataMutation, useGetModelsMutation } from "../api/model-bar";

const useRetrain = ({ item }) => {
  const queryClient = useQueryClient();
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [isDialogOpen, setDialogOpen] = useState(false);

  const updateError = useBaseStore((state) => state.updateError);
  const { status, updateStatus } = useTrainStore(
    useShallow((state) => ({
      status: state.status,
      updateStatus: state.updateStatus,
    })),
  );

  const { mutateAsync: retrainModel } = useRetrainDataMutation({ updateError });
  const { mutateAsync: getModels } = useGetModelsMutation({ updateError });

  const handleOpenDialog = (open) => {
    if (open) {
      loadModels();
    } else {
      setSelectedModel("");
    }
    setDialogOpen(open);
  };

  const loadModels = () => {
    getModels()
      .then((data) => {
        const itemModels = data.filter((model) => model.item === item);
        setModels(itemModels);
      })
      .catch((err) => {
        updateError(err.message);
      });
  };
  const handleModelSelect = (modelName) => {
    setSelectedModel(modelName);
  };

  const handleStartRetrain = () => {
    if (selectedModel) {
      queryClient.removeQueries();
      setDialogOpen(false);

      retrainModel({ item, ai_model_name: selectedModel }).then((data) =>
        updateStatus(data?.status),
      );
    }
  };

  return {
    state: {
      status,
      selectedModel,
      models,
      isDialogOpen,
    },
    action: {
      handleModelSelect,
      handleStartRetrain,
      handleOpenDialog,
    },
  };
};

export default useRetrain;
