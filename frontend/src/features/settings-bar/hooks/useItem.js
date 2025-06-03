import useSettingsStore from "@/store/settings";
import { useShallow } from "zustand/react/shallow";

const useItem = () => {
  const { item, updateItem } = useSettingsStore(
    useShallow((state) => ({ item: state.item, updateItem: state.updateItem })),
  );

  const handleOnChange = (e) => {
    updateItem(e.target.value);
  };

  return { state: { item }, action: { handleOnChange } };
};

export default useItem;
