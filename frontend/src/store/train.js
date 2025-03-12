import { create } from "zustand";

const initTrain = {
  status: "idle",
};

const useTrainStore = create((set) => ({
  ...initTrain,

  //Define Actions
  resetTrain: () => set(initTrain),
  updateStatus: (status) => set({ status }),
}));

export default useTrainStore;
