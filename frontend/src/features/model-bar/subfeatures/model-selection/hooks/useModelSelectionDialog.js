import { useState } from "react";
import useBaseStore from "@/store/base";
import { useGetModelsMutation } from "@/features/model-bar/api/model-bar";

const useModelSelectionDialog = (item, onModelSelect) => {
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [selectedModel, setSelectedModel] = useState("");
  const [models, setModels] = useState([]);

  const updateError = useBaseStore((state) => state.updateError);
  const { mutateAsync: getModels } = useGetModelsMutation({ updateError });

  const handleDialogOpen = (open) => {
    // If the dialog is being opened (or was just opened)
    if (open) {
      getModels().then((data) => {
        // Filter models for the current item only
        const itemModels = data.filter((model) => model.item === item);
        setModels(itemModels);
      });
    } else {
      // If the dialog is being closed, reset selected model
      setSelectedModel("");
    }
    setDialogOpen(open);
  };

  const handleRetrain = () => {
    if (selectedModel) {
      onModelSelect(selectedModel);
      setDialogOpen(false);
    }
  };

  return {
    state: {
      isDialogOpen,
      selectedModel,
      models,
    },
    actions: {
      handleDialogOpen,
      setSelectedModel,
      handleRetrain,
    },
  };
};

export default useModelSelectionDialog;
