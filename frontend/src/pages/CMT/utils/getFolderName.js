import { API } from "../../../core/config";

export const getFolderName = async () => {
  const resp = await fetch(`${API}/CMT/ds_folders`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export const getEvalFolder = async () => {
  const resp = await fetch(`${API}/CMT/eval_folders`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};
