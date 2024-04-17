import { API } from "../core/config";

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

export const zipModel = async (model_path) => {
  const resp = await fetch(`${API}/CMT/zip_model`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ m_path: model_path }),
  });
  return resp;
};
