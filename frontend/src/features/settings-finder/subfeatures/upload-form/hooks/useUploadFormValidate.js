import { z } from "zod";
import { useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const useUploadFormValidate = () => {
  const uploadFormInfo = {
    quantity: {
      label: "Quantity",
      placeholder: "12345",
      schema: z.coerce.number().int().gt(0),
    },
  };

  const uploadSchema = z.object(
    Object.fromEntries(
      Object.entries(uploadFormInfo).map(([key, { schema }]) => [key, schema]),
    ),
  );

  const uploadForm = useForm({
    resolver: zodResolver(uploadSchema),
    defaultValues: Object.keys(uploadFormInfo).reduce((acc, key) => {
      acc[key] = "";
      return acc;
    }, {}),
  });

  const ref = useRef(null);
  function onSubmit() {
    ref?.current.click();
  }

  return {
    state: { ref, uploadFormInfo },
    action: { onSubmit, uploadForm },
  };
};

export default useUploadFormValidate;
