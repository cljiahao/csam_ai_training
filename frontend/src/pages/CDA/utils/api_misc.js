import { API } from "../../../core/config";

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

export const getRandomCount = async (item) => {
  const resp = await fetch(`${API}/CDA/random_count`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};

export const getRandomness = async (item) => {
  const resp = await fetch(`${API}/CDA/randomness`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};
