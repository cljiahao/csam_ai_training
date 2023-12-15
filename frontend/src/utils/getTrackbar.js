import { API } from "../core/config";

const getTrackbar = async () => {
  const resp = await fetch(`${API}/CDA/trackbar`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getTrackbar;
