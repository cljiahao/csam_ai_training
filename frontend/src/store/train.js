import { create } from "zustand";

import { STATUS } from "@/constants/common";

const initTrain = {
  status: STATUS.IDLE,
  selectedModel: null,
};

const useTrainStore = create((set) => ({
  ...initTrain,

  //Define Actions
  resetTrain: () => set(initTrain),
  updateStatus: (status) => set({ status }),
  updateSelectedModel: (selectedModel) => set({ selectedModel }),
}));

export default useTrainStore;
