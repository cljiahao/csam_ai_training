import { API } from "../../../core/config";

export const startTraining = async (parameters) => {
  const resp = await fetch(`${API}/CMT/train_model`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(parameters),
  });
  const json = await resp.json();
  return json;
};

export const getEpoch = async () => {
  const resp = await fetch(`${API}/CMT/current_epoch`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};
