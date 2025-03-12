import useSettingsStore from "./settings";
import useTrainStore from "./train";

export const resetStore = () => {
  useSettingsStore.getState().resetItem();
  useTrainStore.getState().resetTrain();
};
