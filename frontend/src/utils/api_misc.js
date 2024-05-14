import { API } from "../core/config";

export const getItemType = async (type) => {
  const resp = await fetch(`${API}/${type}/item_type`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};
