import { useState } from "react";
import useBaseStore from "@/store/base";
import {
  useGetModelsMutation,
  useRetrainDataMutation,
} from "@/features/model-bar/api/model-bar";
import { useQueryClient } from "@tanstack/react-query";
import useTrainStore from "@/store/train";

const useModelSelectionDialog = ({ item }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedModel, setSelectedModel] = useState("");
  const [models, setModels] = useState([]);

  const updateError = useBaseStore((state) => state.updateError);
  const updateStatus = useTrainStore((state) => state.updateStatus);

  const { mutateAsync: getModels } = useGetModelsMutation({ updateError });
  const { mutateAsync: retrainModel } = useRetrainDataMutation({ updateError });
  const queryClient = useQueryClient();

  const startRetrain = () => {
    if (!selectedModel) return;

    queryClient.removeQueries();

    retrainModel({ item, ai_model_name: selectedModel })
      .then((data) => {
        updateStatus(data?.status);
      });

    setIsOpen(false);
  };

  const handleOpenChange = (open) => {
    if (open) {
      loadModels();
    } else {
      setSelectedModel("");
    }
    setIsOpen(open);
  };

  const loadModels = () => {
    getModels().then((data) => {
      const itemModels = data.filter((model) => model.item === item);
      setModels(itemModels);
    });
  };
  return {
    isOpen,
    selectedModel,
    models,
    handleOpenChange,
    setSelectedModel,
    startRetrain,
  };
};

export default useModelSelectionDialog;
