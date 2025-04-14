import { useQuery } from "@tanstack/react-query";
import { FaCheck } from "react-icons/fa";
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

  const ModelButton = ({ value, ...props }) => {
    return (
      <Button
        type="button"
        variant="outline"
        role="combobox"
        className={cn(
          "w-[200px] justify-between",
          !value && "text-muted-foreground",
        )}
        {...props}
      >
        {value
          ? allModels.find((model) => model.file_name === value).file_name
          : "Select Model to install"}
        <HiChevronUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
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
              <CommandItem
                value={model.file_name}
                key={model.file_name}
                onSelect={() => {
                  modelForm.setValue("file_name", model.file_name);
                  modelForm.setValue("item", model.item);
                }}
              >
                {model.file_name}
                <FaCheck
                  className={cn(
                    "ml-auto",
                    model.file_name === value ? "opacity-100" : "opacity-0",
                  )}
                />
              </CommandItem>
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
          className="flex-center space-x-8 py-3"
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
