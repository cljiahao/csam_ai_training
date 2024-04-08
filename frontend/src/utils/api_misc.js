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

export const zipModel = async (modelName) => {
  const response = await fetch(`${API}/CMT/zip_model/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ modelname: modelName }),
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }
  const blob = await response.blob();
  return blob;
};
