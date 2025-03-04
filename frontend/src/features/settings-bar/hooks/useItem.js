import useSettingsStore from "@/store/settings";

const useItem = () => {
  const { updateItem } = useSettingsStore();

  const handleOnChange = (e) => {
    updateItem(e.target.value);
  };

  return { state: {}, action: { handleOnChange } };
};

export default useItem;
