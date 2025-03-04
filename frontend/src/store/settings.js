import { create } from "zustand";

const initSettings = {
  item: "",
};

const useSettingsStore = create((set) => ({
  ...initSettings,

  //Define Actions
  resetItem: () => set(initSettings),
  updateItem: (item) => set({ item }),
}));

export default useSettingsStore;
