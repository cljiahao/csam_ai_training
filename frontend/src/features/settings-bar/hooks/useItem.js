import useSettingsStore from "@/store/settings";

const useItem = () => {
  const updateItem = useSettingsStore((state) => state.updateItem);

  const handleOnChange = (e) => {
    updateItem(e.target.value);
  };

  return { state: {}, action: { handleOnChange } };
};

export default useItem;
