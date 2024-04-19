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
