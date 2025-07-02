import { create } from "zustand";

import { STATUS } from "@/constants/common";

const initTrain = {
  status: STATUS.IDLE,
};

const useTrainStore = create((set) => ({
  ...initTrain,

  //Define Actions
  resetTrain: () => set(initTrain),
  updateStatus: (status) => set({ status }),
}));

export default useTrainStore;
