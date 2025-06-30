import { FaCheck } from "react-icons/fa";

import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import CustomDialog from "@/components/widgets/custom-dialog/CustomDialog";
import { cn } from "@/lib/utils";
import useModelSelectionDialog from "./hooks/useModelSelectionDialog";
import { Label } from "@/components/ui/label";

const ModelSelectionDialog = ({ item, triggerChildren, onModelSelect }) => {
  const {
    isDialogOpen,
    selectedModel,
    models,
    handleDialogOpen,
    handleModelSelect,
    handleRetrain,
  } = useModelSelectionDialog(item, onModelSelect);

  const ModelButtons = () => {
    return (
      <div className="flex justify-end gap-2">
        <Button variant="outline" onClick={() => handleDialogOpen(false)}>
          Cancel
        </Button>
        <Button onClick={handleRetrain} disabled={!selectedModel}>
          Retrain Model
        </Button>
      </div>
    );
  };

  const ModelSelector = () => {
    return (
      <div className="space-y-2">
        <Label>Available Models</Label>
        <Command className="rounded-lg border shadow-md">
          <CommandInput placeholder="Search models..." />
          <CommandList style={{ maxHeight: "200px" }}>
            <CommandEmpty>No models found for this item.</CommandEmpty>
            <CommandGroup>
              {models.map((model) => (
                <CommandItem
                  key={model.file_name}
                  value={model.file_name}
                  onSelect={() => handleModelSelect(model.file_name)}
                >
                  <FaCheck
                    className={cn(
                      "mr-2 h-4 w-4",
                      model.file_name === selectedModel
                        ? "opacity-100"
                        : "opacity-0",
                    )}
                  />
                  <span className="truncate">{model.file_name}</span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </div>
    );
  };

  return (
    <CustomDialog
      className="h-1/2 w-fit max-w-screen-3xl"
      trigger={triggerChildren}
      title="Select Model to Retrain"
      description="Choose a model from the list below"
      open={isDialogOpen}
      onOpenChange={handleDialogOpen}
    >
      <div className="space-y-6">
        <ModelSelector />
        <ModelButtons />
      </div>
    </CustomDialog>
  );
};

export default ModelSelectionDialog;
