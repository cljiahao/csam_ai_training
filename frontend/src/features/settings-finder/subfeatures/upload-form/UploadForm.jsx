import { useQueryClient } from "@tanstack/react-query";

import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { cn } from "@/lib/utils";
import useSettingsStore from "@/store/settings";
import useUploadFormValidate from "./hooks/useUploadFormValidate";
import useSettingsFinder from "../../hooks/useSettingsFinder";
import { useSettingsFinderContext } from "../../contexts/SettingsFinderContext";
import showUploadToast from "./components/showUploadToast";

const UploadForm = ({ className, mode }) => {
  const queryClient = useQueryClient();
  const { item } = useSettingsStore();
  const { setError, setImage } = useSettingsFinderContext();

  const {
    action: { handleImageProcess },
  } = useSettingsFinder({ mode, setError });

  const {
    state: { ref, uploadFormInfo },
    action: { onSubmit, uploadForm },
  } = useUploadFormValidate();

  const onFileChange = async (e) => {
    e.preventDefault();
    setError("");

    const file = e.target.files[0];
    if (file) {
      queryClient.removeQueries();

      const fileName = file.name;
      const targetCount = uploadForm.getValues("quantity");

      setImage(URL.createObjectURL(file));

      showUploadToast({ mode, item, fileName, targetCount });

      await handleImageProcess(mode, item, targetCount, file);

      e.target.value = null;
    }
  };

  return (
    <div className={cn("h-full w-full", className)}>
      <Form {...uploadForm}>
        <form
          onSubmit={uploadForm.handleSubmit(onSubmit)}
          className="flex-center hw-full space-x-8 px-4"
        >
          {Object.keys(uploadFormInfo).map((key) => {
            const { label, placeholder } = uploadFormInfo[key];
            return (
              <CustomFormField
                control={uploadForm.control}
                key={key}
                name={key}
                label={`${mode} ${label}`}
              >
                <Input placeholder={placeholder} />
              </CustomFormField>
            );
          })}
          <HoverButton
            className="w-18 h-4/5"
            type="submit"
            hoverText="Upload"
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
