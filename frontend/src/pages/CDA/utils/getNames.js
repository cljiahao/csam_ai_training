import { API } from "../../../core/config";

export const getItemType = async () => {
  const resp = await fetch(`${API}/CDA/item_type`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export const getRandomImg = async (item, no_of_img) => {
  const resp = await fetch(`${API}/CDA/random_img`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item, no_of_img: no_of_img }),
  });
  const json = await resp.json();
  return json;
};

export const getRandomCount = async ({ item }) => {
  const resp = await fetch(`${API}/CDA/rand_count`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};
