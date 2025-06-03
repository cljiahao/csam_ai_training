import Swal from "sweetalert2";

import {
  useGetModelsMutation,
  useInstallModelMutation,
  useQueryAllModels,
} from "@/features/model-bar/api/model-bar";
import { deleteModel } from "@/services/api-ai-model";
import useBaseStore from "@/store/base";

const useModelInstaller = () => {
  const updateError = useBaseStore((state) => state.updateError);

  const { mutateAsync: getModels } = useGetModelsMutation({ updateError });
  const { mutateAsync: installModel } = useInstallModelMutation({
    updateError,
  });

  const allModels = useQueryAllModels();

  function onSubmit(data) {
    const itemModel = allModels.find(
      (model) => model.file_name === data.file_name,
    );
    installModel({ ...itemModel }).then(() =>
      Swal.fire({
        title: "Model Sent!",
        text: "Model Successful Installed into Server.",
        icon: "success",
      }),
    );
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
        deleteModel(item, file_name).then(() =>
          Swal.fire({
            title: "Deleted!",
            text: "Your file has been deleted.",
            icon: "success",
          }),
        );
      }
    });
  }

  return {
    state: { allModels },
    action: { getModels, onSubmit, onModelDelete },
  };
};

export default useModelInstaller;
