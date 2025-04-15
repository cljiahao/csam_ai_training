import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getAllModels, installModel } from "@/services/api_model";

const useGetModelsMutation = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["evaluateModel"],
    mutationFn: async () => await getAllModels(),
    onSuccess: (data) => {
      queryClient.setQueryData(["allModels"], data);
    },
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["allModels"]); // Clear cache on error
    },
  });
};
const useInstallModelMutation = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["evaluateModel"],
    mutationFn: async ({ item, file_name }) =>
      await installModel(item, file_name),
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["evaluatedModel"]); // Clear cache on error
    },
  });
};

const useModelServices = ({ updateError }) => {
  const { mutateAsync: getModels } = useGetModelsMutation({ updateError });
  const { mutateAsync: installModel } = useInstallModelMutation({
    updateError,
  });
  return {
    state: {},
    action: { getModels, installModel },
  };
};

export default useModelServices;
