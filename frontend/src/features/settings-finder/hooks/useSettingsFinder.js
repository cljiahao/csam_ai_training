import { useSettingsMutation } from "../api/settings_finder";

const useSettingsFinder = ({ mode, setError }) => {
  const { mutateAsync: processImage } = useSettingsMutation({
    mode,
    setError,
  });

  const handleImageProcess = async (mode, item, targetCount, file) => {
    const formData = new FormData();
    formData.append("file", file);

    const settingsFound = await processImage({
      mode,
      item,
      targetCount,
      formData,
    });
    return settingsFound;
  };

  return {
    state: {},
    action: { handleImageProcess },
  };
};

export default useSettingsFinder;
