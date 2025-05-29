import { useQueryClient } from "@tanstack/react-query";

import { useSettingsMutation } from "@/features/settings-finder/api/settings-finder";
import { useSettingsFinderContext } from "@/features/settings-finder/context/SettingsFinderContext";
import useSettingsStore from "@/store/settings";
import showUploadToast from "../components/showUploadToast";

const useUploadForm = () => {
  const { item } = useSettingsStore();
  const { setImage, setError } = useSettingsFinderContext();

  const queryClient = useQueryClient();
  const { mutateAsync: processImage } = useSettingsMutation({
    setError,
  });

  const onFileChange = async (e, mode, targetCount) => {
    e.preventDefault();
    setError("");

    const file = e.target.files[0];
    if (file) {
      queryClient.removeQueries();

      const fileName = file.name;
      showUploadToast({ mode, item, fileName, targetCount });

      setImage(URL.createObjectURL(file));

      const formData = new FormData();
      formData.append("file", file);
      await processImage({
        mode,
        item,
        targetCount,
        formData,
      });

      e.target.value = null;
    }
  };

  return {
    state: { item },
    action: { onFileChange },
  };
};

export default useUploadForm;
