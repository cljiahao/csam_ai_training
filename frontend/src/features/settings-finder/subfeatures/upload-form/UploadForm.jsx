import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import useUploadFormValidate from "./hooks/useUploadFormValidate";
import useUploadForm from "./hooks/useUploadForm";

const UploadForm = ({ mode }) => {
  const {
    state: { item },
    action: { onFileChange },
  } = useUploadForm({ mode });

  const {
    state: { formRef, uploadFormInfo },
    action: { onSubmit, uploadForm },
  } = useUploadFormValidate();

  return (
    <div className="hw-full flex-center">
      <Form {...uploadForm}>
        <form
          onSubmit={uploadForm.handleSubmit(onSubmit)}
          className="flex-center hw-full gap-4"
        >
          {Object.keys(uploadFormInfo).map((key) => {
            const { label, placeholder } = uploadFormInfo[key];
            return (
              <CustomFormField
                className="w-fit"
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
            className="w-18"
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
        ref={formRef}
        onChange={(e) =>
          onFileChange(e, mode, uploadForm.getValues("quantity"))
        }
      />
    </div>
  );
};

export default UploadForm;
