import { useQuery } from "@tanstack/react-query";
import { FaCheck } from "react-icons/fa";
import { IoTrashBin } from "react-icons/io5";
import { HiChevronUpDown } from "react-icons/hi2";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Form } from "@/components/ui/form";
import { cn } from "@/lib/utils";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import useModelFormValidate from "../hooks/useModelFormValidate";
import useBaseStore from "@/store/base";
import useModelServices from "../hooks/useModelServices";
import Swal from "sweetalert2";
import { deleteModel } from "@/services/api_model";

const ModelInstaller = () => {
  const { data: allModels = [] } = useQuery({
    queryKey: ["allModels"],
  });

  const updateError = useBaseStore((state) => state.updateError);

  const {
    action: { installModel },
  } = useModelServices({ updateError });

  const {
    state: { modelFormInfo },
    action: { modelForm },
  } = useModelFormValidate();

  function onSubmit(data) {
    const itemModel = allModels.find(
      (model) => model.file_name === data.file_name,
    );
    installModel({ ...itemModel })
      .then(() =>
        Swal.fire({
          title: "Model Sent!",
          text: "Model Successful Installed into Server.",
          icon: "success",
        }),
      )
      .catch((error) => updateError(error));
  }

  function onModelDelete(item, file_name) {
    Swal.fire({
      title: `Delete ${file_name} from ${item} system?`,
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, delete it!",
      customClass: {
        popup: "pointer-events-auto",
      },
    }).then((result) => {
      if (result.isConfirmed) {
        deleteModel(item, file_name)
          .then(() =>
            Swal.fire({
              title: "Deleted!",
              text: "Your file has been deleted.",
              icon: "success",
            }),
          )
          .catch((error) => updateError(error));
      }
    });
  }

  const ModelButton = ({ value, ...props }) => {
    return (
      <Button
        type="button"
        variant="outline"
        role="combobox"
        className={cn(
          "flex-between w-[250px] px-2",
          !value && "text-muted-foreground",
        )}
        {...props}
      >
        <span className="overflow-hidden">
          {value
            ? allModels.find((model) => model.file_name === value).file_name
            : "Select Model to install"}
        </span>
        <HiChevronUpDown className="h-4 w-4 opacity-50" />
      </Button>
    );
  };
  const ModelSelector = ({ value }) => {
    return (
      <Command>
        <CommandInput placeholder="Search Model Name..." />
        <CommandList>
          <CommandEmpty>No Model found.</CommandEmpty>
          <CommandGroup>
            {allModels.map((model) => (
              <div key={model.file_name} className="flex-center gap-2">
                <CommandItem
                  value={model.file_name}
                  onSelect={() => {
                    modelForm.setValue("file_name", model.file_name);
                    modelForm.setValue("item", model.item);
                  }}
                >
                  <FaCheck
                    className={cn(
                      "ml-auto",
                      model.file_name === value ? "opacity-100" : "opacity-0",
                    )}
                  />
                  {model.file_name}
                </CommandItem>
                <IoTrashBin
                  onClick={() => onModelDelete(model.item, model.file_name)}
                />
              </div>
            ))}
          </CommandGroup>
        </CommandList>
      </Command>
    );
  };

  return (
    <div>
      <Form {...modelForm}>
        <form
          onSubmit={modelForm.handleSubmit(onSubmit)}
          className="flex-center space-x-4 py-3"
        >
          {Object.keys(modelFormInfo).map((key) => {
            return (
              <CustomFormField
                control={modelForm.control}
                key={key}
                name={key}
                popoverTrigger={<ModelButton />}
              >
                <ModelSelector />
              </CustomFormField>
            );
          })}
          <HoverButton className="h-12 w-16" type="submit" hoverText="Submit" />
        </form>
      </Form>
    </div>
  );
};

export default ModelInstaller;
