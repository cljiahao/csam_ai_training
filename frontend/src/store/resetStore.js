import useSettingsStore from "./settings";

export const resetStore = () => {
  useSettingsStore.getState().resetItem();
};
