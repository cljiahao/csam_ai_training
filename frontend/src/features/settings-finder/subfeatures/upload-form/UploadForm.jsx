import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { cn } from "@/lib/utils";
import useUploadFormValidate from "./hooks/useUploadFormValidate";
import useUploadForm from "./hooks/useUploadForm";

const UploadForm = ({ className, mode }) => {
  const {
    state: { item },
    action: { onFileChange },
  } = useUploadForm({ mode });

  const {
    state: { ref, uploadFormInfo },
    action: { onSubmit, uploadForm },
  } = useUploadFormValidate();

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
        onChange={(e) =>
          onFileChange(e, mode, uploadForm.getValues("quantity"))
        }
      />
    </div>
  );
};

export default UploadForm;
