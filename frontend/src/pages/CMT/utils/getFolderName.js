import { API } from "../../../core/config";

export const getItemType = async () => {
  const resp = await fetch(`${API}/CMT/item_type`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export const getFolderName = async (item) => {
  const resp = await fetch(`${API}/CMT/ds_folders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};

export const getEvalFolder = async (item) => {
  const resp = await fetch(`${API}/CMT/eval_folders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};
