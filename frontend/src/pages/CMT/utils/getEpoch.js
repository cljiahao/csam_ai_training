import { API } from "../../../core/config";

const getEpoch = async () => {
  const resp = await fetch(`${API}/CMT/current_epoch`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getEpoch;
