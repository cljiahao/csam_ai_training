import { API } from "../../../core/config";

const getCountRand = async () => {
  const resp = await fetch(`${API}/CDA/count_rand`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getCountRand;
