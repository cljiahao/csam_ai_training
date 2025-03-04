import { toast } from "@/hooks/use-toast";
import { useQueryClient } from "@tanstack/react-query";

import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { cn } from "@/lib/utils";
import useSettingsStore from "@/store/settings";
import useUploadFormValidate from "../hooks/useUploadFormValidate";
import useSettingsFinder from "../hooks/useSettingsFinder";
import { useSettingsFinderContext } from "../contexts/SettingsFinderContext";

const UploadForm = ({ className, mode }) => {
  const queryClient = useQueryClient();
  const { item } = useSettingsStore();
  const { setError, setImage, markRef } = useSettingsFinderContext();

  const {
    action: { handleImageProcess },
  } = useSettingsFinder({ mode, setError });

  const {
    state: { ref, uploadFormInfo },
    action: { onSubmit, uploadForm },
  } = useUploadFormValidate();

  const onFileChange = (e) => {
    e.preventDefault();

    const file = e.target.files[0];
    if (file) {
      queryClient.removeQueries();

      const fileName = file.name;
      const targetCount = uploadForm.getValues("quantity");
      setImage(URL.createObjectURL(file));

      toast({
        title: `You submitted the following values for ${mode}:`,
        description: (
          <pre className="mt-2 flex w-[340px] flex-col rounded-md bg-slate-950 p-4">
            <kbd className="text-white">Item Type: {item}</kbd>
            <kbd className="text-white">File Name: {fileName}</kbd>
            <kbd className="text-white">Target Count: {targetCount}</kbd>
          </pre>
        ),
        duration: 2000,
      });

      handleImageProcess(
        mode,
        item,
        targetCount,
        file,
        markRef?.current?.addMark,
      );
    }
  };

  return (
    <div className={cn("h-full w-full py-4", className)}>
      <Form {...uploadForm}>
        <form
          onSubmit={uploadForm.handleSubmit(onSubmit)}
          className="flex-center hw-full space-x-8"
        >
          {Object.keys(uploadFormInfo).map((key) => {
            const { label, placeholder } = uploadFormInfo[key];
            return (
              <CustomFormField
                control={uploadForm.control}
                key={key}
                name={key}
                label={`${mode} ${label}`}
                placeholder={placeholder}
              />
            );
          })}
          <HoverButton
            className="w-18 h-4/5"
            type="submit"
            text="Upload"
            disabled={!item}
          />
        </form>
      </Form>
      <Input
        className="hidden"
        type="file"
        accept=".png, .jpg"
        ref={ref}
        onChange={onFileChange}
      />
    </div>
  );
};

export default UploadForm;
