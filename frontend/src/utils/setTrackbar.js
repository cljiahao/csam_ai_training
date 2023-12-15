import { API } from "../core/config";

const setTrackbar = async () => {
  const resp = await fetch(`${API}/CDA/trackbar`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default setTrackbar;
