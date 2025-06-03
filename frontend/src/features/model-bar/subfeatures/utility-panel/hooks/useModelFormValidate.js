import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const useModelFormValidate = () => {
  const modelFormInfo = {
    file_name: {
      schema: z.string({
        required_error: "Please select a model.",
      }),
    },
  };

  const modelSchema = z.object(
    Object.fromEntries(
      Object.entries(modelFormInfo).map(([key, { schema }]) => [key, schema]),
    ),
  );
  const modelForm = useForm({
    resolver: zodResolver(modelSchema),
    defaultValues: Object.keys(modelFormInfo).reduce((acc, key) => {
      acc[key] = "";
      return acc;
    }, {}),
  });

  return {
    state: { modelFormInfo },
    action: {
      modelForm,
    },
  };
};

export default useModelFormValidate;
