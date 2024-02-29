import { API } from "../../../core/config";

const getRandom = async (no_of_img) => {
  const resp = await fetch(`${API}/CDA/random/${no_of_img}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getRandom;
